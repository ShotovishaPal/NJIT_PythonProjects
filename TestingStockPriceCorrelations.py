import pandas_datareader as web
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt

start = dt.datetime(2022,2,20)
end = dt.datetime.now()

tickers = ["DJIA", "FB", "TSLA", "AAPL", "TWTR", "AMZN", "AMC", "MSFT", "NVDA", "SNAP"]
colnames = []

for ticker in tickers:
    data = web.DataReader(ticker, "yahoo", start, end)
    if len(colnames) == 0:
        combined = data[['Adj Close']].copy()
    else:
        combined = combined.join(data['Adj Close'])
    colnames.append(ticker)
    combined.columns = colnames

# Creating a heatmap using sns seaborn

corr_data = combined.pct_change().corr(method='pearson')
sns.heatmap(corr_data, annot=True, cmap="coolwarm")

plt.show()