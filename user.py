class User:
    counter = 0

    def __init__(self, name: str) -> None:
        User.counter += 1
        self.name = name

    def __del__(self) -> None:
        User.counter -= 1
