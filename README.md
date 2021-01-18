This is screener that uses donchian channels, Average True Range, and other inputs to determine if a stock, future or other financial instrument with timeseries (OHLC) is may breakout out of its defined channel.

This is not advice to trade, it is only information to use at your own risk.

Required data:
- Time series in pandas dataframe (columns need to be titled like: High, Low, Open, Close)
- Define the number of periods (default: 55 periods)
- Average True Range (ATR) window(default: 14 periods)
- ATR multiple (default: 1.5)- used to determine how far from breakout price before positive screen

The response returned is a tuple of the alert and plot. Plot can be set to false if chart is not desired. The alert is one of three options: 1, -1, 0
*  1 - Possbile breakout to go long
* -1 - Possible breakuot to go short
*  0 - Too far from either price channel

Dependencies:
- pandas
- ta
- plotly

Output is a tuple of the alert and plot. Plot can be set to false if chart is not desired.
