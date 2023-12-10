import requests
import pywhatkit
import datetime

now = datetime.datetime.now()
time_hour = now.hour
time_minute = now.minute + 1

print(now)

STOCK_NAME = input("Please input the Stock Name in Exchanges (e.g. NVDA): ")
COMPANY_NAME = input("Please input the actual Company Name(e.g. NVIDIA Corp):")
PHONE_NUMBER = input("Please input your WhatsApp Number w/ Country Code: ")
threshold = int(input("What percentage difference would you want to send the text?: "))


STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
STOCK_API_KEY = "EHGL1SJUYHLB3CDE"
NEWS_API_KEY = "94ae0b563ace46ae83fc42f41eaef314"


stock_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY
}

resp = requests.get(STOCK_ENDPOINT, params=stock_parameters)
data = resp.json()["Time Series (Daily)"]
data_values = [value for (key, value) in data.items()]
yesterday_data = data_values[0]
yesterday_close_price = yesterday_data["4. close"]
two_days_before_data = data_values[1]
two_day_before_close_price = two_days_before_data["4. close"]

difference = (float(yesterday_close_price) - float(two_day_before_close_price))
high_low = ""
if difference > 0:
    high_low = "📈"
else:
    high_low = "📉"

print(difference)
percent_difference = round((difference/float(yesterday_close_price)) * 100)

if abs(percent_difference) > threshold:
    news_parameters = {
        "apiKey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME,
    }
    news_resp = requests.get(NEWS_ENDPOINT, params=news_parameters)
    news_articles = news_resp.json()["articles"]
    top_3_articles = news_articles[:3]
    list_of_3_articles = [f"{STOCK_NAME}: {percent_difference}% {high_low} \n Title: {articles['title']}\n Summary: {articles['description']}" for articles in top_3_articles]
    for article in list_of_3_articles:
        pywhatkit.sendwhatmsg(PHONE_NUMBER, article, time_hour, time_minute)
else:
    pywhatkit.sendwhatmsg(PHONE_NUMBER, f"There has been no meaningful change today {COMPANY_NAME}", time_hour, time_minute)
    print("There has been no meaningful change for ", COMPANY_NAME)
    