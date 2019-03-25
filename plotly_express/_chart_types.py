from ._core import make_figure
from ._doc import make_docstring
import plotly.graph_objs as go
from .colors import qualitative, sequential

default_qualitative = qualitative.Plotly
default_continuous = sequential.Plotly
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
    opacity=None,
    symbol=None,
    size=None,
    hover_name=None,
    text=None,
    facet_row=None,
    facet_col=None,
    error_x=None,
    error_x_minus=None,
    error_y=None,
    error_y_minus=None,
    animation_frame=None,
    animation_group=None,
    category_orders={},
    labels={},
    color_discrete_sequence=default_qualitative,
    color_discrete_map={},
    color_continuous_scale=default_continuous,
    color_continuous_midpoint=None,
    symbol_sequence=default_symbol_seq,
    symbol_map={},
    size_max=default_max_size,
    marginal_x=None,
    marginal_y=None,
    trendline=None,
    trendline_color_override=None,
    log_x=False,
    log_y=False,
    range_x=None,
    range_y=None,
    render_mode="auto",
    title=None,
    template=default_template,
    width=default_width,
    height=default_height,
):
    """
    In a scatter plot, each row of `data_frame` is represented by a symbol mark in 2D space.
    """
    return make_figure(args=locals(), constructor=go.Scatter)


scatter.__doc__ = make_docstring(scatter)


def density_contour(
    data_frame,
    x=None,
    y=None,
    color=None,
    facet_row=None,
    facet_col=None,
    animation_frame=None,
    animation_group=None,
    category_orders={},
    labels={},
    color_discrete_sequence=default_qualitative,
    color_discrete_map={},
    marginal_x=None,
    marginal_y=None,
    trendline=None,
    trendline_color_override=None,
    log_x=False,
    log_y=False,
    range_x=None,
    range_y=None,
    title=None,
    template=default_template,
    width=default_width,
    height=default_height,
):
    """
    In a density contour plot, rows of `data_frame` are grouped together into contour marks to \
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
    facet_row=None,
    facet_col=None,
    error_x=None,
    error_x_minus=None,
    error_y=None,
    error_y_minus=None,
    animation_frame=None,
    animation_group=None,
    category_orders={},
    labels={},
    color_discrete_sequence=default_qualitative,
    color_discrete_map={},
    line_dash_sequence=default_line_dash_seq,
    line_dash_map={},
    log_x=False,
    log_y=False,
    range_x=None,
    range_y=None,
    line_shape=None,
    render_mode="auto",
    title=None,
    template=default_template,
    width=default_width,
    height=default_height,
):
    """
    In a 2D line plot, each row of `data_frame` is represented as vertex of a polyline mark in 2D space.
    """
    return make_figure(args=locals(), constructor=go.Scatter)


line.__doc__ = make_docstring(line)


def bar(
    data_frame,
    x=None,
    y=None,
    color=None,
    facet_row=None,
    facet_col=None,
    hover_name=None,
    text=None,
    error_x=None,
    error_x_minus=None,
    error_y=None,
    error_y_minus=None,
    animation_frame=None,
    animation_group=None,
    category_orders={},
    labels={},
    color_discrete_sequence=default_qualitative,
    color_discrete_map={},
    orientation="v",
    log_x=False,
    log_y=False,
    range_x=None,
    range_y=None,
    title=None,
    template=default_template,
    width=default_width,
    height=default_height,
):
    """
    In a bar plot, each row of `data_frame` is represented as a rectangular mark.
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
    facet_row=None,
    facet_col=None,
    animation_frame=None,
    animation_group=None,
    category_orders={},
    labels={},
    color_discrete_sequence=default_qualitative,
    color_discrete_map={},
    orientation="v",
    barmode="stack",
    barnorm=None,
    histnorm=None,
    log_x=False,
    log_y=False,
    range_x=None,
    range_y=None,
    histfunc=None,
    cumulative=None,
    nbins=None,
    title=None,
    template=default_template,
    width=default_width,
    height=default_height,
):
    """
    In a histogram, rows of `data_frame` are grouped together into a rectangular mark to \
    visualize some aggregate quantity like count or sum.
    """
    return make_figure(
        args=locals(),
        constructor=go.Histogram,
        trace_patch=dict(
            orientation=orientation,
            histnorm=histnorm,
            histfunc=histfunc,
            nbinsx=nbins if orientation == "v" else None,
            nbinsy=nbins if orientation == "h" else None,
            cumulative=dict(enabled=cumulative),
        ),
        layout_patch=dict(barmode=barmode, barnorm=barnorm),
    )


