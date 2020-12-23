from pykrx import stock
df = stock.get_market_ohlcv_by_date("20180810", "20181212", "005930")
print(df.head(3))
df = stock.get_market_cap_by_date("20190101", "20190131", "005930")
print(df.head())