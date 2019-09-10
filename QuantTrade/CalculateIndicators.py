'''
Use the package 'talib' to compute technical indicators
Covered all four types: Trend, Momentum, Volume, Volatility
'''

def Tech_Func(Stock):
    Tech = pd.DataFrame(Stock['ClosingPrice'])

    close= Stock['ClosingPrice'].values
    high= Stock['HighestPrice'].values
    low=Stock['LowestPrice'].values
    volume=Stock['VolumeShares'].values.tolist()
    volume = np.array(volume,dtype=float)

    Tech['Price'] = talib.WCLPRICE(high, low, close)
    Tech['RET'] = Stock['Return']

    # Trend
    Tech['MACD'],Tech['MACDsignal'],Tech['MACDhist']= talib.MACD(close, fastperiod=6, slowperiod=12, signalperiod=9)
    Tech['SAR']= talib.SAR(high, low, acceleration=0, maximum=0)

    # Momentum
    Tech['CCI'] = talib.CCI(high, low, close, timeperiod=14)
    Tech['RSI_fast'] = talib.RSI(close, timeperiod=7)
    Tech['RSI_slow'] = talib.RSI(close, timeperiod=14)
    Tech['ADX'] = talib.ADX(high, low, close, timeperiod=14)
    Tech['+DI'] =talib.PLUS_DI(high, low, close, timeperiod=14)
    Tech['-DI'] =talib.MINUS_DI(high, low, close, timeperiod=14)

    # Volume
    Tech['OBV'] = talib.OBV(close, volume)

    # Volatility
    Tech['ATR'] = talib.ATR(high, low, close, timeperiod=14)
    Tech['BBANDS_upper'], Tech['BBANDS_middle'], Tech['BBANDS_lower'] = talib.BBANDS(close, timeperiod=5, nbdevup=2, nbdevdn=2, matype=0)
    Tech['BBANDS_diff']=Tech['BBANDS_upper'] - Tech['BBANDS_lower']

    return Tech