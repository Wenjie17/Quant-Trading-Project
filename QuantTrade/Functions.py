'''
Some core functions that identify trends or crossovers
'''

def NarrowOrWide(indicator, thresh):
    # Tracking trends of 'convergence' or 'divergence'
    N = len(indicator)
    n = indicator.isna().sum()
    Check = deepcopy(indicator)
    Check.loc[:] = np.nan
    for t in range(2 + n, N):
        mean = np.mean(indicator.iloc[t - 2:t])
        if indicator.iloc[t] > (1 - thresh) * mean and indicator.iloc[t] < (1 + thresh) * mean:  ## within 5%
            Check.iloc[t] = 0
        elif indicator.iloc[t] < (1 - thresh) * mean:  # Narrow
            Check.iloc[t] = -1
        elif indicator.iloc[t] > (1 + thresh) * mean:  # Wide
            Check.iloc[t] = 1
    return Check


def CrossoverLines(indicator, up, down, thresh):  # e.g. P & BOLL
    N = len(indicator)
    n = up.isna().sum()
    Check = deepcopy(indicator)
    Check.loc[:] = np.nan
    for t in range(n + 1, N):
        if indicator.iloc[t] > (1 - thresh) * up.iloc[t] and indicator.iloc[t - 1] < (1 - thresh) * up.iloc[t - 1]:
            Check.iloc[t] = 1
        elif indicator.iloc[t] < (1 + thresh) * down.iloc[t] and indicator.iloc[t - 1] > (1 + thresh) * down.iloc[
            t - 1]:
            Check.iloc[t] = -1
        else:  # within the middle
            Check.iloc[t] = 0
    return Check