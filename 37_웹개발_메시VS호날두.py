import streamlit as st
import pandas as pd
import bokeh
from plots import * # 얘는 설치하는게 아니라 plots.py를 수업자료에서 다운받아주세요.
import json
from bokeh.io import show



messi_df = pd.read_csv("./messi.csv")
ronaldo_df = pd.read_csv("./ronaldo.csv")
foot_df = st.sidebar.radio("발 선택", ["왼발 또는 오른발", "왼발", "오른발"])
st.sidebar.write("# 요약")
#### 요약
if foot_df == "왼발 또는 오른발":
    messi_result_df = messi_df
    ronaldo_result_df = ronaldo_df
elif foot_df == "왼발":
    messi_result_df = messi_df[messi_df["left_foot"]==True]
    ronaldo_result_df = ronaldo_df[ronaldo_df["left_foot"] == True]
elif foot_df == "오른발":
    messi_result_df = messi_df[messi_df["right_foot"]==True]
    ronaldo_result_df = ronaldo_df[ronaldo_df["right_foot"] == True]

result_df = pd.DataFrame({"메시":[
    len(messi_result_df[messi_result_df["goal"]==True]),
    len(messi_result_df[messi_result_df["assist"]==True]),
    len(messi_result_df[messi_result_df["eventName"]=="Shot"]),
    len(messi_result_df[messi_result_df["eventName"]=="Free Kick"]),
    len(messi_result_df[messi_result_df["eventName"] == "Pass"]),
],
"호날두":[
    len(ronaldo_result_df[ronaldo_result_df["goal"]==True]),
    len(ronaldo_result_df[ronaldo_result_df["assist"]==True]),
    len(ronaldo_result_df[ronaldo_result_df["eventName"]=="Shot"]),
    len(ronaldo_result_df[ronaldo_result_df["eventName"]=="Free Kick"]),
    len(ronaldo_result_df[ronaldo_result_df["eventName"] == "Pass"]),
]}, index=["골", "어시스트", "슈팅", "프리킥", "패스"])
st.sidebar.table(result_df)


### 그래프 ####
def plot_panel(event_name):
    if (event_name == "goal") or (event_name == "assist"):
        messi = messi_result_df[messi_result_df[event_name] == True]['positions']
        ronaldo = ronaldo_result_df[ronaldo_result_df[event_name] == True]['positions']
    else:
        messi = messi_result_df[messi_result_df["eventName"] == event_name]['positions']
        ronaldo = ronaldo_result_df[ronaldo_result_df["eventName"] == event_name]['positions']
    p_messi = plot_events(messi, event_name, 'red')
    p_ronaldo = plot_events(ronaldo, event_name, 'blue')
    # grid = bokeh.layouts.column(p_messi, p_ronaldo, sizing_mode="stretch_both")
    grid = bokeh.layouts.grid(
        children=[
            [p_messi, p_ronaldo]
        ],
        sizing_mode="stretch_width",
    )
    return bokeh.models.Panel(child=grid, title=event_name)

tabs = bokeh.models.Tabs(
    tabs=[
        plot_panel("goal"),
        plot_panel("assist"),
        plot_panel("Shot"),
        plot_panel("Free Kick"),
        plot_panel("Pass"),
    ]
)
st.image("https://www.foottheball.com/wp-content/uploads/2018/01/messi-ronaldo-3.jpg")
st.bokeh_chart(tabs)