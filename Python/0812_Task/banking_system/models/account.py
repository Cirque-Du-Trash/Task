class Account:
    bank_name: str = "기본 은행명"

    def __init__(self) -> None:
        self.__balance: int = 0
        self.transactions: list = []

    def deposit(self, amount: int) -> None:
        if amount > 0:
            self.__balance += amount
            self.transactions.append(f"입금: {amount}")
        else:
            raise ValueError("입금 금액은 양수여야 합니다.")

    def withdraw(self, amount: int) -> None:
        if amount > 0 and amount <= self.__balance:
            self.__balance -= amount
            self.transactions.append(f"출금: {amount}")
        else:
            raise ValueError("출금 금액은 양수여야 하며, 잔고를 초과할 수 없습니다.")

    def get_balance(self) -> int:
        return self.__balance

    def get_transactions(self) -> list:
        return self.transactions

    @classmethod
    def get_bank_name(cls) -> str:
        return cls.bank_name

    @classmethod
    def set_bank_name(cls, name: str) -> None:
        cls.bank_name = name