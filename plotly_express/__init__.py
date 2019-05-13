"""
`plotly_express` is a terse, consistent, high-level wrapper around `plotly` for rapid \
data exploration and figure generation. See the gallery at https://plotly.github.io/plotly_express
"""

__version__ = "0.2.1"

from ._chart_types import (  # noqa: F401
    scatter,
    scatter_3d,
    scatter_polar,
    scatter_ternary,
    scatter_mapbox,
    scatter_geo,
    line,
    line_3d,
    line_polar,
    line_ternary,
    line_mapbox,
    line_geo,
    area,
    bar,
    bar_polar,
    violin,
    box,
    histogram,
    scatter_matrix,
    parallel_coordinates,
    parallel_categories,
    choropleth,
    density_contour,
)

from ._core import (  # noqa: F401
    ExpressFigure,
    set_mapbox_access_token,
    defaults,
    get_trendline_results,
)

from . import data, colors  # noqa: F401

__all__ = [
    "scatter",
    "scatter_3d",
    "scatter_polar",
    "scatter_ternary",
    "scatter_mapbox",
    "scatter_geo",
    "scatter_matrix",
    "density_contour",
    "line",
    "line_polar",
    "line_ternary",
    "line_mapbox",
    "line_geo",
    "parallel_coordinates",
    "parallel_categories",
    "area",
    "bar",
    "bar_polar",
    "violin",
    "box",
    "histogram",
    "choropleth",
    "data",
    "colors",
    "set_mapbox_access_token",
    "get_trendline_results",
    "ExpressFigure",
]