histogram.__doc__ = make_docstring(histogram)


def violin(
    data_frame,
    x=None,
    y=None,
    color=None,
    facet_row=None,
    facet_col=None,
    animation_frame=None,
    animation_group=None,
    category_orders={},
    labels={},
    color_discrete_sequence=default_qualitative,
    color_discrete_map={},
    orientation="v",
    log_x=False,
    log_y=False,
    range_x=None,
    range_y=None,
    points=None,
    box=False,
    title=None,
    template=default_template,
    width=default_width,
    height=default_height,
):
    """
    In a violin plot, rows of `data_frame` are grouped together into a curved mark to \
    visualize their distribution.
    """
    return make_figure(
        args=locals(),
        constructor=go.Violin,
        trace_patch=dict(orientation=orientation, points=points, box=dict(visible=box)),
        layout_patch=dict(violinmode="group"),
    )


violin.__doc__ = make_docstring(violin)


def box(
    data_frame,
    x=None,
    y=None,
    color=None,
    facet_row=None,
    facet_col=None,
    animation_frame=None,
    animation_group=None,
    category_orders={},
    labels={},
    color_discrete_sequence=default_qualitative,
    color_discrete_map={},
    orientation="v",
    log_x=False,
    log_y=False,
    range_x=None,
    range_y=None,
    points=None,
    notched=False,
    title=None,
    template=default_template,
    width=default_width,
    height=default_height,
):
    """
    In a box plot, rows of `data_frame` are grouped together into a box-and-whisker mark to \
    visualize their distribution.
    """
    return make_figure(
        args=locals(),
        constructor=go.Box,
        trace_patch=dict(orientation=orientation, boxpoints=points, notched=notched),
        layout_patch=dict(boxmode="group"),
    )


box.__doc__ = make_docstring(box)


def scatter_3d(
    data_frame,
    x=None,
    y=None,
    z=None,
    color=None,
    opacity=None,
    symbol=None,
    size=None,
    text=None,
    hover_name=None,
    error_x=None,
    error_x_minus=None,
    error_y=None,
    error_y_minus=None,
    error_z=None,
    error_z_minus=None,
    animation_frame=None,
    animation_group=None,
    category_orders={},
    labels={},
    size_max=default_max_size,
    color_discrete_sequence=default_qualitative,
    color_discrete_map={},
    color_continuous_scale=default_continuous,
    color_continuous_midpoint=None,
    symbol_sequence=default_symbol_seq,
    symbol_map={},
    log_x=False,
    log_y=False,
    log_z=False,
    range_x=None,
    range_y=None,
    range_z=None,
    title=None,
    template=default_template,
    width=default_width,
    height=default_height,
):
    """
    In a 3D scatter plot, each row of `data_frame` is represented by a symbol mark in 3D space.
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
    hover_name=None,
    error_x=None,
    error_x_minus=None,
    error_y=None,
    error_y_minus=None,
    error_z=None,
    error_z_minus=None,
    animation_frame=None,
    animation_group=None,
    category_orders={},
    labels={},
    color_discrete_sequence=default_qualitative,
    color_discrete_map={},
    line_dash_sequence=default_line_dash_seq,
    line_dash_map={},
    log_x=False,
    log_y=False,
    log_z=False,
    range_x=None,
    range_y=None,
    range_z=None,
    title=None,
    template=default_template,
    width=default_width,
    height=default_height,
):
    """
    In a 3D line plot, each row of `data_frame` is represented as vertex of a polyline mark in 3D space.
    """
    return make_figure(args=locals(), constructor=go.Scatter3d)


line_3d.__doc__ = make_docstring(line_3d)


def scatter_ternary(
    data_frame,
    a=None,
    b=None,
    c=None,
    color=None,
    opacity=None,
    symbol=None,
    size=None,
    text=None,
    hover_name=None,
    animation_frame=None,
    animation_group=None,
    category_orders={},
    labels={},
    color_discrete_sequence=default_qualitative,
    color_discrete_map={},
    color_continuous_scale=default_continuous,
    color_continuous_midpoint=None,
    symbol_sequence=default_symbol_seq,
    symbol_map={},
    size_max=default_max_size,
    title=None,
    template=default_template,
    width=default_width,
    height=default_height,
):
    """
    In a ternary scatter plot, each row of `data_frame` is represented by a symbol mark in ternary coordinates.
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
    animation_frame=None,
    animation_group=None,
    category_orders={},
    labels={},
    color_discrete_sequence=default_qualitative,
    color_discrete_map={},
    line_dash_sequence=default_line_dash_seq,
    line_dash_map={},
    line_shape=None,
    title=None,
    template=default_template,
    width=default_width,
    height=default_height,
):
    """
    In a ternary line plot, each row of `data_frame` is represented as vertex of a polyline mark in ternary coordinates.
    """
    return make_figure(args=locals(), constructor=go.Scatterternary)


