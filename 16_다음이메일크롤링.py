from selenium import webdriver
import time
import chromedriver_autoinstaller

chrome_path = chromedriver_autoinstaller.install()
# 크롬 헤드리스 모드
# option = webdriver.ChromeOptions()
# option.add_argument("headless")
# browser = webdriver.Chrome(chrome_path, options=option)
# 크롬 헤드리스 모드 X
browser = webdriver.Chrome(chrome_path)
browser.get("https://logins.daum.net/accounts/signinform.do?url=https%3A%2F%2Fwww.daum.net%2F")

# 아이디 입력
id = browser.find_element_by_css_selector("input#id")
id.send_keys("talingpython")
# 비밀번호 입력
pw = browser.find_element_by_css_selector("input#inputPwd")
pw.send_keys("q1w2e3!@#")
# 로그인 버튼 클릭
button = browser.find_element_by_css_selector("button#loginBtn")
button.click()
time.sleep(3)

# 이메일 함으로 이동
browser.get("https://mail.daum.net/")
time.sleep(2)

# 이메일 제목 크롤링
title = browser.find_elements_by_css_selector("strong.tit_subject")
for i in title:
    print(i.text)
browser.close()