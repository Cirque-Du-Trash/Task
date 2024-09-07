from banking_system.services.banking_service import BankingService
from banking_system.utils.exceptions import UserNotFoundError

def main() -> None:
    banking_service = BankingService()

    while True:
        print("\n1. 사용자 추가")
        print("2. 사용자 찾기")
        print("3. 종료")
        choice = input("원하는 작업을 선택하세요: ")

        if choice == '1':
            username = input("추가할 사용자 이름을 입력하세요: ")
            banking_service.add_user(username)
            print(f"사용자 {username}가 추가되었습니다.")
        elif choice == '2':
            username = input("찾을 사용자 이름을 입력하세요: ")
            try:
                banking_service.user_menu(username)
            except UserNotFoundError as e:
                print(e)
        elif choice == '3':
            print("프로그램을 종료합니다.")
            break
        else:
            print("잘못된 선택입니다. 다시 시도하세요.")

if __name__ == "__main__":
    main()