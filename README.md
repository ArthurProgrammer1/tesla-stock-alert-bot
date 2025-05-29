# Tesla Stock Alert Bot 📈📲

This Python script tracks Tesla Inc. (TSLA) stock price using the Alpha Vantage API. If the price fluctuates by more than ±5%, it fetches related news headlines via the News API and sends a concise SMS alert using Twilio.

## Features
- Monitors TSLA stock's daily close price
- Calculates percent change from the previous day
- Sends SMS alerts when the stock moves ±5% or more
- Fetches and includes up to 3 business news headlines in the message

## Setup

### Prerequisites
- Python 3.x
- Alpha Vantage API Key
- News API Key
- Twilio Account (SID, Auth Token, phone numbers)
