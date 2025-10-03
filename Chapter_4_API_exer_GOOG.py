import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

# Download data
#data = yf.download("GOOG", period="1y", interval="1d")
data = yf.download(["AAPL", "MSFT", "TSLA"], start="2020-01-01", end="2025-09-26", interval="1d")["Close"]

# Display data info
print(data.head())
print(data.tail())
print(data.shape)

# Plot
#fig, ax = plt.subplots()
fig, ax = plt.subplots(nrows=1, ncols=3, sharey=True)
ax[0].plot(data.AAPL)
ax[0].set_title("AAPL Closing Prices")
ax[0].set_xlabel("Date")
ax[0].set_ylabel("Price (USD)")
ax[0].ticklabel_format(axis='y', style='plain')
ax[1].plot(data.MSFT)
ax[1].set_title("MSFT Closing Prices")
ax[1].set_xlabel("Date")
ax[1].set_ylabel("Price (USD)")
ax[1].ticklabel_format(axis='y', style='plain')
ax[2].plot(data.TSLA)
ax[2].set_title("TSLA Closing Prices")
ax[2].set_xlabel("Date")
ax[2].set_ylabel("Price (USD)")
ax[2].ticklabel_format(axis='y', style='plain')
fig.tight_layout()

plt.show()

