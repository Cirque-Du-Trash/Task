from typing import Callable, Any

def validate_transaction(func: Callable) -> Callable:
    def wrapper(amount: int, *args: Any, **kwargs: Any) -> Any:
        if amount <= 0:
            raise ValueError("금액은 0보다 커야 합니다.")
        return func(amount, *args, **kwargs)
    return wrapper