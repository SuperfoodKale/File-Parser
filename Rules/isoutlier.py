def isoutlier(allRows: list, rowID: int, colID: int, colValue: str, options: list):
    try:
        value = float(colValue)
    except (ValueError, TypeError):
        return False

    numeric_vals = []
    for row in allRows:
        try:
            numeric_vals.append(float(row[colID]))
        except (ValueError, TypeError):
            continue

    if len(numeric_vals) < 4:
        return False

    numeric_vals.sort()
    n = len(numeric_vals)
    q1 = numeric_vals[n // 4]
    q3 = numeric_vals[(3 * n) // 4]
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr

    is_outlier = value < lower or value > upper
    expected = options[0].strip().lower() == "true" if options else True
    return is_outlier == expected
