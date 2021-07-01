from bs4 import BeautifulSoup
import urllib.request as req

page_num = 1
while True:
    code = req.urlopen("https://movie.naver.com/movie/bi/mi/pointWriteFormList.nhn?code=10106&type=after&isActualPointWriteExecute=false&isMileageSubscriptionAlready=false&isMileageSubscriptionReject=false&page={}".format(page_num))
    soup = BeautifulSoup(code, "html.parser")
    comment = soup.select("li > div.score_reple > p > span")
    if len(comment) == 0:
        break
    for i in comment:
        i = i.text.strip()
        if i == "관람객":
            continue
        print(i)
    if page_num == 3:
        break
    page_num += 1