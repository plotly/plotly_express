from setuptools import setup, find_packages
from os import path

# io.open is needed for projects that support Python 2.7
# It ensures open() defaults to text mode with universal newlines,
# and accepts an argument to specify the text encoding
# Python 3 only projects can skip this import
from io import open

here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()


setup(
    name="plotly_express",  # Required
    version="0.1a7",  # Required
    description="Plotly Express: a high level wrapper for Plotly.py",  # Optional
    long_description=long_description,  # Optional
    long_description_content_type="text/markdown",  # Optional (see note above)
    url="https://github.com/plotly/plotly_express",  # Optional
    author="Nicolas Kruchten",  # Optional
    author_email="nicolas@plot.ly",  # Optional
    classifiers=[  # Optional
        "Development Status :: 3 - Alpha",
        "Topic :: Scientific/Engineering :: Visualization",
        "License :: OSI Approved :: MIT License",
    ],
    packages=find_packages(),  # Required
    package_data={"plotly_express": ["data/*.csv.xz"]},
    install_requires=["pandas>=0.20.0", "plotly>=3.6.0"],  # Optional
)
