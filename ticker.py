import pybithumb
import time

tickers = pybithumb.get_tickers()
print(tickers)
# for ticker in tickers:
#     price = pybithumb.get_current_price(ticker)
#     print(ticker, price)
#     time.sleep(0.1)

while True:
     price = pybithumb.get_current_price("XRP")
     print(price)
     time.sleep(1)