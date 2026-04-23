def istype(allRows: list, rowID: int, colID: int, colValue: str, options: list):
    typeMap = {
        "int": int,
        "integer": int,

        "float": float,
        "double": float,
        "decimal": float,
        "number": float,

        "str": str,
        "string": str,
        "text": str,

        "bool": None,
        "boolean": None
    }

    for opt in options:
        opt = opt.lower().strip()

        if opt in {"bool", "boolean"}:
            if str(colValue).lower() in {"true", "false", "1", "0"}:
                return True
            continue

        caster = typeMap.get(opt)
        if caster is None:
            continue  # unknown type

        try:
            caster(colValue)
            return True
        except (ValueError, TypeError):
            continue

    return False