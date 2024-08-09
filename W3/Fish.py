#붕어빵 재고
stock = {
    "팥붕어빵" : 10,   
    "슈크림붕어빵" : 8,
    "초코붕어빵" : 5
}
#가격 초기화
prices = {
    "팥붕어빵" : 1000,
    "슈크림붕어빵" : 1200,
    "초코붕어빵" : 1500

}
#당일 판매 개수 초기화
sales = {
    "팥붕어빵" : 0,
    "슈크림붕어빵" : 0,
    "초코붕어빵" : 0
}

while True:
    mode = input("원하는 모드를 선택하세요(주문, 관리자, 종료)") #모드 선택 코드

    if mode == "종료":
        break

    if mode == "관리자":
        while True:
            bread_type = input("추가할 붕어빵 종류를 입력하세요 (팥붕어빵, 슈크리붕어빵, 초코붕어빵) 뒤로가기를 원하시면 '뒤로'를 입력해주세요")
            if bread_type == "뒤로":
                break
            
            additional_stock = int(input(f"{bread_type}의 추가할 개수를 입력하세요")) # 결과는 str -> 숫자 -> int()
            stock[bread_type] += additional_stock # stock[bread_type] = stock[bread_type] + additional_stock
            print(f"{bread_type}이 {additional_stock}개 추가되었습니다.")
            print("현재 붕어빵 재고는 아래와 같습니다.")
            for type, count in stock.items():
                print(f"{type} : {count}") #dict에서 items를 사용하면 키와 벨류 토해냅니다. 자랑하면

    if mode == "주문":
        while True:
            bread_type = input("주문할 붕어빵의 맛을 입력해주세요 (뒤로가기를 원하시면 '뒤로'를 입력해주세요)")
            if bread_type == "뒤로":
                break

            bread_count = int(input("주문할 붕어빵 개수를 입력하세요"))

            if stock[bread_type] >= bread_count:
                stock[bread_type] = stock[bread_type] - bread_count
                sales[bread_type] += bread_count
                print(f"{bread_type} {bread_count}개를 판매했습니다.")
            else:
                print("미안해 그만큼 줄수 있는 붕어빵이 없어")

            print("현재 붕어빵 재고")
            for bread_type, bread_count in stock.items():
                print(f"{bread_type} : {bread_count}")   

print("오늘의 영업을 종료합니다.")
total_sales = sum(sales[bread]*prices[bread] for bread in sales)
print(f"총 매출: {total_sales}원")
