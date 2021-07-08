import streamlit as st
import pandas as pd
import joblib

# 학습한 모델 불러오기
file = open("./model.pkl", "rb")
model = joblib.load(file)

# 제목
st.write("# 붓꽃 품종 예측")

# 사이드바 만들기
st.sidebar.title("Features")
value1 = st.sidebar.slider(label="Sepal Length (cm)", value=5.2, min_value=0.0, max_value=8.0)
value2 = st.sidebar.slider(label="Sepal Width (cm)", value=3.2, min_value=0.0, max_value=8.0)
value3 = st.sidebar.slider(label="Petal Length (cm)", value=4.2, min_value=0.0, max_value=8.0)
value4 = st.sidebar.slider(label="Petal Width (cm)", value=1.2, min_value=0.0, max_value=8.0)

button_clicked = st.button("붓꽃 품종 예측시키기")
st.write("---")

# 이미지 url 주소
setosa = "https://upload.wikimedia.org/wikipedia/commons/thumb/5/56/Kosaciec_szczecinkowaty_Iris_setosa.jpg/440px-Kosaciec_szczecinkowaty_Iris_setosa.jpg"
versicolor = "https://upload.wikimedia.org/wikipedia/commons/thumb/2/27/Blue_Flag%2C_Ottawa.jpg/440px-Blue_Flag%2C_Ottawa.jpg"
virginica = "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f8/Iris_virginica_2.jpg/440px-Iris_virginica_2.jpg"

if button_clicked == True:
    result = model.predict([
        [value1, value2, value3, value4]
    ])
    if result == 0:
        st.image(setosa)
        st.write("# Setosa")
    elif result == 1:
        st.image(versicolor)
        st.write("# Versicolor")
    elif result == 2:
        st.image(virginica)
        st.write("# Verginica")