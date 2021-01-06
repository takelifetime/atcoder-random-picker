import math

def modrate(raw_rate: float) -> int:
    """
    Simurate rating modification used in AtCoder
    Reference: https://qiita.com/anqooqie/items/92005e337a0d2569bdbd

    Parameters
    ----------
    raw_rate: float
        Rating before modification
    
    Returns
    -------
    mod_rate: float
        Rating after modification
    """

    if raw_rate >= 400:
        return int(raw_rate)
    else:
        return int(400 / math.exp((400 - raw_rate) / 400) + 0.5)