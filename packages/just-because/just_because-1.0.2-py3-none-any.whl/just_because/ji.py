from .patterns import ji_pattern

def ji(string: str) -> str: # pylint: disable = invalid-name
    """
    this function is used to replace ji to 只因.
    """
    return ji_pattern.sub('只因', string)
