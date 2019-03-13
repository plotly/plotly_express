from ._core import make_figure
from ._doc import make_docstring
import plotly.graph_objs as go
from .colors.qualitative import Plotly as default_qualitative
from .colors.sequential import Plotly as default_continuous

default_template = "plotly"
default_width = None
default_height = 600
default_max_size = 20
default_symbol_seq = ["circle", "diamond", "square", "x", "cross"]
default_line_dash_seq = ["solid", "dot", "dash", "longdash", "dashdot", "longdashdot"]


def scatter(
    data_frame,
    x=None,
    y=None,
    color=None,
    symbol=None,
    size=None,
    hover_name=None,
    text=None,
    color_discrete_map={},
    symbol_map={},
    color_discrete_sequence=default_qualitative,
    color_continuous_scale=default_continuous,
    color_continuous_midpoint=None,
    symbol_sequence=default_symbol_seq,
    facet_row=None,
    facet_col=None,
    log_x=False,
    log_y=False,
    marginal_x=None,
    marginal_y=None,
    error_x=None,
    error_x_minus=None,
    error_y=None,
    error_y_minus=None,
    size_max=default_max_size,
    animation_frame=None,
    animation_key=None,
    category_orders={},
    range_x=None,
    range_y=None,
    title=None,
    template=default_template,
    labels={},
    width=default_width,
    height=default_height,
    trendline=None,
    trendline_color_override=None,
    render_mode="auto",
):
    """
    In a scatter plot, each row of `data_frame` is represented by a marker in 2D space.
    """
    return make_figure(args=locals(), constructor=go.Scatter)


scatter.__doc__ = make_docstring(scatter)


def density_contour(
    data_frame,
    x=None,
    y=None,
    color=None,
    color_discrete_map={},
    color_discrete_sequence=default_qualitative,
    facet_row=None,
    facet_col=None,
    log_x=False,
    log_y=False,
    marginal_x=None,
    marginal_y=None,
    category_orders={},
    range_x=None,
    range_y=None,
    animation_frame=None,
    animation_key=None,
    title=None,
    template=default_template,
    labels={},
    width=default_width,
    height=default_height,
    trendline=None,
    trendline_color_override=None,
):
    """
    In a density contour plot, rows of `data_frame` are grouped together into contours to \
    visualize the density of their distribution in 2D space.
    """
    return make_figure(
        args=locals(),
        constructor=go.Histogram2dContour,
        trace_patch=dict(contours=dict(coloring="none")),
    )


density_contour.__doc__ = make_docstring(density_contour)


def line(
    data_frame,
    x=None,
    y=None,
    line_group=None,
    color=None,
    line_dash=None,
    hover_name=None,
    text=None,
    color_discrete_map={},
    line_dash_map={},
    color_discrete_sequence=default_qualitative,
    line_dash_sequence=default_line_dash_seq,
    facet_row=None,
    facet_col=None,
    log_x=False,
    log_y=False,
    error_x=None,
    error_x_minus=None,
    error_y=None,
    error_y_minus=None,
    category_orders={},
    range_x=None,
    range_y=None,
    animation_frame=None,
    animation_key=None,
    title=None,
    template=default_template,
    labels={},
    width=default_width,
    height=default_height,
    render_mode="auto",
):
    """
    In a 2D line plot, each row of `data_frame` is represented as vertex of a polyline in 2D space.
    """
    return make_figure(args=locals(), constructor=go.Scatter)


line.__doc__ = make_docstring(line)


def bar(
    data_frame,
    x=None,
    y=None,
    color=None,
    color_discrete_map={},
    color_discrete_sequence=default_qualitative,
    facet_row=None,
    facet_col=None,
    hover_name=None,
    text=None,
    orientation="v",
    log_x=False,
    log_y=False,
    error_x=None,
    error_x_minus=None,
    error_y=None,
    error_y_minus=None,
    category_orders={},
    range_x=None,
    range_y=None,
    animation_frame=None,
    animation_key=None,
    title=None,
    template=default_template,
    labels={},
    width=default_width,
    height=default_height,
):
    """
    In a bar plot, each row of `data_frame` is represented as a rectangle.
    """
    return make_figure(
        args=locals(),
        constructor=go.Bar,
        trace_patch=dict(orientation=orientation, textposition="auto"),
        layout_patch=dict(barmode="relative"),
    )


bar.__doc__ = make_docstring(bar)


