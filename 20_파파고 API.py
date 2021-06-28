import os
import sys
import urllib.request
import json

sentence = input("문장 입력 >> ")
client_id = "qVYQU3MDutURc68w3PPl" # 개발자센터에서 발급받은 Client ID 값
client_secret = "nIcsZuE2Yz" # 개발자센터에서 발급받은 Client Secret 값
encText = urllib.parse.quote(sentence)
data = "source=ko&target=vi&text=" + encText
url = "https://openapi.naver.com/v1/papago/n2mt"
request = urllib.request.Request(url)
request.add_header("X-Naver-Client-Id",client_id)
request.add_header("X-Naver-Client-Secret",client_secret)
response = urllib.request.urlopen(request, data=data.encode("utf-8"))
rescode = response.getcode()
if(rescode==200):
    response_body = response.read()
    result = json.loads(response_body.decode('utf-8'))
    print(result["message"]["result"]["translatedText"])
else:
    print("Error Code:" + rescode)