# stock news monitoring
import requests
from smtplib import SMTP
from data import STOCK_API_KEY, NEWS_API_KEY, MY_EMAIL, MY_PASSWORD, RECIEVERS_EMAIL
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
STOCK_ENDPOINT="https://www.alphavantage.co/query"
NEWS_ENDPOINT="https://newsapi.org/v2/everything"


stock_parameters={
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": STOCK_API_KEY,
}
stock_response=requests.get(STOCK_ENDPOINT, stock_parameters)
stocks_each_day=stock_response.json()["Time Series (Daily)"]
# print(stocks_each_day)
stock_list=[{"date": date, "close": float(stock_data['4. close'])} for (date, stock_data) in stocks_each_day.items()]
# print(stock_list)
yesterday_price=round(stock_list[0]['close'],2)
day_before_yesterday_price=round(stock_list[1]['close'],2)
# print(yesterday_price)
# print(day_before_yesterday_price)
stock_price_difference=round(yesterday_price - day_before_yesterday_price, 2)
# print(stock_price_difference)
percentage_differenece=round(stock_price_difference/yesterday_price*100, 2)
# print(percentage_differenece)

news_params={
    "apiKey": NEWS_API_KEY,
    "qInTitle": COMPANY_NAME,
}
news_response=requests.get(url=NEWS_ENDPOINT, params=news_params)
articles=news_response.json()["articles"]
# print(articles)
top_3_artles=articles[:3]
print(top_3_artles)

formatted_articles=[f'Headline: {artilce["title"]}\n\n{artilce["description"]}\nread more: {artilce["url"]}\n\nsource:{artilce["source"]["name"]}\n\n' for artilce in top_3_artles]
print(formatted_articles[0])
def send_mail(imoji: str, stock_name, percentage_diff, articles):
    with SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=MY_PASSWORD)
        connection.sendmail(from_addr=MY_EMAIL, to_addrs=RECIEVERS_EMAIL, msg=f'subject: Stocks Alert\n\n{stock_name}: {imoji}{abs(percentage_diff)}%\n{articles[0]}\n{articles[1]}\n{articles[2]}'.encode('utf-8'))
if stock_price_difference>0:
    send_mail(imoji="🔺", stock_name=STOCK, percentage_diff=percentage_differenece, articles=formatted_articles)
else:
    send_mail(imoji="🔻", stock_name=STOCK, percentage_diff=percentage_differenece, articles=formatted_articles)