def histogram(
    data_frame,
    x=None,
    y=None,
    color=None,
    color_discrete_map={},
    color_discrete_sequence=default_qualitative,
    facet_row=None,
    facet_col=None,
    orientation="v",
    mode="stack",
    normalization=None,
    log_x=False,
    log_y=False,
    category_orders={},
    range_x=None,
    range_y=None,
    animation_frame=None,
    animation_key=None,
    title=None,
    template=default_template,
    labels={},
    width=default_width,
    height=default_height,
):
    """
    In a histogram, rows of `data_frame` are grouped together into a rectangle to \
    visualize some aggregate quantity like count or sum.
    """
    return make_figure(
        args=locals(),
        constructor=go.Histogram,
        trace_patch=dict(orientation=orientation, histnorm=normalization),
        layout_patch=dict(barmode=mode),
    )


histogram.__doc__ = make_docstring(histogram)


def violin(
    data_frame,
    x=None,
    y=None,
    color=None,
    color_discrete_map={},
    color_discrete_sequence=default_qualitative,
    orientation="v",
    facet_row=None,
    facet_col=None,
    log_x=False,
    log_y=False,
    category_orders={},
    range_x=None,
    range_y=None,
    animation_frame=None,
    animation_key=None,
    title=None,
    template=default_template,
    labels={},
    width=default_width,
    height=default_height,
):
    """
    In a violin plot, rows of `data_frame` are grouped together into a curved shape to \
    visualize their distribution.
    """
    return make_figure(
        args=locals(),
        constructor=go.Violin,
        trace_patch=dict(orientation=orientation),
        layout_patch=dict(violinmode="group"),
    )


violin.__doc__ = make_docstring(violin)


def box(
    data_frame,
    x=None,
    y=None,
    color=None,
    color_discrete_map={},
    color_discrete_sequence=default_qualitative,
    orientation="v",
    facet_row=None,
    facet_col=None,
    log_x=False,
    log_y=False,
    category_orders={},
    range_x=None,
    range_y=None,
    animation_frame=None,
    animation_key=None,
    title=None,
    template=default_template,
    labels={},
    width=default_width,
    height=default_height,
):
    """
    In a box plot, rows of `data_frame` are grouped together into a box-and-whisker shape to \
    visualize their distribution.
    """
    return make_figure(
        args=locals(),
        constructor=go.Box,
        trace_patch=dict(orientation=orientation),
        layout_patch=dict(boxmode="group"),
    )


box.__doc__ = make_docstring(box)


def scatter_3d(
    data_frame,
    x=None,
    y=None,
    z=None,
    color=None,
    symbol=None,
    size=None,
    text=None,
    color_discrete_map={},
    symbol_map={},
    hover_name=None,
    color_discrete_sequence=default_qualitative,
    color_continuous_scale=default_continuous,
    color_continuous_midpoint=None,
    symbol_sequence=default_symbol_seq,
    log_x=False,
    log_y=False,
    log_z=False,
    error_x=None,
    error_x_minus=None,
    error_y=None,
    error_y_minus=None,
    error_z=None,
    error_z_minus=None,
    size_max=default_max_size,
    category_orders={},
    animation_frame=None,
    animation_key=None,
    range_x=None,
    range_y=None,
    range_z=None,
    title=None,
    template=default_template,
    labels={},
    width=default_width,
    height=default_height,
):
    """
    In a 3D scatter plot, each row of `data_frame` is represented by a marker in 3D space.
    """
    return make_figure(args=locals(), constructor=go.Scatter3d)


scatter_3d.__doc__ = make_docstring(scatter_3d)


def line_3d(
    data_frame,
    x=None,
    y=None,
    z=None,
    color=None,
    line_dash=None,
    text=None,
    line_group=None,
    color_discrete_map={},
    line_dash_map={},
    hover_name=None,
    color_discrete_sequence=default_qualitative,
    line_dash_sequence=default_line_dash_seq,
    log_x=False,
    log_y=False,
    log_z=False,
    error_x=None,
    error_x_minus=None,
    error_y=None,
    error_y_minus=None,
    error_z=None,
    error_z_minus=None,
    category_orders={},
    animation_frame=None,
    animation_key=None,
    range_x=None,
    range_y=None,
    range_z=None,
    title=None,
    template=default_template,
    labels={},
    width=default_width,
    height=default_height,
):
    """
    In a 3D line plot, each row of `data_frame` is represented as vertex of a polyline in 3D space.
    """
    return make_figure(args=locals(), constructor=go.Scatter3d)


line_3d.__doc__ = make_docstring(line_3d)


def scatter_ternary(
    data_frame,
    a=None,
    b=None,
    c=None,
    color=None,
    symbol=None,
    size=None,
    text=None,
    color_discrete_map={},
    symbol_map={},
    hover_name=None,
    color_discrete_sequence=default_qualitative,
    color_continuous_scale=default_continuous,
    color_continuous_midpoint=None,
    symbol_sequence=default_symbol_seq,
    size_max=default_max_size,
    category_orders={},
    animation_frame=None,
    animation_key=None,
    title=None,
    template=default_template,
    labels={},
    width=default_width,
    height=default_height,
):
    """
    In a ternary scatter plot, each row of `data_frame` is represented by a marker in ternary coordinates.
    """
    return make_figure(args=locals(), constructor=go.Scatterternary)


