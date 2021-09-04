import time
import pybithumb
import datetime
import requests

con_key = "e0adab55659113a21b209382eeedc90d"
sec_key = "d43f3af07cef1d46f086e012c0c443dc"
myToken = "xoxb-2419582512212-2419602096964-4GFKQCsNLCwvJ3uM2cuARiJR"

def post_message(token, channel, text):
    response = requests.post("https://slack.com/api/chat.postMessage",
        headers={"Authorization": "Bearer "+token},
        data={"channel": channel,"text": text}
    )


bithumb = pybithumb.Bithumb(con_key, sec_key)

def get_target_price(ticker):
    df = pybithumb.get_ohlcv(ticker)
    yesterday = df.loc[yesterday_check]
    today_open = yesterday['close']
    yesterday_high = yesterday['high']
    yesterday_low = yesterday['low']
    target = today_open + (yesterday_high - yesterday_low) * 0.2
    return target

def buy_crypto_currency(ticker):
    krw = bithumb.get_balance(ticker)[2]
    orderbook = pybithumb.get_orderbook(ticker)
    sell_price = orderbook['asks'][0]['price']   
    unit = krw/float(sell_price)
    bithumb.buy_market_order(ticker, unit)

def sell_crypto_currency(ticker):
    unit = bithumb.get_balance(ticker)[0]
    bithumb.sell_market_order(ticker, unit)

def get_yesterday_ma5(ticker):
    df = pybithumb.get_ohlcv(ticker)
    close = df['close']
    ma = close.rolling(5).mean()
    return ma[-2]

now = datetime.datetime.now()
mid = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)
yesterday_check = datetime.datetime(now.year, now.month, now.day) - datetime.timedelta(1)
ma5 = get_yesterday_ma5("ETH")
target_price = get_target_price("ETH")
post_message(myToken,"#engineer", "autotrade start" + "target_price : " + str(target_price))

while True:
    try:
        now = datetime.datetime.now()
        print(now)
        if mid < now < mid + datetime.delta(seconds=10): 
            target_price = get_target_price("ETH")
            mid = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)
            ma5 = get_yesterday_ma5("ETH")
            sell_crypto_currency("ETH")
            post_message(myToken,"#engineer", "Coin sell completed")
    
        current_price = pybithumb.get_current_price("ETH")          
        if (current_price > target_price) and (current_price > ma5):
            if (now > mid + datetime.timedelta(minutes=2)):
                buy_crypto_currency("ETH")
                post_message(myToken,"#engineer", "Coin buy completed" + "target price : " + str(target_price)) 

    except:
        print("에러 발생")        
    time.sleep(1)
