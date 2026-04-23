def has(allRows: list,rowID: int, colID: int, colValue: str, options: list):
    for option in options:
        if option.lower() in colValue.lower(): #does not need exact match therefore .lower() 
            return True 
    return False