scatter_ternary.__doc__ = make_docstring(scatter_ternary)


def line_ternary(
    data_frame,
    a=None,
    b=None,
    c=None,
    color=None,
    line_dash=None,
    line_group=None,
    hover_name=None,
    text=None,
    color_discrete_map={},
    line_dash_map={},
    color_discrete_sequence=default_qualitative,
    line_dash_sequence=default_line_dash_seq,
    category_orders={},
    animation_frame=None,
    animation_key=None,
    title=None,
    template=default_template,
    labels={},
    width=default_width,
    height=default_height,
):
    """
    In a ternary line plot, each row of `data_frame` is represented as vertex of a polyline in ternary coordinates.
    """
    return make_figure(args=locals(), constructor=go.Scatterternary)


line_ternary.__doc__ = make_docstring(line_ternary)


def scatter_polar(
    data_frame,
    r,
    theta,
    color=None,
    symbol=None,
    size=None,
    hover_name=None,
    text=None,
    color_discrete_map={},
    symbol_map={},
    color_discrete_sequence=default_qualitative,
    color_continuous_scale=default_continuous,
    color_continuous_midpoint=None,
    symbol_sequence=default_symbol_seq,
    direction="clockwise",
    startangle=90,
    size_max=default_max_size,
    category_orders={},
    animation_frame=None,
    animation_key=None,
    range_r=None,
    log_r=False,
    title=None,
    template=default_template,
    labels={},
    width=default_width,
    height=default_height,
    render_mode="auto",
):
    """
    In a polar scatter plot, each row of `data_frame` is represented by a marker in
    polar coordinates.
    """
    return make_figure(args=locals(), constructor=go.Scatterpolar)


scatter_polar.__doc__ = make_docstring(scatter_polar)


def line_polar(
    data_frame,
    r,
    theta,
    color=None,
    line_dash=None,
    hover_name=None,
    line_group=None,
    text=None,
    color_discrete_map={},
    line_dash_map={},
    color_discrete_sequence=default_qualitative,
    line_dash_sequence=default_line_dash_seq,
    direction="clockwise",
    startangle=90,
    line_close=False,
    category_orders={},
    animation_frame=None,
    animation_key=None,
    range_r=None,
    log_r=False,
    title=None,
    template=default_template,
    labels={},
    width=default_width,
    height=default_height,
    render_mode="auto",
):
    """
    In a polar line plot, each row of `data_frame` is represented as vertex of a polyline in polar coordinates.
    """
    return make_figure(args=locals(), constructor=go.Scatterpolar)


line_polar.__doc__ = make_docstring(line_polar)


def bar_polar(
    data_frame,
    r=None,
    theta=None,
    color=None,
    hover_name=None,
    color_discrete_map={},
    color_discrete_sequence=default_qualitative,
    normalization="",
    mode="relative",
    direction="clockwise",
    startangle=90,
    category_orders={},
    animation_frame=None,
    animation_key=None,
    range_r=None,
    log_r=False,
    title=None,
    template=default_template,
    labels={},
    width=default_width,
    height=default_height,
):
    """
    In a polar bar plot, each row of `data_frame` is represented as a sector in polar coordinates.
    """
    return make_figure(
        args=locals(),
        constructor=go.Barpolar,
        layout_patch=dict(barnorm=normalization, barmode=mode),
    )


bar_polar.__doc__ = make_docstring(bar_polar)


def choropleth(
    data_frame,
    lat=None,
    lon=None,
    locations=None,
    color=None,
    color_continuous_scale=default_continuous,
    color_continuous_midpoint=None,
    hover_name=None,
    size=None,
    size_max=default_max_size,
    category_orders={},
    animation_frame=None,
    animation_key=None,
    title=None,
    template=default_template,
    labels={},
    width=default_width,
    height=default_height,
):
    """
    In a choropleth map, each row of `data_frame` is represented by a colored region on a map.
    """
    return make_figure(args=locals(), constructor=go.Choropleth)


choropleth.__doc__ = make_docstring(choropleth)


