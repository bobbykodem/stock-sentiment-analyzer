import requests
from textblob import TextBlob
import yfinance as yf
from google.cloud import language_v1


# Fetch news data and parse it into a single clean string
def fetch_stock_news(stock_symbol):
    url = f'https://newsapi.org/v2/everything?q={stock_symbol}&apiKey=8cd9302b8da84fbcbb5d62a8b0b28153'
    response = requests.get(url)
    text_data = ""
    if response.status_code == 200:
        data = response.json()
        for article in data['articles']:
            # Extract title, description, and content
            title = article.get('title', '')
            description = article.get('description', '')
            content = article.get('content', '')
            
            # Combine the text data from each article
            article_text = f"{title} {description} {content}"
            text_data += article_text + " "
    else:
        print("Failed to fetch data:", response.status_code)
        print(response.text)
    return text_data.strip()


# Perform sentiment analysis using TextBlob, return a rating between 0 and 100
def analyze_sentiment_TB(text_data):
    analysis = TextBlob(text_data)
    polarity = analysis.sentiment.polarity  # Polarity score: -1 to 1
    return polarity




def analyze_sentiment_google(text):
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    sentiment = client.analyze_sentiment(request={'document': document}).document_sentiment
    return sentiment.score  # Returns a score between -1 and 1


def analyze_sentiment(stock):
    news_data = fetch_stock_news(stock)
    normalized_TBscore = ((analyze_sentiment_TB(news_data) + 1) / 2) * 100
    normalized_google_score = ((analyze_sentiment_google(news_data) + 1) / 2) * 100
    total = 0.5 * normalized_TBscore + 0.5 * normalized_google_score

    return total


print(analyze_sentiment("AAPL"))