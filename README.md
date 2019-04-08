# Plotly Express

Plotly Express is a terse, consistent, high-level wrapper around [Plotly.py](https://plot.ly/python) for rapid data exploration and figure generation.

Documentation and examples can be found at https://plotly.express/

## Installation

Plotly Express is compatible with Python 3+ and Python 2.7.

### Via `pip`

Just running `pip install plotly_express` in your terminal should do it!

### Via `conda`

You'll have to install from the `plotly` channel with `conda install -c plotly plotly_express`

### Running in JupyterLab

Using Plotly Express in JupyterLab requires the [`plotly-extension`](https://github.com/jupyterlab/jupyter-renderers/tree/master/packages/plotly-extension) to be installed by running `jupyter labextension install @jupyterlab/plotly-extension`.

## Troubleshooting

Plotly Express depends on very recent versions of `plotly` and it's sometimes possible to get into a state where you have multiple versions of `plotly` installed (e.g. once with `pip` and once with `conda`) so be sure to check your version by running `plotly.__version__` in the same environment that you're having issues with `plotly_express`.
