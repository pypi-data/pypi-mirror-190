# tothemoon evx ML model

This is a simplified version of [evxpredictor](https://pypi.org/project/evxpredictor/) package used to generate buy and sell signals for crypto and conventional stock markets based on the excess volume indicator(EVX). EVX is a concept where the bid-ask spread is estimated inherently from current market prices. 

You can read more about Evx in the free whitepaper [here](https://www.researchgate.net/publication/345313655_DeFiPaper)  
# Installation
Install tothemoon with `python3 -m pip install tothemoon`  
# Usage

In your python script simply import the module and use as follows:

```  
from tothemoon.moon import signal
print(signal(20,65,utcdatetime))
```
The above methods take an assets open, close prices of the asset based on the time interval you have chosen in OHCLV type. A zero classification output would instruct the user to sell, while one output means don't sell or buy if the asset is not already present in the orders.  

# Testing an entire dataframe
Testing of a dataframe for correct buy, sell signals is as simple as applying the function as follows:  

```
import pandas as pd
from moon import signal, Regbot

df = pd.read_csv('path/toyour/file.csv')

def getSignal(open,close,utcdatetime):
    return signal(open,close,utcdatetime)

# select long profitable trades
df2 = df[df['close_profit_abs'] > 0]
df2 = df2[df2['is_short'] == 0]
print(df2.head())

# Run all predictions
df2['enter_long_pred'] = df.apply(lambda row: getSignal(row['open'], row['close'], row['date']), axis=1)

print(len(df2[df2['enter_long_pred'] == df2['is_short']]), len(df) )

print(df2[df2['is_short']==0].head(15))

```

Your original data must already have some presumed 'buy' signal.

# Warning
This is not financial advise. tothemoon is entirely on its preliminary stages. Use it at your own risk.