line_ternary.__doc__ = make_docstring(line_ternary)


def scatter_polar(
    data_frame,
    r=None,
    theta=None,
    color=None,
    opacity=None,
    symbol=None,
    size=None,
    hover_name=None,
    text=None,
    animation_frame=None,
    animation_group=None,
    category_orders={},
    labels={},
    color_discrete_sequence=default_qualitative,
    color_discrete_map={},
    color_continuous_scale=default_continuous,
    color_continuous_midpoint=None,
    symbol_sequence=default_symbol_seq,
    symbol_map={},
    direction="clockwise",
    start_angle=90,
    size_max=default_max_size,
    range_r=None,
    log_r=False,
    render_mode="auto",
    title=None,
    template=default_template,
    width=default_width,
    height=default_height,
):
    """
    In a polar scatter plot, each row of `data_frame` is represented by a symbol mark in
    polar coordinates.
    """
    return make_figure(args=locals(), constructor=go.Scatterpolar)


scatter_polar.__doc__ = make_docstring(scatter_polar)


def line_polar(
    data_frame,
    r=None,
    theta=None,
    color=None,
    line_dash=None,
    hover_name=None,
    line_group=None,
    text=None,
    animation_frame=None,
    animation_group=None,
    category_orders={},
    labels={},
    color_discrete_sequence=default_qualitative,
    color_discrete_map={},
    line_dash_sequence=default_line_dash_seq,
    line_dash_map={},
    direction="clockwise",
    start_angle=90,
    line_close=False,
    line_shape=None,
    render_mode="auto",
    range_r=None,
    log_r=False,
    title=None,
    template=default_template,
    width=default_width,
    height=default_height,
):
    """
    In a polar line plot, each row of `data_frame` is represented as vertex of a polyline mark in polar coordinates.
    """
    return make_figure(args=locals(), constructor=go.Scatterpolar)


line_polar.__doc__ = make_docstring(line_polar)


def bar_polar(
    data_frame,
    r=None,
    theta=None,
    color=None,
    hover_name=None,
    animation_frame=None,
    animation_group=None,
    category_orders={},
    labels={},
    color_discrete_sequence=default_qualitative,
    color_discrete_map={},
    barnorm="",
    barmode="relative",
    direction="clockwise",
    start_angle=90,
    range_r=None,
    log_r=False,
    title=None,
    template=default_template,
    width=default_width,
    height=default_height,
):
    """
    In a polar bar plot, each row of `data_frame` is represented as a wedge mark in polar coordinates.
    """
    return make_figure(
        args=locals(),
        constructor=go.Barpolar,
        layout_patch=dict(barnorm=barnorm, barmode=barmode),
    )


bar_polar.__doc__ = make_docstring(bar_polar)


def choropleth(
    data_frame,
    lat=None,
    lon=None,
    locations=None,
    locationmode=None,
    color=None,
    hover_name=None,
    size=None,
    animation_frame=None,
    animation_group=None,
    category_orders={},
    labels={},
    color_continuous_scale=default_continuous,
    color_continuous_midpoint=None,
    size_max=default_max_size,
    projection=None,
    scope=None,
    center=None,
    title=None,
    template=default_template,
    width=default_width,
    height=default_height,
):
    """
    In a choropleth map, each row of `data_frame` is represented by a colored region mark on a map.
    """
    return make_figure(
        args=locals(),
        constructor=go.Choropleth,
        trace_patch=dict(locationmode=locationmode),
    )


choropleth.__doc__ = make_docstring(choropleth)


