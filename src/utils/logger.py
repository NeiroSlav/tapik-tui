def logger(data: str) -> None:
    with open("../log.txt", "a") as log:
        log.write(data + "\n")


logger("\nRESTART\n")
