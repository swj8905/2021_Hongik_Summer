from bs4 import BeautifulSoup
import urllib.request as req

code = req.urlopen("https://finance.naver.com/marketindex/")
soup = BeautifulSoup(code, "html.parser")
price = soup.select("ul#exchangeList span.value")
for i in price:
    print(i.string)