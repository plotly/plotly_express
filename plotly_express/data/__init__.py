"""
Built-in datasets for demonstration, educational and test purposes.
"""


def gapminder():
    """
    Each row represents a country on a given year.

    https://www.gapminder.org/data/

    Returns:
        A `pandas.DataFrame`.
    """
    return _get_dataset("gapminder")


def tips():
    """
    Each row represents a restaurant bill.

    https://vincentarelbundock.github.io/Rdatasets/doc/reshape2/tips.html

    Returns:
        A `pandas.DataFrame`.
    """
    return _get_dataset("tips")


def iris():
    """
    Each row represents a flower

    https://en.wikipedia.org/wiki/Iris_flower_data_set

    Returns:
        A `pandas.DataFrame`.
    """
    return _get_dataset("iris")


def wind():
    """
    Each row represents a level of wind intensity in a cardinal direction.

    Returns:
        A `pandas.DataFrame`.
    """
    return _get_dataset("wind")


def election():
    """
    Each row represents voting results for an electoral district in the 2013 Montréal mayoral election.

    Returns:
        A `pandas.DataFrame`.
    """
    return _get_dataset("election")


def carshare():
    """
    Each row represents the availability of car-sharing services per location per hour of data in Montréal.

    Returns:
        A `pandas.DataFrame`.
    """
    return _get_dataset("carshare")


def _get_dataset(d):
    import pandas
    import os

    return pandas.read_csv(os.path.join(os.path.dirname(__file__), d + ".csv.xz"))
