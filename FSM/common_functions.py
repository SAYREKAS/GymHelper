def is_number(stroke: str) -> bool:
    try:
        float(stroke.replace(',', '.'))
        return True
    except ValueError:
        return False
