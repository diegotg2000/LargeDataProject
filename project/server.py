import requests
import time
import json
import socket

NEWSAPI_KEY = 'f0da6281add04d428709b050f9e7e415'
PORT = 9998


def fetch_articles():
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWSAPI_KEY}"
    response = requests.get(url)
    data = response.json()
    return data['articles']

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', PORT))
    server_socket.listen(1)
    print("🚧 Waiting for connection...")

    client_socket, _ = server_socket.accept()
    print("✅ Connection established.")
    
    while True:
        articles = fetch_articles()
        for article in articles:
            print(article)
            message = json.dumps(article)
            client_socket.send((message + '\n').encode('utf-8'))
            print("📩 Message sent :\n",message)
            time.sleep(1)  # Send one message per second

        time.sleep(120) 

if __name__ == "__main__":
    main()