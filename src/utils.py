def to_num(value: str) -> int | float | None:
    try:
        return int(value)
    except ValueError:
        return float(value)
    except Exception:
        return
