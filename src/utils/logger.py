def logger(data: str) -> None:
    with open("log.txt", "a") as log:
        log.write(data + "\n")


with open("log.txt", "w") as log:
    log.write("")

logger("\nRESTART\n")
