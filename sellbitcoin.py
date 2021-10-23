import time
import pybithumb
import datetime
import requests


con_key = "e0adab55659113a21b209382eeedc90d"
sec_key = "d43f3af07cef1d46f086e012c0c443dc"
myToken = "xoxb-2419582512212-2419602096964-HnE2su3qbfdwnS6NvTFZ713z"


def post_message(token, channel, text):
    """슬랙 메시지 전송"""
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

def buy_crypto_currency(ticker, krw):
    # krw = bithumb.get_balance(ticker)[2]
    orderbook = pybithumb.get_orderbook(ticker)
    sell_price = orderbook['asks'][0]['price']   
    unit = krw/float(sell_price)
    bithumb.buy_market_order(ticker, unit*0.5)


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

prev_dict = {}
tickers = ['BTC', 'ETH', 'ADA', 'BNB', 'XRP', 'BCH', 'DOT', 'DOGE', 'LUNA', 'LTC', 'ALGO']
all_coin = pybithumb.get_current_price("ALL")

for ticker in tickers:
    prev_dict[ticker] = all_coin.get(ticker)['fluctate_rate_24H']

sort_all = sorted(prev_dict.items(), key = lambda x : float(x[1]), reverse=True)
ticker_1 = sort_all[0][0]
ticker_2 = sort_all[1][0]
ticker_3 = sort_all[2][0]
ticker_4 = sort_all[3][0]

print(ticker_1, ticker_2, ticker_3, ticker_4)

krw = bithumb.get_balance(ticker_1)[2]
krw_first = krw / 4
krw_second = krw / 4
krw_third = krw / 4
krw_forth = krw / 4

target_price_1 = get_target_price(ticker_1)
target_price_2 = get_target_price(ticker_2)
target_price_3 = get_target_price(ticker_3)
target_price_4 = get_target_price(ticker_4)
ma5_1 = get_yesterday_ma5(ticker_1)
ma5_2 = get_yesterday_ma5(ticker_2)
ma5_3 = get_yesterday_ma5(ticker_3)
ma5_4 = get_yesterday_ma5(ticker_4)
buy_price_1 = 1
buy_price_2 = 1
buy_price_3 = 1
buy_price_4 = 1          
post_message(myToken,"#engineer", ticker_1 + " Target Price : " + str(target_price_1))
post_message(myToken,"#engineer", ticker_2 + " Target Price : " + str(target_price_2))
post_message(myToken,"#engineer", ticker_3 + " Target Price : " + str(target_price_3))
post_message(myToken,"#engineer", ticker_4 + " Target Price : " + str(target_price_4))


while True:
    try:
        now = datetime.datetime.now()
        if mid + datetime.timedelta(seconds=20) < now < mid + datetime.timedelta(seconds=50):
            # Sell current coin 
            sell_crypto_currency(ticker_1)
            sell_crypto_currency(ticker_2)
            sell_crypto_currency(ticker_3)
            sell_crypto_currency(ticker_4)
            post_message(myToken,"#engineer", "All coin sell completed")

            # WON distribution
            krw = bithumb.get_balance(ticker_1)[2]
            krw_first = krw / 4
            krw_second = krw / 4
            krw_third = krw / 4
            krw_forth = krw / 4

            # coin candidates
            all_coin = pybithumb.get_current_price("ALL")
            for ticker in tickers:
                prev_dict[ticker] = all_coin.get(ticker)['fluctate_rate_24H']
            sort_all = sorted(prev_dict.items(), key = lambda x : float(x[1]), reverse=True)
            ticker_1 = sort_all[0][0]
            ticker_2 = sort_all[1][0]
            ticker_3 = sort_all[2][0]
            ticker_4 = sort_all[3][0]

            yesterday_check = datetime.datetime(now.year, now.month, now.day) - datetime.timedelta(1) 
            mid = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)
            mid_yesterday = mid - datetime.timedelta(1)
            
            # Target Price & MA5
            target_price_1 = get_target_price(ticker_1)
            target_price_2 = get_target_price(ticker_2)
            target_price_3 = get_target_price(ticker_3)
            target_price_4 = get_target_price(ticker_4)
            ma5_1 = get_yesterday_ma5(ticker_1)
            ma5_2 = get_yesterday_ma5(ticker_2)
            ma5_3 = get_yesterday_ma5(ticker_3)
            ma5_4 = get_yesterday_ma5(ticker_4)
            buy_price_1 = 1
            buy_price_2 = 1
            buy_price_3 = 1
            buy_price_4 = 1    
            post_message(myToken,"#engineer", ticker_1 + " Target Price : " + str(target_price_1))
            post_message(myToken,"#engineer", ticker_2 + " Target Price : " + str(target_price_2))
            post_message(myToken,"#engineer", ticker_3 + " Target Price : " + str(target_price_3))
            post_message(myToken,"#engineer", ticker_4 + " Target Price : " + str(target_price_4))       
    
        current_price_1 = pybithumb.get_current_price(ticker_1)
        current_price_2 = pybithumb.get_current_price(ticker_2)
        current_price_3 = pybithumb.get_current_price(ticker_3)
        current_price_4 = pybithumb.get_current_price(ticker_4)
                
        if (current_price_1 > target_price_1) and (current_price_1 > ma5_1):
            if (now > mid_yesterday + datetime.timedelta(minutes=5)):
                buy_crypto_currency(ticker_1, krw_1)
                buy_price_1 = current_price_1
                # post_message(myToken,"#engineer", "BTC buy completed") 
        
        if (current_price_2 > target_price_2) and (current_price_2 > ma5_2):
            if (now > mid_yesterday + datetime.timedelta(minutes=5)):
                buy_crypto_currency(ticker_2, krw_2)
                buy_price_2 = current_price_2
                # post_message(myToken,"#engineer", "BTC buy completed") 
        
        if (current_price_3 > target_price_3) and (current_price_3 > ma5_3):
            if (now > mid_yesterday + datetime.timedelta(minutes=5)):
                buy_crypto_currency(ticker_3, krw_3)
                buy_price_3 = current_price_3
                # post_message(myToken,"#engineer", "BTC buy completed") 
        
        if (current_price_4 > target_price_4) and (current_price_4 > ma5_4):
            if (now > mid_yesterday + datetime.timedelta(minutes=5)):
                buy_crypto_currency(ticker_4, krw_4)
                buy_price_4 = current_price_4
                # post_message(myToken,"#engineer", "BTC buy completed") 
         
        rate_1 = (current_price_1 - buy_price_1) / buy_price_1 * 100
        rate_2 = (current_price_2 - buy_price_2) / buy_price_2 * 100
        rate_3 = (current_price_3 - buy_price_3) / buy_price_3 * 100
        rate_4 = (current_price_4 - buy_price_4) / buy_price_4 * 100
     
        if rate_1 < -5:
            sell_crypto_currency(ticker_1)
        if rate_2 < -5:
            sell_crypto_currency(ticker_2)
        if rate_3 < -5:
            sell_crypto_currency(ticker_3)
        if rate_4 < -5:
            sell_crypto_currency(ticker_4)

    except:
        print("Error!")
        post_message(myToken,"#engineer", "Error!")         
    time.sleep(5)

