import yfinance as yf
import matplotlib.pyplot as plt

data = yf.download("BTC-USD", start="2020-01-01", end="2025-09-26", interval="1d")
#data = yf.download("BTC-USD", period = "1d", interval = "1m")
print(type(data)) # <class 'pandas.core.frame.DataFrame'>

print(data.head()) # Display the first few rows of the DataFrame

plt.figure(figsize=(12, 6))
plt.plot(data['Close'], label='BTC-USD Close Price')
plt.title('Bitcoin Price Chart')
plt.xlabel('Date')
plt.ylabel('Price (USD)')
plt.legend()
plt.savefig(r'bitcoin_price_chart.png')
plt.show()