# Spark Streaming Project: Sentiment Analysis and Clustering

## Overview

This project involves processing API data as a stream, performing sentiment analysis on the textual data, and clustering the messages based on sentiment and location. The project also includes creating a dynamic dashboard to visualize the cluster sizes in sliding windows. ([link](https://www.lri.fr/~groz/documents/m1ai-2022/docs-exercices/miniproject-spark.pdf))

## Team Members
- Dana Aubakirova
- Diego Andres Torres Guarin
- Benedictus Kent Rachmat

## Project Structure
- `server.py` : Python server script to connect to the API and send individual messages to a socket.
- `spark.py` and `analyze.py` : Spark Streaming script to read data, perform sentiment analysis, clustering, and window operations.
- `main.ipynb` : Jupyter Notebook for visualizing the cluster sizes in sliding windows.

## Requirements
- Python 3.x
- Pyspark
- TextBlob
- Jupyter Notebook
- Matplotlib, Seaborn, or Plotly (for visualization)

## Instructions
### Step 1: Set up the API and Python server
Register and obtain access to [NEWS API](https://newsapi.org/) and run Docker with the following command : 
```bash
$ docker exec -it sparklab bash

# if you haven't install the image
$ docker run --name sparklab -it --rm --user root -e GRANT_SUDO=yes \
-p 8888:8888 -p 4040:4040 -p 4041:4041 \
jupyter/pyspark-notebook
```

### Step 2: Run the project
```bash
# to run the server
$ python server.py

# to run spark streaming 
$ python analyze.py
```
### Step 3: Visualize data
