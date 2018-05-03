import numpy as np
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import pandas_datareader.data as web

start = datetime.datetime(2010,1,1)
end = datetime.datetime.now()
sp500=web.DataReader('GOOG','morningstar',start,end)

#based on 60days & 252days influctuation(moving average
df =pd.DataFrame(sp500['Close'])

sp500['60d']=np.round(df.rolling(window=60).mean(),2)
sp500['252d']=np.round(df.rolling(window=252).mean(),2)

sp500['60-252'] = sp500['60d'] - sp500['252d']
fig, axes = plt.subplots(3,1)
sp500[['Close','60d','252d']].plot(grid=True, ax=axes[0])


# Long 1, Short -1
SD=0.5
sp500['Regime'] = np.where(sp500['60-252'] > SD, 1 ,0)
sp500['Regime'] = np.where(sp500['60-252'] < -SD, -1 ,sp500['Regime'])
print(sp500['Regime'].value_counts()) #Returns object containing counts of unique values.
sp500['Regime'].plot(grid=True,lw=1.5,ax=axes[1])
fig.autofmt_xdate()
# plt.ylim([-1.1, 1.1])

# shift method: Logarithm Profit every day
sp500['Market'] = np.log(sp500['Close'] / sp500['Close'].shift(1)) #shift one trading day

# Regime * Returns at next day = profit of today
sp500['Strategy'] = sp500['Regime'].shift(1)*sp500['Market']

# exponentially accumulative profit 
sp500[['Market','Strategy']].cumsum().apply(np.exp).plot(figsize=(8,5),grid=True,ax=axes[2])
plt.show()
