score = int(input("점수 입력 >> "))
if score >= 90:
    print("학점 A")
elif 80 <= score < 90:
    print("학점 B")
elif 70 <= score < 80:
    print("학점 C")
else:
    print("학점 F")