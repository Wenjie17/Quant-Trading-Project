
import talib
'''
install package inside Pycharm:
go to File-Settings-Project-Project Interpreter-Select '+', search and install Ta-lib
'''
import pandas as pd
from pandas import read_csv
import numpy as np
import glob
import matplotlib.pyplot as plt
import keras
from copy import deepcopy
#from pandas_ml import ConfusionMatrix
#pd.options.mode.chained_assignment = None  # default='warn'
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from keras.models import Sequential
from keras.layers import Dense
from sklearn import svm
from collections import Counter
import os
import os.path
#Read Data
path = r'/Data/'

from QuantTrade.CalculateIndicators import *
from QuantTrade.EncodeSignals import *
from QuantTrade.Functions import *
from QuantTrade.Predictions import *

# Example
filenames = glob.glob(path + 'HKEQ'+ "/*.csv")
for name in filenames:
  #Read CSV
  Stock= read_csv(name,header=0,index_col = 0)
  Stock = pd.DataFrame(Stock)
  Stock= Stock.dropna()   ## Not include any NA values
  if len(Stock)>0:
  #Call Functions
    Tech = Tech_Func(Stock)
    Check = CheckTech(Tech)
    Signals = Signals_Tech()
    ##Simple
    SimpleSum = deepcopy(Signals)
    SimpleSum['Sum'] = SimpleSum.iloc[:, 2:].sum(axis=1)
    SimpleSum['Sum_Predicted'] = decision(SimpleSum['Sum'])
    #ML
    final = Predict()
    Final = pd.concat([Stock['ClosingPrice'],Signals['Return'],final,SimpleSum['Sum_Predicted']], axis = 1)
    Final = Final.dropna()
    #Save
    save = name.replace('HKEQ','Technical_Indicators_Final')
    Final.to_csv(save,index=True,na_rep='NA')
