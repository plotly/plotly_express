from ._px import make_figure
import plotly.graph_objs as go

default_max_size = 20
default_symbol_seq = ["circle", "diamond", "square", "x", "cross"]
default_dash_seq = ["solid", "dot", "dash", "longdash", "dashdot", "longdashdot"]


def scatter(
    df,
    x=None,
    y=None,
    color=None,
    symbol=None,
    size=None,
    hover=None,
    text=None,
    color_map={},
    symbol_map={},
    color_sequence=None,
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
    orders={},
    range_x=None,
    range_y=None,
):
    return make_figure(args=locals(), constructor=go.Scatter)


def density_contour(
    df,
    x=None,
    y=None,
    color=None,
    color_map={},
    color_sequence=None,
    facet_row=None,
    facet_col=None,
    log_x=False,
    log_y=False,
    marginal_x=None,
    marginal_y=None,
    orders={},
    range_x=None,
    range_y=None,
    animation_frame=None,
    animation_key=None,
):
    return make_figure(
        args=locals(),
        constructor=go.Histogram2dContour,
        trace_patch=dict(contours=dict(coloring="none")),
    )


def line(
    df,
    x=None,
    y=None,
    split=None,
    color=None,
    dash=None,
    hover=None,
    text=None,
    color_map={},
    dash_map={},
    color_sequence=None,
    dash_sequence=default_dash_seq,
    facet_row=None,
    facet_col=None,
    log_x=False,
    log_y=False,
    error_x=None,
    error_x_minus=None,
    error_y=None,
    error_y_minus=None,
    orders={},
    range_x=None,
    range_y=None,
    animation_frame=None,
    animation_key=None,
):
    return make_figure(args=locals(), constructor=go.Scatter)


def bar(
    df,
    x=None,
    y=None,
    color=None,
    color_map={},
    color_sequence=None,
    facet_row=None,
    facet_col=None,
    hover=None,
    text=None,
    orientation="v",
    normalization="",
    mode="group",
    log_x=False,
    log_y=False,
    error_x=None,
    error_x_minus=None,
    error_y=None,
    error_y_minus=None,
    orders={},
    range_x=None,
    range_y=None,
    animation_frame=None,
    animation_key=None,
):
    return make_figure(
        args=locals(),
        constructor=go.Bar,
        trace_patch=dict(orientation=orientation, textposition="auto"),
        layout_patch=dict(barnorm=normalization, barmode=mode),
    )


def histogram(
    df,
    x=None,
    y=None,
    color=None,
    color_map={},
    color_sequence=None,
    facet_row=None,
    facet_col=None,
    orientation="v",
    mode="stack",
    normalization=None,
    log_x=False,
    log_y=False,
    orders={},
    range_x=None,
    range_y=None,
    animation_frame=None,
    animation_key=None,
):
    return make_figure(
        args=locals(),
        constructor=go.Histogram,
        trace_patch=dict(orientation=orientation, histnorm=normalization),
        layout_patch=dict(barmode=mode),
    )


def violin(
    df,
    x=None,
    y=None,
    color=None,
    color_map={},
    color_sequence=None,
    orientation="v",
    mode="group",
    facet_row=None,
    facet_col=None,
    log_x=False,
    log_y=False,
    orders={},
    range_x=None,
    range_y=None,
    animation_frame=None,
    animation_key=None,
):
    return make_figure(
        args=locals(),
        constructor=go.Violin,
        trace_patch=dict(orientation=orientation),
        layout_patch=dict(violinmode=mode),
    )


def box(
    df,
    x=None,
    y=None,
    color=None,
    color_map={},
    color_sequence=None,
    orientation="v",
    mode="group",
    facet_row=None,
    facet_col=None,
    log_x=False,
    log_y=False,
    orders={},
    range_x=None,
    range_y=None,
    animation_frame=None,
    animation_key=None,
):
    return make_figure(
        args=locals(),
        constructor=go.Box,
        trace_patch=dict(orientation=orientation),
        layout_patch=dict(boxmode=mode),
    )


def scatter_3d(
    df,
    x=None,
    y=None,
    z=None,
    color=None,
    symbol=None,
    size=None,
    text=None,
    color_map={},
    symbol_map={},
    hover=None,
    color_sequence=None,
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
    orders={},
    animation_frame=None,
    animation_key=None,
    range_x=None,
    range_y=None,
    range_z=None,
):
    return make_figure(args=locals(), constructor=go.Scatter3d)


def line_3d(
    df,
    x=None,
    y=None,
    z=None,
    color=None,
    dash=None,
    text=None,
    split=None,
    color_map={},
    dash_map={},
    hover=None,
    color_sequence=None,
    dash_sequence=default_dash_seq,
    log_x=False,
    log_y=False,
    log_z=False,
    error_x=None,
    error_x_minus=None,
    error_y=None,
    error_y_minus=None,
    error_z=None,
    error_z_minus=None,
    orders={},
    animation_frame=None,
    animation_key=None,
    range_x=None,
    range_y=None,
    range_z=None,
):
    return make_figure(args=locals(), constructor=go.Scatter3d)


