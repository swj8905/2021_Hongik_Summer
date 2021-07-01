from bs4 import BeautifulSoup
import urllib.request as req
import urllib.parse as par

keyword = input("키워드 입력 >> ")
encoded = par.quote(keyword) # 한글 -> 특수한 문자

page_num = 1
while True:
    url = "https://news.joins.com/Search/JoongangNews?page={}&Keyword={}&SortType=New&SearchCategoryType=JoongangNews".format(page_num, encoded)
    code = req.urlopen(url)
    soup = BeautifulSoup(code, "html.parser")
    title = soup.select("h2.headline.mg > a")
    if len(title) == 0: # 끝 페이지까지 크롤링 완료했으면?
        break
    for i in title:
        print("제목 :", i.text)
        print("링크 :", i.attrs["href"])
        print()
        code_news = req.urlopen(i.attrs["href"])
        soup_news = BeautifulSoup(code_news, "html.parser")
        content = soup_news.select_one("div#article_body")
        print(content.text.strip().replace("     ", " ").replace("   ", ""))

    if page_num == 1:
        break
    page_num += 1