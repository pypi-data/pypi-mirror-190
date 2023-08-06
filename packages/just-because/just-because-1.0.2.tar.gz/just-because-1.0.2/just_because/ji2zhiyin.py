from .patterns import ji_pattern

def ji2zhiyin(string: str) -> str:
    """
    this function is used to replace ji to 只因.
    """
    return ji_pattern.sub('只因', string)
