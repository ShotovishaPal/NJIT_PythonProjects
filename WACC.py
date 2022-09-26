#WACC = Kd * (1 -Tc) * (D /D+E) + Ke * (E /D+E)
    # WACC = Weighted Average Cost of Capital
    # Kd = Cost of debt
    # Tc = Firm tax rate
    # Ke = Cost of equity
    # D / D + E = Proportion of debt in firm capital structure


import requests
import numpy as np
import pandas as pd
import pandas_datareader.data as web
import datetime

company = 'GOOG'
demo = '518144771fc56140c3b4d53bd431c967'

def interest_coveraga_and_RF(company):
    IS= requests.get(f'https://financialmodelingprep.com/api/v3/income-statement/{company}?apikey={demo}').json()
    #print(IS)
    EBIT= IS[0]['ebitda'] - IS[0]['depreciationAndAmortization'] 
    interest_expense = IS[0]['interestExpense']
    interest_coverage_ratio = EBIT / interest_expense
    print(interest_coverage_ratio) #263.2369942196532
    #print(interest_coveraga_and_RF(company))

    #Risk Free
    start = datetime.datetime(2021, 5, 9)
    end= datetime.datetime.today().strftime('%Y-%m-%d')
    #end = datetime.datetime(2022, 5, 9)

    Treasury = web.DataReader(['TB1YR'], 'fred', start, end)
    RF = float(Treasury.iloc[-1])
    RF = RF/100
    print(RF, interest_coverage_ratio) #RF0.0181 #interest_coverage_ratio-263.2369942196532
    return [RF,interest_coverage_ratio]

interest = interest_coveraga_and_RF(company)
RF = interest[0]
interest_coverage_ratio = interest[1]

#------------

def cost_of_debt(company, RF,interest_coverage_ratio):
        if interest_coverage_ratio > 8.5:
            #Rating is AAA
            credit_spread = 0.0063
        if (interest_coverage_ratio > 6.5) & (interest_coverage_ratio <= 8.5):
            #Rating is AA
            credit_spread = 0.0078
        if (interest_coverage_ratio > 5.5) & (interest_coverage_ratio <=  6.5):
            #Rating is A+
            credit_spread = 0.0098
        if (interest_coverage_ratio > 4.25) & (interest_coverage_ratio <=  5.49):
            #Rating is A
            credit_spread = 0.0108
        if (interest_coverage_ratio > 3) & (interest_coverage_ratio <=  4.25):
            #Rating is A-
            credit_spread = 0.0122
        if (interest_coverage_ratio > 2.5) & (interest_coverage_ratio <=  3):
            #Rating is BBB
            credit_spread = 0.0156
        if (interest_coverage_ratio > 2.25) & (interest_coverage_ratio <=  2.5):
            #Rating is BB+
            credit_spread = 0.02
        if (interest_coverage_ratio > 2) & (interest_coverage_ratio <=  2.25):
            #Rating is BB
            credit_spread = 0.0240
        if (interest_coverage_ratio > 1.75) & (interest_coverage_ratio <=  2):
            #Rating is B+
            credit_spread = 0.0351
        if (interest_coverage_ratio > 1.5) & (interest_coverage_ratio <=  1.75):
            #Rating is B
            credit_spread = 0.0421
        if (interest_coverage_ratio > 1.25) & (interest_coverage_ratio <=  1.5):
            #Rating is B-
            credit_spread = 0.0515
        if (interest_coverage_ratio > 0.8) & (interest_coverage_ratio <=  1.25):
            #Rating is CCC
            credit_spread = 0.0820
        if (interest_coverage_ratio > 0.65) & (interest_coverage_ratio <=  0.8):
            #Rating is CC
            credit_spread = 0.0864
        if (interest_coverage_ratio > 0.2) & (interest_coverage_ratio <=  0.65):
            #Rating is C
            credit_spread = 0.1134
        if interest_coverage_ratio <=  0.2:
            #Rating is D
            credit_spread = 0.1512
    
        cost_of_debt = RF + credit_spread
        print(cost_of_debt)
        return cost_of_debt
        
kd = cost_of_debt(company,RF,interest_coverage_ratio)


def costofequity(company):
    #Risk Free
    start = datetime.datetime(2021, 5, 9)
    end= datetime.datetime.today().strftime('%Y-%m-%d')
    #end = datetime.datetime(2022, 5, 9)
    Treasury = web.DataReader(['TB1YR'], 'fred', start, end)
    RF = float(Treasury.iloc[-1])
    RF = RF/100

#Beta
    beta = requests.get(f'https://financialmodelingprep.com/api/v3/company/profile/{company}?apikey={demo}')
    beta = beta.json()
    beta = float(beta['profile']['beta'])
    
#Market Return
    start = datetime.datetime(2021, 5, 9)
    end= datetime.datetime.today().strftime('%Y-%m-%d')

    SP500 = web.DataReader(['sp500'], 'fred', start, end)
    #Drop all Not a number values using drop method.
    SP500.dropna(inplace = True)
    
    SP500yearlyreturn = (SP500['sp500'].iloc[-1]/ SP500['sp500'].iloc[-252])-1
    
    cost_of_equity = RF+(beta*(SP500yearlyreturn - RF))
    print(cost_of_equity)
    return cost_of_equity

print(costofequity(company))

ke = costofequity(company)

#------------

#effective tax rate and capital structure

def wacc(company):
#effective tax rate
    FR = requests.get(f'https://financialmodelingprep.com/api/v3/ratios/{company}?apikey={demo}').json()
    ETR = FR[0]['effectiveTaxRate']

#capital structure 
    BS = requests.get(f'https://financialmodelingprep.com/api/v3/balance-sheet-statement/{company}?apikey={demo}').json()

    Debt_to = BS[0]['totalDebt'] / (BS[0]['totalDebt'] + BS[0]['totalStockholdersEquity'])
    equity_to = BS[0]['totalStockholdersEquity'] / (BS[0]['totalDebt'] + BS[0]['totalStockholdersEquity'])

#wacc
    WACC = (kd*(1-ETR)*Debt_to) + (ke*equity_to)
    print(WACC,equity_to,Debt_to)
    return WACC

wacc_company = wacc(company)
print('wacc of ' + company + ' is ' + str((wacc_company*100))+'%')