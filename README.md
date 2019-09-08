# Quantitative-Trading-Project (Final Year Project)
The whole project contains two part: Pairs trading strategy & Technical Indicators strategy.
Codes presented here are for technical indicators strategy, and are solely developed by myself.

------------------------------------------------------------- CODES -----------------------------------------------------------------
#Codes are shared from google drive as read-only. Please open with Google Colaboratory.

Data Collection: https://drive.google.com/file/d/1xPbpxuwkYiWo_a6HjPM9LOIBxnVc3Kmu/view?usp=sharing

Mock Trading: https://drive.google.com/file/d/1JVJtTXB7KM_iwn5mwwCZiZSLW4Pl7Ypa/view?usp=sharing
- This is a simplified and merged version of mock trading codes. It displayed the core logic of our strategy, which are further explained below.


------------------------------------------------------------- NOTES -----------------------------------------------------------------
*Techinical Indicators: 

To capture trading signals as accurate and comprehensive as possible, a variety of empirical technical indicators with different focuses and purposes have been selected for the compilation of this strategy, as shown below:
- Trend Indicators (MACD, Parabolic SAR) are selected to eliminate the noise of daily volatility
- Momentum Indicators (KDJ, RSI, ICH) are deployed to show the fluctuation of a stock
- Volatility Indicators (BBANDS, Illiquidity, ATR) are used as a protection mechanism against breakout 
- Volume Indicators (OBV, ROC) would provide indication on the strength and direction of price movement.


*Key Steps:

1. Calculation: 
With previous market data, we calculate the result from each individual indicator respectively and from the combination of different indicators. 

2. Encoding: 
The observed range and trends from the above mentioned process then yield us new trading signals indicating long(1), weak long(0.5), hold(0), weak short(-0.5), and short(-1) respectively. 

3. Integration & Prediction: 
The encoded signals are combined together to produce an integrated final signal for our trade under specific strategy. 
Four models are applied: Random Forest, Neural Networks, SVM and Logistic Regressions, while predictions made by logistic regressions are prioritized based on backtesting results.
