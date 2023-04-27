import requests
import os
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
stock_api = os.environ['STOCK_API']
stock_url = "https://www.alphavantage.co/query?"

stock_params = {
    "function": "TIME_SERIES_DAILY_ADJUSTED",
    "symbol": STOCK,
    "apikey": stock_api
}

stock_res = requests.get(stock_url, stock_params)
stock_data = stock_res.json()["Time Series (Daily)"]
stock_price = []

for stock in stock_data:
    stock_price.append(stock_data[stock]["4. close"])

current_day = float(stock_price[0])
previous_day = float(stock_price[1])
diff = abs(current_day - previous_day)
diff_percentage = round(((diff/current_day)*100), 2)

## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.
news_api = os.environ["NEWS_API"]
news_url = "https://newsapi.org/v2/everything"

news_params = {
    "q": COMPANY_NAME,
    "from": "2023-03-27",
    "sortBy": "publishedAt",
    "apiKey": news_api
}

news_res = requests.get(news_url, news_params)
news_data = news_res.json()["articles"][0:3]

## STEP 3: Use https://www.twilio.com
# Send a separate message with the percentage change and each article's title and description to your phone number.
account_sid = os.environ["TWILIO_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]
from_number = os.environ["FROM_NUMBER"]
to_number = os.environ["TO_NUMBER"]

client = Client(account_sid, auth_token)

if diff_percentage > 3:

    for article in news_data:
        description = article["description"]
        title = article["title"]
        sms_message = f"{STOCK}: {diff_percentage} \nHeadline: {title} \nBrief: {description}"
        message = client.messages.create(
                                      from_=from_number,
                                      body=sms_message,
                                      to=to_number
                                  )
# print(message.sid)

# Optional: Format the SMS message like this:
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file
 by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the 
 coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file
 by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the
  coronavirus market crash.
"""
