import requests
import pandas as pd
import numpy as np
from pandas import read_csv
import glob
import time
import datetime
import os
import os.path

# Get Stock Tickers
ticker = read_csv('/Data/TICKER.csv',header = None)  # e.g. 0001.HK
path = '/Data/'
IDList = list(ticker[0])
IDList.sort()

# Set Dates
start = '01/01/2015'
end = str(int(time.time()))
stamp = datetime.datetime.strptime(start, "%d/%m/%Y").timestamp()
stamp = str(int(stamp))

# Download Data from yahoo finance
for i in IDList:
  site = 'https://query1.finance.yahoo.com/v7/finance/download/' + i + '?period1='+ stamp + '&period2=' + end + '&interval=1d&events=history&crumb=hP2rOschxO0'
  ##wk; mo; d
  response = requests.post(site)
  idint = i.replace('.HK','')
  save = path + 'Raw Data/' + idint + '.csv'
  dirname = os.path.dirname(save)
  if not os.path.exists(dirname):
    os.makedirs(dirname)
  with open(save , 'w') as f:
    f.writelines(response.text)
    print(i)

# Format the data
filenames = glob.glob(path + 'Raw Data/' + "/*.csv")
Files = []
for name in filenames:
    df = read_csv(name, header=0, index_col=None)
    df = df.sort_values(by=['Date'])
    col = name.replace(path + 'Raw Data/', '')
    col = col.replace('.csv', '')
    df['ID'] = col
    Files = Files + [df]

feature = 'Close'
Output = pd.DataFrame({})
for file in Files:
    col = file['ID'].iloc[0]
    file = file.set_index('Date')
    temp = file[feature].to_frame()
    temp.columns = [col]
    if temp.index.duplicated().any():
        temp = temp.reset_index().drop_duplicates(subset='Date', keep='first').set_index('Date')
    Output = pd.concat([Output, temp], axis=1)
save = path + 'WorkFile/' + feature + '.csv'
Output = Output.round(2)
Output.to_csv(save, index=True, na_rep='NA')