def scatter_geo(
    data_frame,
    lat=None,
    lon=None,
    locations=None,
    locationmode=None,
    color=None,
    text=None,
    hover_name=None,
    size=None,
    animation_frame=None,
    animation_group=None,
    category_orders={},
    labels={},
    color_discrete_sequence=default_qualitative,
    color_discrete_map={},
    color_continuous_scale=default_continuous,
    color_continuous_midpoint=None,
    size_max=default_max_size,
    projection=None,
    scope=None,
    center=None,
    title=None,
    template=default_template,
    width=default_width,
    height=default_height,
):
    """
    In a geographic scatter plot, each row of `data_frame` is represented by a symbol mark on a map.
    """
    return make_figure(
        args=locals(),
        constructor=go.Scattergeo,
        trace_patch=dict(locationmode=locationmode),
    )


scatter_geo.__doc__ = make_docstring(scatter_geo)


def line_geo(
    data_frame,
    lat=None,
    lon=None,
    locations=None,
    locationmode=None,
    color=None,
    line_dash=None,
    text=None,
    hover_name=None,
    line_group=None,
    animation_frame=None,
    animation_group=None,
    category_orders={},
    labels={},
    color_discrete_sequence=default_qualitative,
    color_discrete_map={},
    line_dash_sequence=default_line_dash_seq,
    line_dash_map={},
    projection=None,
    scope=None,
    center=None,
    title=None,
    template=default_template,
    width=default_width,
    height=default_height,
):
    """
    In a geographic line plot, each row of `data_frame` is represented as vertex of a polyline mark on a map.
    """
    return make_figure(
        args=locals(),
        constructor=go.Scattergeo,
        trace_patch=dict(locationmode=locationmode),
    )


line_geo.__doc__ = make_docstring(line_geo)


def scatter_mapbox(
    data_frame,
    lat=None,
    lon=None,
    color=None,
    text=None,
    hover_name=None,
    size=None,
    animation_frame=None,
    animation_group=None,
    category_orders={},
    labels={},
    color_discrete_sequence=default_qualitative,
    color_discrete_map={},
    color_continuous_scale=default_continuous,
    color_continuous_midpoint=None,
    size_max=default_max_size,
    zoom=8,
    title=None,
    template=default_template,
    width=default_width,
    height=default_height,
):
    """
    In a Mapbox scatter plot, each row of `data_frame` is represented by a symbol mark on a Mapbox map.
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
    animation_frame=None,
    animation_group=None,
    category_orders={},
    labels={},
    color_discrete_sequence=default_qualitative,
    color_discrete_map={},
    zoom=8,
    title=None,
    template=default_template,
    width=default_width,
    height=default_height,
):
    """
    In a Mapbox line plot, each row of `data_frame` is represented as vertex of a polyline mark on a Mapbox map.
    """
    return make_figure(args=locals(), constructor=go.Scattermapbox)


line_mapbox.__doc__ = make_docstring(line_mapbox)


def scatter_matrix(
    data_frame,
    dimensions=None,
    color=None,
    opacity=None,
    symbol=None,
    size=None,
    category_orders={},
    labels={},
    color_discrete_sequence=default_qualitative,
    color_discrete_map={},
    color_continuous_scale=default_continuous,
    color_continuous_midpoint=None,
    symbol_sequence=default_symbol_seq,
    symbol_map={},
    size_max=default_max_size,
    title=None,
    template=default_template,
    width=default_width,
    height=default_height,
):
    """
    In a scatter plot matrix (or SPLOM), each row of `data_frame` is represented \
    by a multiple symbol marks, one in each cell of a grid of 2D scatter plots, which \
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
    labels={},
    color_continuous_scale=default_continuous,
    color_continuous_midpoint=None,
    title=None,
    template=default_template,
    width=default_width,
    height=default_height,
):
    """
    In a parallel coordinates plot, each row of `data_frame` is represented \
    by a polyline mark which traverses a set of parallel axes, one for each of the \
    `dimensions`.
    """
    return make_figure(args=locals(), constructor=go.Parcoords)


parallel_coordinates.__doc__ = make_docstring(parallel_coordinates)


def parallel_categories(
    data_frame,
    dimensions=None,
    color=None,
    labels={},
    color_continuous_scale=default_continuous,
    color_continuous_midpoint=None,
    title=None,
    template=default_template,
    width=default_width,
    height=default_height,
):
    """
    In a parallel categories (or parallel sets) plot, each row of `data_frame` is \
    grouped with other rows that share the same values of `dimensions` and then plotted \
    as a polyline mark through a set of parallel axes, one for each of the `dimensions`.
    """
    return make_figure(args=locals(), constructor=go.Parcats)


parallel_categories.__doc__ = make_docstring(parallel_categories)