def scatter_geo(
    data_frame,
    lat=None,
    lon=None,
    locations=None,
    color=None,
    text=None,
    hover_name=None,
    color_discrete_map={},
    color_discrete_sequence=default_qualitative,
    color_continuous_scale=default_continuous,
    color_continuous_midpoint=None,
    size=None,
    size_max=default_max_size,
    category_orders={},
    animation_frame=None,
    animation_key=None,
    title=None,
    template=default_template,
    labels={},
    width=default_width,
    height=default_height,
):
    """
    In a geographic scatter plot, each row of `data_frame` is represented by a marker on a map.
    """
    return make_figure(args=locals(), constructor=go.Scattergeo)


scatter_geo.__doc__ = make_docstring(scatter_geo)


def line_geo(
    data_frame,
    lat=None,
    lon=None,
    locations=None,
    color=None,
    line_dash=None,
    text=None,
    hover_name=None,
    line_group=None,
    color_discrete_map={},
    color_discrete_sequence=default_qualitative,
    line_dash_map={},
    line_dash_sequence=default_line_dash_seq,
    category_orders={},
    animation_frame=None,
    animation_key=None,
    title=None,
    template=default_template,
    labels={},
    width=default_width,
    height=default_height,
):
    """
    In a geographic line plot, each row of `data_frame` is represented as vertex of a polyline on a map.
    """
    return make_figure(args=locals(), constructor=go.Scattergeo)


line_geo.__doc__ = make_docstring(line_geo)


def scatter_mapbox(
    data_frame,
    lat=None,
    lon=None,
    color=None,
    text=None,
    hover_name=None,
    color_discrete_map={},
    color_discrete_sequence=default_qualitative,
    color_continuous_scale=default_continuous,
    color_continuous_midpoint=None,
    size=None,
    size_max=default_max_size,
    zoom=8,
    category_orders={},
    animation_frame=None,
    animation_key=None,
    title=None,
    template=default_template,
    labels={},
    width=default_width,
    height=default_height,
):
    """
    In a Mapbox scatter plot, each row of `data_frame` is represented by a marker on a Mapbox map.
    """
    return make_figure(args=locals(), constructor=go.Scattermapbox)


scatter_mapbox.__doc__ = make_docstring(scatter_mapbox)


def line_mapbox(
    data_frame,
    lat=None,
    lon=None,
    color=None,
    text=None,
    hover_name=None,
    line_group=None,
    color_discrete_map={},
    color_discrete_sequence=default_qualitative,
    zoom=8,
    category_orders={},
    animation_frame=None,
    animation_key=None,
    title=None,
    template=default_template,
    labels={},
    width=default_width,
    height=default_height,
):
    """
    In a Mapbox line plot, each row of `data_frame` is represented as vertex of a polyline on a Mapbox map.
    """
    return make_figure(args=locals(), constructor=go.Scattermapbox)


line_mapbox.__doc__ = make_docstring(line_mapbox)


def scatter_matrix(
    data_frame,
    dimensions=None,
    color=None,
    symbol=None,
    color_discrete_map={},
    symbol_map={},
    color_discrete_sequence=default_qualitative,
    color_continuous_scale=default_continuous,
    color_continuous_midpoint=None,
    symbol_sequence=default_symbol_seq,
    size=None,
    size_max=default_max_size,
    category_orders={},
    title=None,
    template=default_template,
    labels={},
    width=default_width,
    height=default_height,
):
    """
    In a scatter plot matrix (or SPLOM), each row of `data_frame` is represented \
    by a multiple markers, one in each cell of a grid of 2D scatter plots, which \
    plot each pair of `dimensions` against each other.
    """
    return make_figure(
        args=locals(), constructor=go.Splom, layout_patch=dict(dragmode="select")
    )


scatter_matrix.__doc__ = make_docstring(scatter_matrix)


def parallel_coordinates(
    data_frame,
    dimensions=None,
    color=None,
    color_continuous_scale=default_continuous,
    color_continuous_midpoint=None,
    title=None,
    template=default_template,
    labels={},
    width=default_width,
    height=default_height,
):
    """
    In a parallel coordinates plot, each row of `data_frame` is represented \
    by a polyline which traverses a set of parallel axes, one for each of the \
    `dimensions`.
    """
    return make_figure(args=locals(), constructor=go.Parcoords)


parallel_coordinates.__doc__ = make_docstring(parallel_coordinates)


def parallel_categories(
    data_frame,
    dimensions=None,
    color=None,
    color_continuous_scale=default_continuous,
    color_continuous_midpoint=None,
    title=None,
    template=default_template,
    labels={},
    width=default_width,
    height=default_height,
):
    """
    In a parallel categories (or parallel sets) plot, each row of `data_frame` is \
    grouped with other rows that share the same values of `dimensions` and then plotted \
    as a polyline through a set of parallel axes, one for each of the `dimensions`.
    """
    return make_figure(args=locals(), constructor=go.Parcats)


parallel_categories.__doc__ = make_docstring(parallel_categories)
