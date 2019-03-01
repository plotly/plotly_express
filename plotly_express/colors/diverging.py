from .colorbrewer import (  # noqa: F401
    BrBG,
    PRGn,
    PiYG,
    PuOr,
    RdBu,
    RdGy,
    RdYlBu,
    RdYlGn,
    Spectral,
)
from .cmocean import balance, delta, curl  # noqa: F401
from .carto import Armyrose, Fall, Geyser, Temps, Tealrose, Tropic, Earth  # noqa: F401


from ._swatches import _swatches


def swatches():
    return _swatches(__name__, globals())
