def hasexact(allRows: list,rowID: int, colID: int, colValue: str, options: list):
    for option in options:
        if str(option) == str(colValue.strip()): #exact match to one of the posibilities, includes case sensitivity 
            return True 
    return False