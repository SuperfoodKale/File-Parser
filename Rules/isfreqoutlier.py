def isfreqoutlier(allRows: list, rowID: int, colID: int, colValue: str, options: list):
    counts = {}
    for row in allRows:
        val = str(row[colID]).strip()
        counts[val] = counts.get(val, 0) + 1

    freq_vals = sorted(counts.values())
    n = len(freq_vals)
    if n < 4:
        return False

    q1 = freq_vals[n // 4]
    q3 = freq_vals[(3 * n) // 4]
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr

    val_freq = counts.get(str(colValue).strip(), 0)
    is_outlier = val_freq < lower or val_freq > upper
    expected = options[0].strip().lower() == "true" if options else True
    return is_outlier == expected
