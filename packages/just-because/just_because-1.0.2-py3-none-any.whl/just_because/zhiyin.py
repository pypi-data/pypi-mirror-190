from .patterns import zhiyin_pattern

def zhiyin(string: str) -> str:
    """
    this function is used to replace zhiyin to 鸡.
    """
    return zhiyin_pattern.sub('鸡', string)