def scatter_ternary(
    df,
    a=None,
    b=None,
    c=None,
    color=None,
    symbol=None,
    size=None,
    text=None,
    color_map={},
    symbol_map={},
    hover=None,
    color_sequence=None,
    symbol_sequence=default_symbol_seq,
    size_max=default_max_size,
    orders={},
    animation_frame=None,
    animation_key=None,
):
    return make_figure(args=locals(), constructor=go.Scatterternary)


def line_ternary(
    df,
    a=None,
    b=None,
    c=None,
    color=None,
    dash=None,
    split=None,
    hover=None,
    text=None,
    color_map={},
    dash_map={},
    color_sequence=None,
    dash_sequence=default_dash_seq,
    orders={},
    animation_frame=None,
    animation_key=None,
):
    return make_figure(args=locals(), constructor=go.Scatterternary)


def scatter_polar(
    df,
    r,
    theta,
    color=None,
    symbol=None,
    size=None,
    hover=None,
    text=None,
    color_map={},
    symbol_map={},
    color_sequence=None,
    symbol_sequence=default_symbol_seq,
    direction="clockwise",
    startangle=90,
    size_max=default_max_size,
    orders={},
    animation_frame=None,
    animation_key=None,
    range_r=None,
    log_r=False,
):
    return make_figure(args=locals(), constructor=go.Scatterpolar)


def line_polar(
    df,
    r,
    theta,
    color=None,
    dash=None,
    hover=None,
    split=None,
    text=None,
    color_map={},
    dash_map={},
    color_sequence=None,
    dash_sequence=default_dash_seq,
    direction="clockwise",
    startangle=90,
    close_lines=False,
    orders={},
    animation_frame=None,
    animation_key=None,
    range_r=None,
    log_r=False,
):
    return make_figure(args=locals(), constructor=go.Scatterpolar)


def bar_polar(
    df,
    r=None,
    theta=None,
    color=None,
    hover=None,
    color_map={},
    color_sequence=None,
    normalization="",
    mode="relative",
    direction="clockwise",
    startangle=90,
    orders={},
    animation_frame=None,
    animation_key=None,
    range_r=None,
    log_r=False,
):
    return make_figure(
        args=locals(),
        constructor=go.Barpolar,
        layout_patch=dict(barnorm=normalization, barmode=mode),
    )


def choropleth(
    df,
    lat=None,
    lon=None,
    locations=None,
    color=None,
    color_sequence=None,
    hover=None,
    size=None,
    size_max=default_max_size,
    orders={},
    animation_frame=None,
    animation_key=None,
):
    return make_figure(args=locals(), constructor=go.Choropleth)


def scatter_geo(
    df,
    lat=None,
    lon=None,
    locations=None,
    color=None,
    text=None,
    hover=None,
    color_map={},
    color_sequence=None,
    size=None,
    size_max=default_max_size,
    orders={},
    animation_frame=None,
    animation_key=None,
):
    return make_figure(args=locals(), constructor=go.Scattergeo)


def line_geo(
    df,
    lat=None,
    lon=None,
    locations=None,
    color=None,
    dash=None,
    text=None,
    hover=None,
    split=None,
    color_map={},
    color_sequence=None,
    dash_map={},
    dash_sequence=default_dash_seq,
    orders={},
    animation_frame=None,
    animation_key=None,
):
    return make_figure(args=locals(), constructor=go.Scattergeo)


def scatter_mapbox(
    df,
    lat=None,
    lon=None,
    color=None,
    text=None,
    hover=None,
    color_map={},
    color_sequence=None,
    size=None,
    size_max=default_max_size,
    zoom=8,
    orders={},
    animation_frame=None,
    animation_key=None,
):
    return make_figure(args=locals(), constructor=go.Scattermapbox)


def line_mapbox(
    df,
    lat=None,
    lon=None,
    color=None,
    text=None,
    hover=None,
    split=None,
    color_map={},
    color_sequence=None,
    zoom=8,
    orders={},
    animation_frame=None,
    animation_key=None,
):
    return make_figure(args=locals(), constructor=go.Scattermapbox)


def scatter_matrix(
    df,
    dimensions=None,
    color=None,
    symbol=None,
    color_map={},
    symbol_map={},
    color_sequence=None,
    symbol_sequence=default_symbol_seq,
    size=None,
    size_max=default_max_size,
    orders={},
):
    return make_figure(
        args=locals(), constructor=go.Splom, layout_patch=dict(dragmode="select")
    )


def parallel_coordinates(df, dimensions=None, color=None, color_sequence=None):
    return make_figure(args=locals(), constructor=go.Parcoords)


def parallel_categories(df, dimensions=None, color=None, color_sequence=None):
    return make_figure(args=locals(), constructor=go.Parcats)
