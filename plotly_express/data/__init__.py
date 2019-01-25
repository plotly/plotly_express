def gapminder():
    return _get_dataset("gapminder")


def tips():
    return _get_dataset("tips")


def iris():
    return _get_dataset("iris")


def wind():
    return _get_dataset("wind")


def election():
    return _get_dataset("election")


def carshare():
    return _get_dataset("carshare")


def _get_dataset(d):
    import pandas
    import os

    return pandas.read_csv(os.path.join(os.path.dirname(__file__), d + ".csv.xz"))
