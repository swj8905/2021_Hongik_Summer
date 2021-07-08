import yfinance as yf
import datetime
import streamlit as st
import plotly.graph_objects as go

st.write("# 주식 데이터 시각화")

ticker = st.text_input("티커 입력")
# ticker = "GOOGL"
data = yf.Ticker(ticker)
today = datetime.datetime.today().strftime("%Y-%m-%d")
df = data.history(period="1d", start="2015-1-1", end=today)

st.dataframe(df)

st.write("## 주가 - 종가 기준")
st.line_chart(df["Close"])

st.write("## 주가 - 캔들 차트")
data = go.Candlestick(x=df.index, open=df["Open"], close=df["Close"],
               high=df["High"], low=df["Low"])
fig = go.Figure(data=[data])
st.plotly_chart(fig)

st.write("## 주가 - 거래량")
st.bar_chart(df["Volume"])