from konlpy.tag import Okt

okt = Okt()
result = okt.nouns("저는 형태소 분석기를 사용 중입니다.")
print(result)