from banking_system.models.user import User
from banking_system.utils.exceptions import UserNotFoundError

class BankingService:
    def __init__(self) -> None:
        self.users: list[User] = []

    def add_user(self, username: str) -> None:
        user = User(username)
        self.users.append(user)

    def find_user(self, username: str) -> User:
        for user in self.users:
            if user.username == username:
                return user
        raise UserNotFoundError(username)

    def user_menu(self, username: str) -> None:
        user = self.find_user(username)
        while True:
            print(f"\n사용자: {user.username}")
            print("1. 입금")
            print("2. 출금")
            print("3. 잔고 확인")
            print("4. 거래 내역 확인")
            print("5. 종료")
            choice = input("원하는 작업을 선택하세요: ")

            if choice == '1':
                amount = int(input("입금할 금액을 입력하세요: "))
                user.account.deposit(amount)
            elif choice == '2':
                amount = int(input("출금할 금액을 입력하세요: "))
                user.account.withdraw(amount)
            elif choice == '3':
                balance = user.account.get_balance()
                print(f"현재 잔고: {balance}원")
            elif choice == '4':
                transactions = user.account.get_transactions()
                print("거래 내역:")
                for transaction in transactions:
                    print(transaction)
            elif choice == '5':
                break
            else:
                print("잘못된 선택입니다. 다시 시도하세요.")