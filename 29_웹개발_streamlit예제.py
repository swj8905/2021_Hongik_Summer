import streamlit as st

st.text("일반 텍스트 입니다.")
st.text("아무말이나 써보세요.")
st.text("텍스트 함수는 한줄씩 차례대로 기록합니다")
st.text("always rerun 버튼 누르면")
st.text("수정사항이 자동으로 반영됩니다.")

st.write("---")
st.write("이런 것도 됩니다.")
st.write("# 이런 것도 됩니다.")
st.write("## 이런 것도 됩니다.")
st.write("### 이런 것도 됩니다.")
st.write("#### 이런 것도 됩니다.")
st.write("##### 이런 것도 됩니다.")
st.write("###### 이런 것도 됩니다.")
st.write("> 이런 것도 됩니다.")
st.write(">> 이런 것도 됩니다.")
st.write(">>> 이런 것도 됩니다.")
st.write(">>>> 이런 것도 됩니다.")

st.write("https://www.naver.com")

foo = {"짜장면":5000, "짬뽕":5000, "탕수육":10000}
st.write(foo)

st.write("1 + 1 = ", 2)

st.code("print('Hello World')")

"문자열만 이렇게 넣어주면"
"알아서 웹페이지에 띄워줍니다."

"""
# 매직 커맨드

매직 커맨드는 굳이 write()함수를 쓰지 않아도

이렇게 더 직관적으로 코드를 짤 수 있습니다.

----------------------------------

https://www.naver.com

```python
print("Hello World")
```

|         |   수학       |  평가       |
|---------|:-----------:|:------------:|
| 철수    |  90         | 참잘했어요. |
| 영희    |  40         | 분발하세요. |

"""






