class InsufficientFundsError(Exception):
    def __init__(self, balance: int) -> None:
        super().__init__(f"잔고 부족: 현재 잔고는 {balance}원입니다.")
        self.balance = balance

class NegativeAmountError(Exception):
    def __init__(self) -> None:
        super().__init__("금액은 0보다 커야 합니다.")

class UserNotFoundError(Exception):
    def __init__(self, username: str) -> None:
        super().__init__(f"사용자를 찾을 수 없습니다: {username}")
        self.username = username