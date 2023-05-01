from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.mllib.clustering import StreamingKMeans
from pyspark.mllib.linalg import Vectors
from pyspark.mllib.regression import LabeledPoint
from textblob import TextBlob
import json
import re
import csv
import pandas as pd

PORT = 9998

def extract_text(article):
    if not article['content']:
        return article['title']
    article_content = re.sub(r'\[\+\d+ chars\]', '', article['content'])
    return article_content + article['title']

def sentiment_analysis(article):
    text = extract_text(article)
    analysis = TextBlob(text)
    sentiment = analysis.sentiment.polarity
    article['sentiment'] = sentiment
    return article

def print_predictions(time, rdd):
    print(f"========== 🕐 {str(time)} ==========") 
    for prediction in rdd.collect():
        (title, sentiment), cluster = prediction
        print(f"Title: {title}")
        print(f"Sentiment: {sentiment}")
        print(f"Cluster: {cluster}")
        print()
        
def save_predictions(time, rdd):
    print('Saving to file...')
    current_file = pd.read_csv('predictions.csv')
    rows = []
    for prediction in rdd.collect():
        (title, sentiment), cluster = prediction
        rows.append([title, sentiment, cluster])
        
    new_file = pd.DataFrame(rows, columns=['Title', 'Sentiment', 'Cluster'])
    
    print(new_file)
    
    print(current_file)
        
    updated_file = pd.concat([current_file[~current_file['Title'].isin(new_file['Title'])], new_file], axis=0, ignore_index=True)
    updated_file.to_csv('predictions.csv', index=False)
            
            

if __name__ == "__main__":
    sc = SparkContext("local[2]", "NewsAPI Sentiment Analysis")
    ssc = StreamingContext(sc, 5)
    sc.setLogLevel("ERROR") 
    
    model = StreamingKMeans(k=3, decayFactor=1.0).setRandomCenters(1, 0.01, 42)
    
    lines = ssc.socketTextStream('localhost', PORT).map(lambda x: json.loads(x))\
                                                   .map(sentiment_analysis)\
                                                   .filter(lambda x: 'sentiment' in x)\
                        

    # Add window operation
    window_length = 30   
    sliding_interval = 10   
    windowed_lines = lines.window(window_length, sliding_interval).map(lambda x: ((x['title'], x['sentiment']), 
                                                                                 Vectors.dense(x['sentiment'])))
    
    
    training_data = windowed_lines.map(lambda x: x[1])
    
    model.trainOn(training_data)
    
    predictions = model.predictOnValues(windowed_lines)
    
    predictions.foreachRDD(print_predictions)
    
    predictions.foreachRDD(save_predictions)
        
    ssc.start()
    ssc.awaitTermination()