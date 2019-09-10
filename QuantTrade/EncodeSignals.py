'''
Encode technical indicators based on their financial implications
'''

def Check_RSI(indicator):
    N = len(indicator)
    n = indicator.isna().sum()
    Check = deepcopy(indicator)
    Check.loc[:] = np.nan
    for t in range(n, N):
        if indicator.iloc[t] >= 70:
            Check.iloc[t] = 1
        elif indicator.iloc[t] <= 30:
            Check.iloc[t] = -1
        elif indicator.iloc[t] > 50 and indicator.iloc[t] < 70:
            Check.iloc[t] = 0.5
        elif indicator.iloc[t] > 30 and indicator.iloc[t] <= 50:
            Check.iloc[t] = -0.5
    return Check


def CheckTech(Tech):
    #Interpret the values of those techinical indicators and encode them into long/hold/short signals

    Check = pd.DataFrame(Stock['Return'])
    Check['BBANDS_diff'] = NarrowOrWide(Tech['BBANDS_diff'], 0.05)
    Check['BBANDS_up'] = NarrowOrWide(Tech['BBANDS_upper'], 0.05)
    Check['BBANDS_lower'] = NarrowOrWide(Tech['BBANDS_lower'], 0.05)

    Check['Price_Boll'] = CrossoverLines(Tech['ClosingPrice'], Tech['BBANDS_upper'], Tech['BBANDS_lower'], 0.03)

    Check['RSI_fast'] = Check_RSI(Tech['RSI_fast'])
    Check['RSI_slow'] = Check_RSI(Tech['RSI_slow'])
    return Check


def RET(indicator):
    N = len(indicator)
    n = indicator.isna().sum()
    Check = deepcopy(indicator)
    Check.loc[:] = np.nan
    for t in range(n, N):
        if indicator.iloc[t] >= 0.5:
            Check.iloc[t] = 1
        elif indicator.iloc[t] < -0.5:
            Check.iloc[t] = -1
        else:
            Check.iloc[t] = 0
        '''
        if indicator.iloc[t]>0.5 and indicator.iloc[t]<3:
          Check.iloc[t] = 0.5
        if indicator.iloc[t]>= -0.5 and indicator.iloc[t]<=0.5 :
          Check.iloc[t] = 0
        if indicator.iloc[t]>-3 and indicator.iloc[t]<-0.5:
          Check.iloc[t] = -0.5
        '''
    return Check


def combine1(df):
    #Trading strategy with Bollinger bands and RSI
    df = df.dropna()
    N = len(df)
    signal = deepcopy(df['Return'])
    signal.loc[:] = np.nan
    for t in range(0, N):
        ##Scenario 1
        if df['BBANDS_diff'].iloc[t] == 0:  # and df['BBANDS_up'].iloc[t]==0 and df['BBANDS_lower'].iloc[t]==0:
            if df['Price_Boll'].iloc[t] == 1:
                signal.iloc[t] = -1  # short
            elif df['Price_Boll'].iloc[t] == -1:
                signal.iloc[t] = 1  # long
            else:
                signal.iloc[t] = 0
        ##Scenario 2
        elif df['BBANDS_diff'].iloc[t] == -1:
            if df['RSI_fast'].iloc[t] == 1:  # and df['RSI_slow'].iloc[t]==1:
                signal.iloc[t] = -1
            elif df['RSI_fast'].iloc[t] == -1:  # and df['RSI_slow'].iloc[t]==-1:
                signal.iloc[t] = 1
            else:
                signal.iloc[t] = 0
        ##Scenario 3
        elif df['BBANDS_diff'].iloc[t] == 1:
            if df['RSI_fast'].iloc[t] == 0.5 and df['RSI_slow'].iloc[t] == 0.5:
                signal.iloc[t] = 1
            elif df['RSI_fast'].iloc[t] == -0.5 and df['RSI_slow'].iloc[t] == -0.5:
                signal.iloc[t] = -1
            else:
                signal.iloc[t] = 0
    return signal


def Check_MACD(DIFF, DEA, HIST):
    # macd（diff），macdsignal（dea），macdhist（macd）
    # Long if DIFF>0 and DEA>0； Long if MACDHIST changes from negative to positive
    N = len(DIFF)
    n = DIFF.isna().sum()
    Check = deepcopy(DIFF)
    Check.loc[:] = np.nan
    for t in range(n, N):
        if DIFF.iloc[t] > 0 and DEA.iloc[t] > 0 and HIST.iloc[t] > 0:
            Check.iloc[t] = 1
        elif DIFF.iloc[t] < 0 and DEA.iloc[t] < 0 and HIST.iloc[t] < 0:
            Check.iloc[t] = -1
        else:
            Check.iloc[t] = 0
    return Check


