#Python code to compute the daily returns in percentage, of Dow Stocks
#calls function StockReturnsComputing to compute asset returns

#dependencies
import numpy as np
import pandas as pd

#input stock prices dataset
stockFileName = (r'G:\NJIT\02_Courses\03_Wed_FIN 620 - Adv. Financial Data Analysis - Stephen\Project2\Dow Jones_Historical Data.xlsx')
rows = 10  #excluding header
columns = 29  #excluding date

#read stock prices 
df = pd.read_excel(stockFileName, nrows= rows)

#extract asset labels
assetLabels = df.columns[1:columns+1].tolist()
print(assetLabels)

#extract asset prices data
stockPrice = df.iloc[0:, 1:]
print(stockPrice.shape)

#print stock price
print(stockPrice)


#function to compute asset returns 
def StockReturnsComputing(StockPrice, Rows, Columns):
    
    import numpy as np
    
    StockReturn = np.zeros([Rows-1, Columns])
    for j in range(Columns):        # j: Assets
        for i in range(Rows-1):     # i: Daily Prices
            StockReturn[i,j]=((StockPrice[i+1, j]-StockPrice[i,j])/StockPrice[i,j])* 100

    return StockReturn

#------------------------------------------------------

#compute daily returns in percentage of the Dow stocks

import numpy as np

stockPriceArray = np.asarray(stockPrice)
[Rows, Cols]=stockPriceArray.shape
stockReturns = StockReturnsComputing(stockPriceArray, Rows, Cols)
print('Daily returns of selective Dow 30 stocks\n', stockReturns)

#compute mean returns and variance covariance matrix of returns
meanReturns = np.mean(stockReturns, axis = 0)
print('Mean returns of Dow Stocks:\n',  meanReturns)

covReturns = np.cov(stockReturns, rowvar=False)
print('Variance-covariance matrix of returns of Dow Stocks:\n')
print(covReturns)

#------------------------------------------------------

#compute betas of Dow stocks over a 3-year historical period,
#DJIA Index- April 2019 to April 2022

#dependencies
import numpy as np
import pandas as pd

#input stock prices and market datasets
stockFileName = (r'G:\NJIT\02_Courses\03_Wed_FIN 620 - Adv. Financial Data Analysis - Stephen\Project2\DowStocks_PortfolioP_Apr2019to2022_Beta.xlsx')
marketFileName = (r'G:\NJIT\02_Courses\03_Wed_FIN 620 - Adv. Financial Data Analysis - Stephen\Project2\DJIA_MarketData_Apr2019to2022_Beta.xlsx')
stockRows = 758  #excluding header 
stockColumns = 15  #excluding date
marketRows = 758
marketColumns = 6

#read stock prices dataset and market dataset 
dfStock = pd.read_excel(stockFileName,  nrows= stockRows)
dfMarket = pd.read_excel(marketFileName, nrows = marketRows)

#extract asset labels of stocks in the portfolio
assetLabels = dfStock.columns[1:stockColumns+1].tolist()
print('Portfolio stocks\n', assetLabels)

#extract asset prices data and market data
stockData = dfStock.iloc[0:, 1:]
marketData = dfMarket.iloc[0:, [4]] #closing price 

#compute asset returns
arrayStockData = np.asarray(stockData)
[sRows, sCols]=arrayStockData.shape
stockReturns = StockReturnsComputing(arrayStockData, sRows, sCols)

#compute market returns
arrayMarketData = np.asarray(marketData)
[mRows, mCols]=arrayMarketData.shape
marketReturns = StockReturnsComputing(arrayMarketData, mRows, mCols)

#compute betas of assets in the portfolio
beta= []
Var = np.var(marketReturns, ddof =1)
for i in range(stockColumns):
    CovarMat = np.cov(marketReturns[:,0], stockReturns[:, i ])
    Covar  = CovarMat[1,0]
    beta.append(Covar/Var)
    
    
#output betas of assets in the portfolio
print('Asset Betas:  \n')
for data in beta:
    print('{:9.3f}'.format(data))

#------------------------------------------------------

#portfolio risk, expected return and portfolio beta computation

#input weights and asset betas for portfolio P 
weights = np.array([0.15, 0.08, 0.06, 0.02, 0.04, 0.04, 0.1, 0.04, 0.08, \
                    0.08, 0.05, 0.07, 0.07, 0.04, 0.08])
assetBeta = np.array([1.03, 0.69, 1.47, 1.74, 1.02, 0.95, 0.94, 1.24, 1.04,\
                      1.27, 1.00, 1.09, 0.93, 1.08, 0.60])

#compute mean and covariance of asset returns of portfolio P available in stockReturns
meanReturns = np.mean(stockReturns, axis = 0)
covReturns = np.cov(stockReturns, rowvar=False)

#compute portfolio risk
portfolioRisk = np.matmul((np.matmul(weights,covReturns)), np.transpose(weights))

#compute annualized portfolio risk for trading days = 251
annualizedRisk  =   np.sqrt(portfolioRisk*251) 

#compute expected portfolio return
portfolioReturn = np.matmul(np.array(meanReturns),weights.T)

#compute annualized expected portfolio return
annualizedReturn = 251*np.array(portfolioReturn) 

#compute portfolio beta
portfolioBeta = np.matmul(assetBeta,weights.T)

#display results
print("\n Annualized Portfolio Risk: %4.2f" % annualizedRisk,"%")
print("\n Annualized Expected Portfolio Return: %4.2f" % annualizedReturn,"%")
print("\n Portfolio Beta:%4.2f" % portfolioBeta)