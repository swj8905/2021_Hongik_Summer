import streamlit as st
from selenium import webdriver
import time
import chromedriver_autoinstaller
from konlpy.tag import Okt
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import load_model
import json
import os
import pandas as pd
import altair as alt
import traceback

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

st.write("# 유튜브 댓글 감성 분석")
form = st.form(key="form")
max_num = form.slider('최대 크롤링 개수', 1, 1000, 1)
youtube_link = form.text_input("유튜브 링크 입력")
submit_button = form.form_submit_button(label="크롤링 시작")

if submit_button:

    st.write("감성분석 모델을 불러오는 중입니다. 잠시만 기다려주세요.")
    st.write("----")
    okt = Okt()
    tokenizer = Tokenizer(19417, oov_token = 'OOV')
    with open('wordIndex.json') as json_file:
      word_index = json.load(json_file)
      tokenizer.word_index = word_index

    loaded_model = load_model('best_model.h5')
    def sentiment_predict(new_sentence):
        max_len = 30
        stopwords = ['의','가','이','은','들','는','좀','잘','걍','과','도','를','으로','자','에','와','한','하다']
        new_sentence = okt.morphs(new_sentence, stem=True) # 토큰화
        new_sentence = [word for word in new_sentence if not word in stopwords] # 불용어 제거
        encoded = tokenizer.texts_to_sequences([new_sentence]) # 정수 인코딩
        pad_new = pad_sequences(encoded, maxlen = max_len) # 패딩
        score = float(loaded_model.predict(pad_new)) # 예측
        return score

    def string_to_num(string):
        if "K" in string:
            result = float(string.replace("K", "")) * 1000
        elif "M" in string:
            result = float(string.replace("M", "")) * 10000
        else:
            try:
                result = float(string)
            except:
                result = 0
        return int(result)

    chrome_path = chromedriver_autoinstaller.install()
    opt = webdriver.ChromeOptions()
    opt.add_argument("headless")
    opt.add_argument("window-size=1920,1080")
    browser = webdriver.Chrome(chrome_path, options=opt)
    browser.get(youtube_link)
    time.sleep(5)
    browser.execute_script("scrollBy(0, 1000);")
    time.sleep(4)
    browser.save_screenshot("test.png")

    replies = browser.find_elements_by_css_selector("ytd-comment-thread-renderer.style-scope.ytd-item-section-renderer")
    idx = 0
    df = pd.DataFrame(columns=["score", "like", "reply"])
    sentiment_result = {"매우긍정":0, "긍정":0, "중립":0, "부정":0, "매우부정":0}
    while True:
        try:
            reply = replies[idx]
            user_comment = reply.find_elements_by_css_selector("#content-text")[0].text
            like_num = reply.find_elements_by_css_selector("span#vote-count-middle")[0].text
            try:
                reply_of_reply = int(reply.find_elements_by_css_selector("#text > span.style-scope.yt-formatted-string:nth-child(2)")[0].text)
            except:
                reply_of_reply = 1
            st.write("##### " + user_comment)
            score = sentiment_predict(user_comment)
            like_num = string_to_num(like_num)
            df = df.append({"score":score, "like":like_num, "reply":reply_of_reply}, ignore_index=True)

            if score >= 0.5:
                st.write(f"###### {score * 100:.2f} % 확률로 __긍정__입니다.   ")
            else:
                st.write(f"###### {100 - score * 100:.2f} % 확률로 __부정__입니다.   ")
            st.text("\n")
            if 0.8 <= score <= 1:
                sentiment_result["매우긍정"] += 1
            elif 0.6 <= score < 0.8:
                sentiment_result["긍정"] += 1
            elif 0.4 <= score < 0.6:
                sentiment_result["중립"] += 1
            elif 0.2 <= score < 0.4:
                sentiment_result["부정"] += 1
            elif 0 <= score < 0.2:
                sentiment_result["매우부정"] += 1
        except Exception as e:
            print(traceback.format_exc())
            print("===== 크롤링 완료! =====")
            break
        idx += 1
        if idx == max_num:
            break
        if idx % 20 == 0:
            # browser.find_element_by_css_selector("html").send_keys(Keys.END)
            browser.execute_script(f"scrollBy(0, 4000);")
            time.sleep(4)
            browser.save_screenshot("test.png")
            replies = browser.find_elements_by_css_selector("ytd-comment-thread-renderer.style-scope.ytd-item-section-renderer")
    browser.close()
    result = pd.DataFrame({"감성": sentiment_result.keys(), "댓글 수":sentiment_result.values()})
    "# 감성분석 결과"
    fig = alt.Chart(result).mark_bar().encode(x=alt.X("감성", sort=list(sentiment_result.keys())), y="댓글 수")

    st.altair_chart(fig, use_container_width=True)
    print(df)
    df.to_csv("./test.csv")
    c = alt.Chart(df).mark_circle().encode(x='score', y='like', size=alt.Size('reply', scale=alt.Scale(domain=[1, df["reply"].max()])), color='reply', tooltip=['score', 'like', 'reply'])

    st.altair_chart(c, use_container_width=True)


