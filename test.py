list = []
numOfData = 0

##### 이런 것도 하나의 함수로 만들어 놓으면 조금이라도 코드의 가독성을 높이는 효과가 있습니다.
def showMenu():
    print("—————————" + "\n" + f"현재 {len(list)}개의 데이터가 있습니다." + "\n" + "—————————")
    print('''1. 전화번호 추가
    2. 전화번호 검색
    3. 전화번호 삭제
    4. 전화번호 전체 출력
    5. 종료
    ------------------''')

def showMsg():
    print("프로그램을 종료합니다.")
###################

def insertData():
    name = input("이름을 입력하세요. >>> ")
    num = input("전화번호를 입력하세요. >>> ")
    list.append({"name": name, "number": num})
    print("===전화번호 추가가 완료되었습니다.===")


def searchData():
    while True:
        search = input("검색할 이름, 혹은 전화번호를 입력하세요 >>> ")
        for i in list:
            if search == i['name'] or search == i['number']:
                print(f"이름 : {i['name']}, 전화번호 : {i['number']}") # search에 성공하자마자 바로 그냥 화면에 출력합니다.
                return  # 기존에는 searchResult 변수를 활용해주셨지만, 다른 방법도 알려드립니다. 이렇게 return을 쓰게 되면 바로 "현재 들어와있는 함수"를 탈출하게 됩니다.
        print("찾는 이름이 없습니다.") # 따라서 위 return 때문에 search에 성공하지 못했을 때만 인터프리터가 이 line에 오게 되어, 그냥 별 조건문 없이 여기다가 "찾는 이름이 없다.'라고 메시지 출력하도록 적어놓으면 됩니다.



def removeData():
    while True:
        deleteSearch = input("삭제할 이름을 입력하세요. >>> ")
        for i in list:
            if deleteSearch == i['name']:
                list.remove(i)
                print("삭제 되었습니다.")
                return
        print("찾는 이름이 없습니다.")


def showAllData():
    for i in list:
        print(f"이름 : {i['name']}, 전화번호 : {i['number']}")


while True:
    showMenu()
    ans = input("원하시는 메뉴를 선택해주세요." + "\n")

    if not ans.isdigit(): # 혹시 실수로 문자를 입력했을 경우를 위한 처리입니다.
        print("숫자를 입력해주세요!")
        continue

    if ans == "1":
        insertData()
    elif ans == "2": # 여기서는 elif 를 써주시는 것이 좋습니다. 기존에 해주셨던 것처럼 전부 if로 해도 결국 실행결과는 똑같지만, if ~ elif ~ elif ~ else 이렇게 해주어야 코드의 가독성이 더 높아집니다.
        searchData()
    elif ans == "3":
        removeData()
    elif ans == "4":
        showAllData()
    elif ans == "5":
        showMsg()
        break
    else:
        print("올바른 선택이 아닙니다.")