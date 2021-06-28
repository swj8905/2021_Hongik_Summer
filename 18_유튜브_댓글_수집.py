from selenium import webdriver
import time
import chromedriver_autoinstaller
from selenium.webdriver.common.keys import Keys

chrome_path = chromedriver_autoinstaller.install()
browser = webdriver.Chrome(chrome_path)
browser.get("https://www.youtube.com/watch?v=ToG7tNAAfWk")
time.sleep(4)

# 스크롤 한번만 살짝 내리기
browser.find_element_by_css_selector("html").send_keys(Keys.PAGE_DOWN) # 스크롤 끝까지 내리고 싶으면 --> Keys.END
time.sleep(3)
# 댓글 수집
comments = browser.find_elements_by_css_selector("#content-text")
idx = 0
while True:
    print(comments[idx].text)
    idx += 1
    if idx % 20 == 0:
        browser.find_element_by_css_selector("html").send_keys(Keys.END)
        time.sleep(3)
        comments = browser.find_elements_by_css_selector("#content-text")