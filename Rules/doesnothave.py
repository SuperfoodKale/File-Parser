def doesnothave(allRows: list, rowID: int, colID: int, colValue: str, options: list):
    for option in options:
        if option.lower() in colValue.lower():  # partial match, like Has but inverted
            return False
    return True
