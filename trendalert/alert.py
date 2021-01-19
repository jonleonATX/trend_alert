import ta
import plotly.graph_objects as go
import pandas as pd

class breakout_screen():
    ''' using donchian channels to alert when market may breakout '''
    def __init__(self):
        self.last_don_lband = None
        self.last_don_hband = None
        self.last_open = None
        self.last_high = None
        self.last_low = None
        self.last_close = None
        self.last_tradingDay = None
        self.last_atr = None
        self.don_hband = None
        self.don_lband = None
        self.delta_from_high = None
        self.delta_from_low = None
        self.atr_multiple_high = None
        self.atr_multiple_low = None
        self.atr = None
        self.atrmh = None
        self.atrml = None

    def roundto(self, number, base, places):
        """rounding numbers based on tick characteristics"""
        return round(base*round(number/base), places)

    def breaking_out(self, df, symbol, atr_window=14, breakout_periods=55, atrmultiple_test=1.5, create_chart=False):
        ''' identify potential upcoming breakout to the high or low side '''
        indicator_atr = ta.volatility.AverageTrueRange(df['High'], df['Low'], df['Close'], window=atr_window, fillna=False)
        self.atr = indicator_atr.average_true_range()

        # get last atr
        self.last_atr = self.roundto(self.atr[-1], 0.0000001, 7)

        # calculate the donchian channels
        indicator_don = ta.volatility.DonchianChannel(df['High'], df['Low'], df['Close'], window=breakout_periods, offset=0, fillna=False)
        self.don_hband = indicator_don.donchian_channel_hband()
        self.don_lband = indicator_don.donchian_channel_lband()

        # get the most recent values
        self.last_don_lband = self.don_lband[-1]
        self.last_don_hband = self.don_hband[-1]
        self.last_high = df["High"][-1]
        self.last_open = df["Open"][-1]
        self.last_low = df["Low"][-1]
        self.last_close = df["Close"][-1]
        self.last_tradingDay = df.index[-1]

        # This is a screening routine that notifies if it's within the atr_multiple specified
        # calculate atr multiples
        self.delta_from_high = self.last_don_hband - self.last_high
        self.delta_from_low = self.last_low - self.last_don_lband
        self.atr_multiple_high = self.roundto(self.delta_from_high / self.last_atr, 0.00001, 5)
        self.atr_multiple_low = self.roundto(self.delta_from_low / self.last_atr, 0.00001, 5)
        atr_test_delta = atrmultiple_test * self.last_atr
        self.atrmh = self.last_don_hband - atr_test_delta
        self.atrml = self.last_don_lband + atr_test_delta

        if create_chart:
            chart = self.get_plot(df, symbol, self.don_hband, self.don_lband, self.atrmh, self.atrml)
        else:
            chart = None

        if 0 <= self.atr_multiple_high <= atrmultiple_test:
            return 1, chart
        elif 0 <= self.atr_multiple_low <= atrmultiple_test:
            return -1, chart
        else:
            return 0, chart

    def get_plot(self, dfp, symbol, hband, lband, atrmh, atrml):
        ''' plotly candlestick chart '''
        fig = go.Figure()
        trace1=go.Candlestick(x=dfp.index, open=dfp['Open'], high=dfp['High'], low=dfp['Low'], close=dfp['Close'], name=symbol)
        trace2 = go.Scatter(x=hband.index, y=hband.values, mode='lines', line_color='blue', name='high band')
        trace3 = go.Scatter(x=lband.index, y=lband.values, mode='lines', line_color='blue', name='low band')
        trace4 = go.Scatter(x=pd.Series(dfp.index[-1]), y=[atrmh], name='long_alert_value', mode='markers+text', marker_size=10,
                            marker_color='black', marker_symbol='triangle-up', text=['alert_threshold'], textposition='middle right')
        trace5 = go.Scatter(x=pd.Series(dfp.index[-1]), y=[atrml], name='short_alert_value', mode='markers+text', marker_size=10,
                            marker_color='black', marker_symbol='triangle-down', text=['alert_threshold'], textposition='middle right')
        fig.add_trace(trace1)
        fig.add_trace(trace2)
        fig.add_trace(trace3)
        fig.add_trace(trace4)
        fig.add_trace(trace5)

        fig.update(layout_xaxis_rangeslider_visible=False)
        fig.update_layout(
        title='Breakout Analysis: ' + symbol,
        xaxis_title="Date",
        yaxis_title="Price")
        return fig
