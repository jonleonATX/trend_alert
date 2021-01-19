This module is not intended as advice to trade, it is for use in your trading analyses and algorithms. Use at your own risk.

This screener uses Donchian Channels, Average True Range, and other inputs to determine if a stock, future or other financial instrument with timeseries (OHLC) may breakout out of its defined channel.

**Required data:**

-Pandas dataframe containing index as datetime and columns (High, Low, Open, Close) as float
-Define the number of breakout periods (default: 55 periods)
-Average True Range (ATR) window (default: 14 periods)
-ATR multiple (default: 1.5)- sensitivy used to determine a level at which the alert will provide a positive signal

**Response:**

The response returned is a tuple of the signal and a plotly chart: (signal, chart) create_chart=False is default. The signal is one of three options: 1, -1, 0

  * 1 - Possible breakout to go long
  * -1 - Possible breakout to go short
  * 0 - Too far from either price channel

**Dependencies:**

- pandas
- ta
- plotly

**Install module:**

https://pypi.org/project/trendalert/

**Detailed documentation:**

https://github.com/jonleonATX/donchian_trend_alert/blob/master/trendalert.ipynb