def Trend(indicator, period):
    N = len(indicator)
    n = indicator.isna().sum()
    Check = deepcopy(indicator)
    Check.loc[:] = np.nan
    for t in range(period + n, N):
        mean = np.mean(indicator.iloc[t - period:t])
        if indicator.iloc[t] > mean:  # Up
            Check.iloc[t] = 1
        elif indicator.iloc[t] < mean:  # Down
            Check.iloc[t] = -1
        elif indicator.iloc[t] == mean:  # Same
            Check.iloc[t] = 0
    return Check


def ADX(indicator):
    N = len(indicator)
    n = indicator.isna().sum()
    Check = deepcopy(indicator)
    Check.loc[:] = np.nan
    P_trend = Trend(Tech['Price'], 2)
    for t in range(n, N):
        if indicator.iloc[t] >= 30:
            if indicator.iloc[t] > Tech['+DI'].iloc[t] + 15 and Tech['ADX'].iloc[t] > Tech['-DI'].iloc[
                t] + 15:  # ADX>>DI“过多”, oversell/overpurchase, not preferred
                Check.iloc[t] = 0
            else:
                Check.iloc[t] = 1 * P_trend.iloc[t]

        else:
            Check.iloc[t] = 0
    return Check


def OBV(indicator):
    N = len(indicator)
    n = indicator.isna().sum()
    Check = deepcopy(indicator)
    Check.loc[:] = np.nan
    P_trend = Trend(Tech['Price'], 2)
    OBV_trend = Trend(indicator, 2)
    for t in range(n, N):
        if P_trend.iloc[t] == 0:
            if OBV_trend.iloc[t] > 0:
                Check.iloc[t] = 1
            elif OBV_trend.iloc[t] < 0:
                Check.iloc[t] = -1
            else:
                Check.iloc[t] = 0

        elif P_trend.iloc[t] == 1:
            if OBV_trend.iloc[t] <= 0:
                Check.iloc[t] = -0.5
            else:
                Check.iloc[t] = 0

        elif P_trend.iloc[t] == -1:
            if OBV_trend.iloc[t] >= 0:
                Check.iloc[t] = 0.5
            else:
                Check.iloc[t] = 0
    return Check


def CCI(indicator, up, down):
    N = len(indicator)
    n = indicator.isna().sum()
    Check = deepcopy(indicator)
    Check.loc[:] = np.nan
    for t in range(1 + n, N):
        if indicator.iloc[t] > up and indicator.iloc[t - 1] < up:  ## 向上突破up
            Check.iloc[t] = 1
        elif indicator.iloc[t] < up and indicator.iloc[t - 1] > up:  ## 向下突破up
            Check.iloc[t] = -1
        elif indicator.iloc[t] > down and indicator.iloc[t - 1] < down:  ## 向上突破down
            Check.iloc[t] = 0.5
        elif indicator.iloc[t] < down and indicator.iloc[t - 1] > down:  ## 向下突破down
            Check.iloc[t] = -0.5
        else:  # within the middle
            Check.iloc[t] = 0
    return Check


def Signals_Tech():
    Signals = pd.DataFrame(Stock['Return'])
    Signals['Ret'] = RET(Signals['Return'])
    signal = combine1(Check).to_frame()
    signal.columns = ['BOLL+RSI+CCI']
    Signals = pd.concat([Signals, signal], axis=1)

    Signals['RSI_Cross'] = CrossoverLines(Tech['RSI_fast'], Tech['RSI_slow'], Tech['RSI_slow'], 0)
    Signals['MACD_LS'] = Check_MACD(Tech['MACD'], Tech['MACDsignal'], Tech['MACDhist'])
    Signals['MACD_Cross'] = CrossoverLines(Tech['MACD'], Tech['MACDsignal'], Tech['MACDsignal'], 0)
    Signals['ADX'] = ADX(Tech['ADX'])
    Signals['OBV'] = OBV(Tech['OBV'])
    Signals['CCI'] = CCI(Tech['CCI'], 100, -100)
    Signals = Signals.dropna()
    return Signals
