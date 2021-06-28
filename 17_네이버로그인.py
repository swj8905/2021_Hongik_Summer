# 네이버 셀레니움 로그인
from selenium import webdriver
import pyperclip    # pip install pyperclip 입력하여 모듈 설치!
from selenium.webdriver import ActionChains
import time
from selenium.webdriver.common.keys import Keys
import chromedriver_autoinstaller # 터미널 창에 pip install chromedriver_autoinstaller 입력하여 모듈 설치!

def input_id_pw(browser, css, user_input):
    pyperclip.copy(user_input)  # input을 클립보드로 복사
    browser.find_element_by_css_selector(css).click()  # element focus 설정
    # ActionChains(browser).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()  # 윈도우 : Ctrl+V 전달
    ActionChains(browser).key_down(Keys.LEFT_SHIFT).key_down(Keys.INSERT).key_up(Keys.LEFT_SHIFT).key_up(Keys.INSERT).perform()  # 맥 : shift+insert 전달
    time.sleep(1)

chrome_path = chromedriver_autoinstaller.install() # 추가
browser = webdriver.Chrome(chrome_path) # 추가

browser.get("https://nid.naver.com/nidlogin.login")

input_id_pw(browser, "#id", "본인 아이디 입력해주세요.")
time.sleep(1)
input_id_pw(browser, "#pw", "본인 비밀번호 입력해주세요.")
time.sleep(1)

browser.find_element_by_css_selector("#frmNIDLogin > fieldset > input").click()
time.sleep(3)
