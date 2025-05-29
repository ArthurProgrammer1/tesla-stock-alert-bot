from newsapi import NewsApiClient
from twilio.rest import Client
import requests
import os
from dotenv import load_dotenv

load_dotenv()

STOCK = 'TSLA'
COMPANY_NAME = 'Tesla Inc'
ALPHA_KEY = os.getenv("ALPHA_KEY")
NEWS_KEY = os.getenv("NEWS_KEY")
TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_TOKEN = os.getenv("TWILIO_TOKEN")
FROM = os.getenv("TWILIO_FROM")
TO = os.getenv("MY_PHONE")

stock_url = "https://www.alphavantage.co/query"
stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": ALPHA_KEY
}
stock_response = requests.get(stock_url, params=stock_params)
stock_data = stock_response.json()["Time Series (Daily)"]

dates = sorted(stock_data.keys(), reverse=True)
yesterday = float(stock_data[dates[0]]["4. close"])
day_before = float(stock_data[dates[1]]["4. close"])
difference = yesterday - day_before
percent_change = (difference / day_before) * 100
direction = "🔺" if percent_change > 0 else "🔻"

def generate_news():
    news_api = NewsApiClient(api_key=NEWS_KEY)
    return news_api.get_top_headlines(
        q=COMPANY_NAME,
        category='business',
        language='en',
        country='us'
    )

def check():
    client = Client(TWILIO_SID, TWILIO_TOKEN)

    if abs(percent_change) >= 5:
        response = generate_news()
        if response["status"] == "ok":
            articles = response["articles"][:3]
            for article in articles:
                msg = (
                    f"{STOCK}: {direction}{abs(percent_change):.2f}%\n"
                    f"Headline: {article['title']}\n"
                    f"Brief: {article['description']}"
                )
                message = client.messages.create(
                    body=msg,
                    from_=FROM,
                    to=TO
                )
                print(f"Message sent: {message.status}")
        else:
            print("News API error:", response.get("message"))
    else:
        msg = f"{STOCK} update: {direction}{abs(percent_change):.2f}% change.\nNo significant movement today."
        message = client.messages.create(
            body=msg,
            from_=FROM,
            to=TO
        )
        print(f"Message sent (no change): {message.status}")

check()