from typing import Any


def logger(*data: Any) -> None:
    with open("log.txt", "a") as log:
        log.write(str(data) + "\n")


with open("log.txt", "w") as log:
    log.write("")
