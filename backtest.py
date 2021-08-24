import pybithumb
import numpy as np

df = pybithumb.get_ohlcv("BTC", payment_currency="KRW", interval="day")
df = df.loc['2021']

df['range'] = (df['high'] - df['low']) 
df['target'] = df['open'] + df['range'].shift(1) * 0.7
df['noise'] = 1 - abs(df['open']-df['close']) / (df['high'] - df['low'])
df['noise_ma20'] = df['noise'].rolling(window=5, min_periods=1).mean()
df['target_noise'] = df['open'] + df['range'].shift(1) * df['noise_ma20']

fee = 0.0032
df['ror'] = np.where(df['high'] > df['target_noise'],
                     df['close'] / df['target_noise'] - fee,
                     1)


df['hpr'] = df['ror'].cumprod()
df['dd'] = (df['hpr'].cummax() - df['hpr']) / df['hpr'].cummax() * 100
print("MDD(%): ", df['dd'].max())

print(df)
df.to_excel("dd.xlsx")