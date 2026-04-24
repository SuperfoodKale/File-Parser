def isempty(allRows: list, rowID: int, colID: int, colValue: str, options: list):
    expected = options[0].strip().lower() == "true" if options else True
    is_empty = colValue is None or str(colValue).strip() == "" or str(colValue).strip().lower() == "null"
    return is_empty == expected
