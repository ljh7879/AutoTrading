import pybithumb
 
con_key = "78d5c7cea79e32fedaa782a5093dd4c5"
sec_key = "ad9108675991fcaeb3b8b433dbe0a33b"

bithumb = pybithumb.Bithumb(con_key, sec_key)

balance = bithumb.get_balance("BTC")
print(balance)

krw = bithumb.get_balance("BTC")[1]
orderbook = pybithumb.get_orderbook("XRP")
print(krw)

# asks = orderbook['asks']
# sell_price = asks[0]['price']
# unit = krw/sell_price
# print(unit)