import requests
import json

import streamlit as st
import pandas as pd
import pydeck as pdk
import math
from bs4 import BeautifulSoup
import urllib.request as req

def multipolygon_to_polygon(df):
    temp = pd.DataFrame()
    for idx, i in df.iterrows():
        if i[0] == "MultiPolygon":
            for polygon in i[1]:
                temp = temp.append(pd.DataFrame({"type":"MultiPolygon", "coordinates":[polygon], "CTP_KOR_NM":i[2]}))
        else:
            temp = temp.append(i)
    return temp.reset_index(drop=True)

st.title('코로나 확진자 맵')

# 코로나 정보 표시
code = req.urlopen("https://kosis.kr/covid/covid_index.do")
soup = BeautifulSoup(code, "html.parser")
text = soup.select("li > p.text")
number = soup.select("li > p.number")
increase = soup.select("li > p.increase")

f"""
|   {text[0].text}   |   {text[1].text}   |   {text[2].text}   |   {text[3].text}   |
|:--------:|:--------:|:--------:|:--------:|
|   {number[0].text}   |   {number[1].text}   |   {number[2].text}   |   {number[3].text}   |
|   {increase[0].text}   |   {increase[1].text}   |   {increase[2].text}   |   {increase[3].text}   |
"""


### 시도별 좌표값 데이터 가져오기
df = pd.read_json("./Si_Do_map_utf8.json")
df = multipolygon_to_polygon(df)

### 확진자 데이터 크롤링
send_data = {"statusGubun" : "confirm"}
data = requests.post("https://kosis.kr/covid/covid_getSidoMapData.do", data=send_data)
result = json.loads(data.text)
city_list = []
lat_list = []
lon_list = []
confirm_num_list = []
for i in result["resultSidoData"]:
    city = i["ovL1Kor"]
    if (city == "전체") or (city == "검역"):
        continue
    confirm_num = i["dtvalCo1"]
    df.loc[df["CTP_KOR_NM"]==city, "confirm_num"] = confirm_num


df["순위"] = df["confirm_num"].rank(method="dense", ascending=False)
df["정규화"] = df["순위"] / df["순위"].max()

# print(df["정규화로그"])
df["confirm_num"] = df["confirm_num"] + 1000
# Make layer
layer = pdk.Layer(
    'PolygonLayer', # 사용할 Layer 타입
    df, # 시각화에 쓰일 데이터프레임
    get_polygon='coordinates', # geometry 정보를 담고있는 컬럼 이름
    get_fill_color='[255*(1-정규화), 100*정규화, 255*정규화]', # 각 데이터 별 rgb 또는 rgba 값 (0~255)
    pickable=True, # 지도와 interactive 한 동작 on
    auto_highlight=True, # 마우스 오버(hover) 시 박스 출력
    extruded=True,
    get_elevation="confirm_num",
    elevation_scale = 6
)

# Set the viewport location
center = [127.82352110051013, 35.52673135292517]
view_state = pdk.ViewState(
    longitude=center[0],
    latitude=center[1],
    zoom=5.8,
    pitch=50)

# Render
r = pdk.Deck(map_style="light",
             layers=[layer],
             initial_view_state=view_state,
             tooltip={"html": "도시 : {CTP_KOR_NM}<br/>확진자: {confirm_num}", "style": {"color": "white"}})

st.pydeck_chart(r)
