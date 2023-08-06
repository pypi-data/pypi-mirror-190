from finbright_technical import technical
import yfinance as yf

tickers = ['BTC-USD']
# Date range
start = "2020-11-09"
end = "2022-11-29"

data = yf.download(tickers, start=start, end=end)
print(data)

output = technical.calc_EMA(dataFrame=data ,period=14)
print(output)