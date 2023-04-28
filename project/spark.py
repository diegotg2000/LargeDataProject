from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from textblob import TextBlob
import json
import re

PORT = 9998

def extract_text(article):
    if not article['content']:
        return article['title']
    article_content = re.sub(r'\[\+\d+ chars\]', '', article['content'])
    return article_content + article['title']

def sentiment_analysis(article):
    # perform sentiment analysis only for title
    text = extract_text(article)
    analysis = TextBlob(text)
    sentiment = analysis.sentiment.polarity
    article['sentiment'] = sentiment
    return article

def process_article(time, rdd): 
    print(f"========== 🕐 {str(time)} ==========") 
    articles = rdd.map(lambda x: json.loads(x)).map(sentiment_analysis).collect()
    for article in articles:
        print(article['title'])
        print(article['content'])
        print(f"Sentiment: {article['sentiment']}")
        print()
        
        
if __name__ == "__main__":
    sc = SparkContext("local[2]", "NewsAPI Sentiment Analysis")
    sc.setLogLevel("ERROR")  
    ssc = StreamingContext(sc, 5)

    lines = ssc.socketTextStream('localhost', PORT).flatMap(lambda x: x.split('\n'))
    lines.foreachRDD(process_article)

    ssc.start()
    ssc.awaitTermination()
