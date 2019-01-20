import plotly.graph_objs as go
from plotly.offline import init_notebook_mode, iplot
from collections import namedtuple
import plotly.io as pio

MAPBOX_TOKEN = ""


def set_mapbox_access_token(token):
    global MAPBOX_TOKEN
    MAPBOX_TOKEN = token


pio.templates["px"] = dict(
    layout=dict(margin={"t": 60}, height=600, legend={"tracegroupgap": 0})
)


class FigurePx(go.Figure):
    print(MAPBOX_TOKEN)
    offline_initialized = False

    def __init__(self, *args, **kwargs):
        super(FigurePx, self).__init__(*args, **kwargs)
        self.update(layout={"template": "plotly+px"})

    def _ipython_display_(self):
        if not FigurePx.offline_initialized:
            init_notebook_mode()
            FigurePx.offline_initialized = True
        iplot(self, show_link=False)


default_max_size = 20
default_color_seq = (
    ["#636efa", "#EF553B", "#00cc96", "#ab63fa"]
    + ["#19d3f3", "#e763fa", "#fecb52", "#ffa15a"]
    + ["#ff6692", "#b6e880"]
)
default_symbol_seq = ["circle", "diamond", "square", "x", "cross"]
default_dash_seq = ["solid", "dot", "dash", "longdash", "dashdot", "longdashdot"]
Mapping = namedtuple(
    "Mapping",
    ["show_in_trace_name", "grouper", "val_map", "sequence", "updater", "variable"],
)
TraceSpec = namedtuple("TraceSpec", ["constructor", "vars", "trace_patch"])


def make_mapping(args, variable):
    if variable == "split":
        return Mapping(
            show_in_trace_name=False,
            grouper=args["split"],
            val_map={},
            sequence=[""],
            variable="split",
            updater=(lambda trace, v: v),
        )
    if variable == "row" or variable == "col":
        letter = "x" if variable == "col" else "y"
        return Mapping(
            show_in_trace_name=False,
            variable=letter,
            grouper=args[variable],
            val_map={},
            sequence=[letter + str(i) for i in range(1, 1000)],
            updater=lambda trace, v: trace.update({letter + "axis": v}),
        )
    (parent, variable) = variable.split(".")
    return Mapping(
        show_in_trace_name=True,
        variable=variable,
        grouper=args[variable],
        val_map=args[variable + "_map"].copy(),
        sequence=args[variable + "_sequence"],
        updater=lambda trace, v: trace.update({parent: {variable: v}}),
    )


def make_trace_kwargs(args, trace_spec, g, mapping_labels, sizeref):

    if "close_lines" in args and args["close_lines"]:
        g = g.append(g.iloc[0])
    result = trace_spec.trace_patch or {}
    hover_header = ""
    for k in trace_spec.vars:
        v = args[k]
        if k == "dimensions":
            result["dimensions"] = [
                dict(label=name, values=column.values)
                for name, column in g.iteritems()
                if (not v) or (name in v)
            ]
        elif v:
            if k == "size":
                result["marker"] = dict(size=g[v], sizemode="area", sizeref=sizeref)
                mapping_labels.append(("%s=%%{%s}" % (v, "marker.size"), None))
            elif k.startswith("error"):
                error_xy = k[:7]
                arr = "arrayminus" if k.endswith("minus") else "array"
                if error_xy not in result:
                    result[error_xy] = {}
                result[error_xy][arr] = g[v]
            elif k == "hover":
                result["hovertext"] = g[v]
                hover_header = "<b>%{hovertext}</b><br><br>"
            else:
                result[k] = g[v]
                mapping_labels.append(("%s=%%{%s}" % (v, k), None))
    if trace_spec.constructor in [go.Scatter, go.Bar]:
        result["hovertemplate"] = hover_header + (
            "<br>".join(s for s, t in mapping_labels) + "<extra></extra>"
        )
    return result


def configure_axes(args, constructor, fig, axes, orders):
    configurators = {
        go.Scatter: configure_cartesian_axes,
        go.Bar: configure_cartesian_axes,
        go.Box: configure_cartesian_axes,
        go.Violin: configure_cartesian_axes,
        go.Histogram: configure_cartesian_axes,
        go.Histogram2dContour: configure_cartesian_axes,
        go.Histogram2d: configure_cartesian_axes,
        go.Scatter3d: configure_3d_axes,
        go.Scatterternary: configure_ternary_axes,
        go.Scatterpolar: configure_polar_axes,
        go.Barpolar: configure_polar_axes,
        go.Scattermapbox: configure_mapbox,
        go.Scattergeo: configure_geo,
        go.Choropleth: configure_geo,
    }
    if constructor in configurators:
        fig.update(configurators[constructor](args, fig, axes, orders))


def configure_cartesian_axes(args, fig, axes, orders):
    if "marginal_x" in args and (args["marginal_x"] or args["marginal_y"]):
        layout = {}
        for letter in ["x", "y"]:
            otherletter = "x" if letter == "y" else "y"
            if args["marginal_" + letter]:
                if args["marginal_" + letter] == "histogram" or (
                    "color" in args and args["color"]
                ):
                    main_size = 0.74
                else:
                    main_size = 0.84
                layout[otherletter + "axis1"] = {
                    "domain": [0, main_size],
                    "showgrid": True,
                }
                layout[otherletter + "axis2"] = {
                    "domain": [main_size + 0.005, 1],
                    "showticklabels": False,
                }
                if args["log_" + letter]:
                    layout[letter + "axis1"]["type"] = "log"
        return dict(layout=layout)
    gap = 0.1
    layout = {
        "annotations": [],
        "grid": {
            "xaxes": [],
            "yaxes": [],
            "xgap": gap,
            "ygap": gap,
            "xside": "bottom",
            "yside": "left",
        },
    }
    for letter in ["x", "y"]:
        for letter_number in [t[letter + "axis"] for t in fig.data]:
            if letter_number not in layout["grid"][letter + "axes"]:
                layout["grid"][letter + "axes"].append(letter_number)
                axis = letter_number.replace(letter, letter + "axis")
                layout[axis] = {}
                if len(letter_number) > 1:
                    layout[axis]["scaleanchor"] = letter + "1"
                layout[axis]["title"] = args[letter]
                if args[letter] in orders:
                    layout[axis]["categoryorder"] = "array"
                    layout[axis]["categoryarray"] = (
                        orders[args[letter]]
                        if letter == "x"
                        else list(reversed(orders[args[letter]]))
                    )
                if args["log_" + letter]:
                    layout[axis]["type"] = "log"

    for letter, direction, row in (("x", "col", False), ("y", "row", True)):
        if args[direction]:
            step = 1.0 / (len(layout["grid"][letter + "axes"]) - gap)
            for key, value in axes[letter].items():
                i = int(value[1:])
                if row:
                    i = len(layout["grid"][letter + "axes"]) - i
                else:
                    i -= 1
                layout["annotations"].append(
                    {
                        "xref": "paper",
                        "yref": "paper",
                        "showarrow": False,
                        "xanchor": "center",
                        "yanchor": "middle",
                        "text": args[direction] + "=" + str(key),
                        "x": 1.01 if row else step * (i + (0.5 - gap / 2)),
                        "y": step * (i + (0.5 - gap / 2)) if row else 1.02,
                        "textangle": 90 if row else 0,
                    }
                )
    return dict(layout=layout)


def configure_ternary_axes(args, fig, axes, orders):
    return dict(
        layout=dict(
            ternary=dict(
                aaxis=dict(title=args["a"]),
                baxis=dict(title=args["b"]),
                caxis=dict(title=args["c"]),
            )
        )
    )


def configure_polar_axes(args, fig, axes, orders):
    patch = dict(
        layout=dict(
            polar=dict(
                angularaxis=dict(
                    direction=args["direction"], rotation=args["startangle"]
                ),
                radialaxis=dict(),
            )
        )
    )
    for var, axis in [("r", "radialaxis"), ("theta", "angularaxis")]:
        if args[var] in orders:
            patch["layout"]["polar"][axis]["categoryorder"] = "array"
            patch["layout"]["polar"][axis]["categoryarray"] = orders[args[var]]

    return patch


def configure_3d_axes(args, fig, axes, orders):
    patch = dict(
        layout=dict(
            scene=dict(
                xaxis=dict(title=args["x"]),
                yaxis=dict(title=args["y"]),
                zaxis=dict(title=args["z"]),
            )
        )
    )
    for letter in ["x", "y", "z"]:
        if args[letter] in orders:
            patch["layout"]["scene"][letter]["categoryorder"] = "array"
            patch["layout"]["scene"][letter]["categoryarray"] = orders[args[letter]]
    return patch


def configure_mapbox(args, fig, axes, orders):
    return dict(
        layout=dict(
            mapbox=dict(
                accesstoken=MAPBOX_TOKEN,
                center=dict(
                    lat=args["df"][args["lat"]].mean(),
                    lon=args["df"][args["lon"]].mean(),
                ),
                zoom=args["zoom"]
                or abs(args["df"][args["lat"]].max() - args["df"][args["lat"]].min())
                * 50,
            )
        )
    )


def configure_geo(args, fig, axes, orders):
    return dict(layout=dict(geo=dict(projection=dict(type="robinson"))))


def make_trace_spec(args, constructor, vars, trace_patch):
    result = [TraceSpec(constructor, vars, trace_patch)]
    for letter in ["x", "y"]:
        if "marginal_" + letter in args and args["marginal_" + letter]:
            trace_spec = None
            axis_map = dict(
                xaxis="x1" if letter == "x" else "x2",
                yaxis="y1" if letter == "y" else "y2",
            )
            if args["marginal_" + letter] == "histogram":
                trace_spec = TraceSpec(
                    constructor=go.Histogram,
                    vars=[letter],
                    trace_patch=dict(opacity=0.5, **axis_map),
                )
            elif args["marginal_" + letter] == "violin":
                trace_spec = TraceSpec(
                    constructor=go.Violin, vars=[letter], trace_patch=axis_map
                )
            elif args["marginal_" + letter] == "box":
                trace_spec = TraceSpec(
                    constructor=go.Box,
                    vars=[letter],
                    trace_patch=dict(notched=True, **axis_map),
                )
            elif args["marginal_" + letter] == "rug":
                trace_spec = TraceSpec(
                    constructor=go.Box,
                    vars=[letter],
                    trace_patch=dict(
                        fillcolor="rgba(255,255,255,0)",
                        line={"color": "rgba(255,255,255,0)"},
                        boxpoints="all",
                        jitter=0,
                        hoveron="points",
                        marker={
                            "symbol": "line-ew-open"
                            if letter == "y"
                            else "line-ns-open"
                        },
                        **axis_map
                    ),
                )
            result.append(trace_spec)
    return result


def one_group(x):
    return ""


available_vars = (
    ["x", "y", "z", "a", "b", "c", "r", "theta", "lat", "lon", "locations"]
    + ["dimensions", "hover", "size", "text", "error_x", "error_x_minus"]
    + ["error_y", "error_y_minus", "error_z", "error_z_minus"]
)


def make_figure(
    args, constructor, vars=None, grouped_mappings=[], trace_patch={}, layout_patch={}
):
    sizeref = 0
    if "size" in args and args["size"]:
        sizeref = args["df"][args["size"]].max() / (args["max_size"] * args["max_size"])

    if vars is None:
        vars = [k for k in available_vars if k in args]

    grouped_mappings = [make_mapping(args, g) for g in grouped_mappings]
    grouper = [x.grouper or one_group for x in grouped_mappings] or [one_group]
    grouped = args["df"].groupby(grouper, sort=False)
    orders = args["orders"].copy()
    group_names = []
    for group_name in grouped.groups:
        if len(grouper) == 1:
            group_name = (group_name,)
        group_names.append(group_name)
        for col, val in zip(grouper, group_name):
            if col not in orders:
                orders[col] = []
            if val not in orders[col]:
                orders[col].append(val)

    for i, col in reversed(list(enumerate(grouper))):
        if col != one_group:
            group_names = sorted(
                group_names,
                key=lambda g: orders[col].index(g[i]) if g[i] in orders[col] else -1,
            )

    trace_names = set()
    traces = []
    trace_specs = make_trace_spec(args, constructor, vars, trace_patch)
    for group_name in group_names:
        group = grouped.get_group(group_name if len(group_name) > 1 else group_name[0])
        mapping_labels = []
        for col, val, m in zip(grouper, group_name, grouped_mappings):
            if col != one_group:
                s = ("%s=%s" % (col, val), m.show_in_trace_name)
                if s not in mapping_labels:
                    mapping_labels.append(s)
        trace_name = ", ".join(s for s, t in mapping_labels if t)

        for trace_spec in trace_specs:
            trace = trace_spec.constructor(
                name=trace_name,
                legendgroup=trace_name,
                showlegend=(trace_name != "" and trace_name not in trace_names),
            )
            trace_names.add(trace_name)
            for i, m in enumerate(grouped_mappings):
                val = group_name[i]
                if val not in m.val_map:
                    m.val_map[val] = m.sequence[len(m.val_map) % len(m.sequence)]
                try:
                    m.updater(trace, m.val_map[val])
                except ValueError:
                    if (
                        len(trace_specs) == 1
                        or trace_specs[0].constructor != go.Scatter
                        or m.variable != "symbol"
                    ):
                        raise
            trace.update(
                make_trace_kwargs(args, trace_spec, group, mapping_labels, sizeref)
            )
            traces.append(trace)

    fig = FigurePx(data=traces, layout=layout_patch)
    axes = {m.variable: m.val_map for m in grouped_mappings}
    configure_axes(args, constructor, fig, axes, orders)
    return fig


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
    color_sequence=default_color_seq,
    symbol_sequence=default_symbol_seq,
    row=None,
    col=None,
    log_x=False,
    log_y=False,
    marginal_x=None,
    marginal_y=None,
    error_x=None,
    error_x_minus=None,
    error_y=None,
    error_y_minus=None,
    max_size=default_max_size,
    orders={},
):
    return make_figure(
        args=locals(),
        constructor=go.Scatter,
        trace_patch=dict(mode="markers" + ("+text" if text else "")),
        grouped_mappings=["col", "row", "marker.color", "marker.symbol"],
        layout_patch=dict(barmode="overlay", violinmode="overlay"),  # for marginals
    )


def density_heatmap(
    df,
    x=None,
    y=None,
    row=None,
    col=None,
    log_x=False,
    log_y=False,
    marginal_x=None,
    marginal_y=None,
    orders={},
):
    return make_figure(
        args=locals(),
        constructor=go.Histogram2d,
        grouped_mappings=["col", "row"],
        layout_patch=dict(barmode="overlay", violinmode="overlay"),  # for marginals
    )


def density_contour(
    df,
    x=None,
    y=None,
    color=None,
    color_map={},
    color_sequence=default_color_seq,
    row=None,
    col=None,
    log_x=False,
    log_y=False,
    marginal_x=None,
    marginal_y=None,
    orders={},
):
    return make_figure(
        args=locals(),
        constructor=go.Histogram2dContour,
        trace_patch=dict(contours=dict(coloring="none")),
        grouped_mappings=["col", "row", "line.color"],
        layout_patch=dict(barmode="overlay", violinmode="overlay"),  # for marginals
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
    color_sequence=default_color_seq,
    dash_sequence=default_dash_seq,
    row=None,
    col=None,
    log_x=False,
    log_y=False,
    error_x=None,
    error_x_minus=None,
    error_y=None,
    error_y_minus=None,
    orders={},
):
    return make_figure(
        args=locals(),
        constructor=go.Scatter,
        trace_patch=dict(mode="lines" + ("+markers+text" if text else "")),
        grouped_mappings=["col", "row", "line.color", "line.dash", "split"],
    )


def bar(
    df,
    x=None,
    y=None,
    color=None,
    color_map={},
    color_sequence=default_color_seq,
    row=None,
    col=None,
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
):
    return make_figure(
        args=locals(),
        constructor=go.Bar,
        trace_patch=dict(orientation=orientation, textposition="auto"),
        grouped_mappings=["col", "row", "marker.color"],
        layout_patch=dict(barnorm=normalization, barmode=mode),
    )


def histogram(
    df,
    x=None,
    y=None,
    color=None,
    color_map={},
    color_sequence=default_color_seq,
    row=None,
    col=None,
    orientation="v",
    mode="stack",
    normalization=None,
    log_x=False,
    log_y=False,
    orders={},
):
    return make_figure(
        args=locals(),
        constructor=go.Histogram,
        trace_patch=dict(orientation=orientation, histnorm=normalization),
        grouped_mappings=["col", "row", "marker.color"],
        layout_patch=dict(barmode=mode),
    )


def violin(
    df,
    x=None,
    y=None,
    color=None,
    color_map={},
    color_sequence=default_color_seq,
    orientation="v",
    mode="group",
    row=None,
    col=None,
    log_x=False,
    log_y=False,
    orders={},
):
    return make_figure(
        args=locals(),
        constructor=go.Violin,
        trace_patch=dict(orientation=orientation),
        grouped_mappings=["col", "row", "marker.color"],
        layout_patch=dict(violinmode=mode),
    )


def box(
    df,
    x=None,
    y=None,
    color=None,
    color_map={},
    color_sequence=default_color_seq,
    orientation="v",
    mode="group",
    row=None,
    col=None,
    log_x=False,
    log_y=False,
    orders={},
):
    return make_figure(
        args=locals(),
        constructor=go.Box,
        trace_patch=dict(orientation=orientation),
        grouped_mappings=["col", "row", "marker.color"],
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
    color_sequence=default_color_seq,
    symbol_sequence=default_symbol_seq,
    error_x=None,
    error_x_minus=None,
    error_y=None,
    error_y_minus=None,
    error_z=None,
    error_z_minus=None,
    max_size=default_max_size,
    orders={},
):
    return make_figure(
        args=locals(),
        constructor=go.Scatter3d,
        trace_patch=dict(mode="markers" + ("+text" if text else "")),
        grouped_mappings=["marker.color", "marker.symbol"],
    )


def line_3d(
    df,
    x=None,
    y=None,
    z=None,
    color=None,
    dash=None,
    text=None,
    color_map={},
    dash_map={},
    hover=None,
    color_sequence=default_color_seq,
    dash_sequence=default_dash_seq,
    error_x=None,
    error_x_minus=None,
    error_y=None,
    error_y_minus=None,
    error_z=None,
    error_z_minus=None,
    orders={},
):
    return make_figure(
        args=locals(),
        constructor=go.Scatter3d,
        trace_patch=dict(mode="lines" + ("+markers+text" if text else "")),
        grouped_mappings=["line.color", "line.dash"],
    )


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
    color_sequence=default_color_seq,
    symbol_sequence=default_symbol_seq,
    max_size=default_max_size,
    orders={},
):
    return make_figure(
        args=locals(),
        constructor=go.Scatterternary,
        trace_patch=dict(mode="markers" + ("+text" if text else "")),
        grouped_mappings=["marker.color", "marker.symbol"],
    )


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
    color_sequence=default_color_seq,
    dash_sequence=default_dash_seq,
    orders={},
):
    return make_figure(
        args=locals(),
        constructor=go.Scatterternary,
        trace_patch=dict(mode="lines" + ("+markers+text" if text else "")),
        grouped_mappings=["marker.color", "line.dash", "split"],
    )


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
    color_sequence=default_color_seq,
    symbol_sequence=default_symbol_seq,
    direction="clockwise",
    startangle=90,
    max_size=default_max_size,
    orders={},
):
    return make_figure(
        args=locals(),
        constructor=go.Scatterpolar,
        trace_patch=dict(mode="markers" + ("+text" if text else "")),
        grouped_mappings=["marker.color", "marker.symbol"],
    )


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
    color_sequence=default_color_seq,
    dash_sequence=default_dash_seq,
    direction="clockwise",
    startangle=90,
    close_lines=False,
    orders={},
):
    return make_figure(
        args=locals(),
        constructor=go.Scatterpolar,
        trace_patch=dict(mode="lines" + ("+markers+text" if text else "")),
        grouped_mappings=["marker.color", "line.dash", "split"],
    )


def bar_polar(
    df,
    r=None,
    theta=None,
    color=None,
    hover=None,
    color_map={},
    color_sequence=default_color_seq,
    normalization="",
    mode="relative",
    direction="clockwise",
    startangle=90,
    orders={},
):
    return make_figure(
        args=locals(),
        constructor=go.Barpolar,
        grouped_mappings=["marker.color"],
        layout_patch=dict(barnorm=normalization, barmode=mode),
    )


def choropleth(
    df,
    lat=None,
    lon=None,
    locations=None,
    z=None,
    text=None,
    hover=None,
    color_map={},
    color_sequence=default_color_seq,
    size=None,
    max_size=default_max_size,
    orders={},
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
    color_sequence=default_color_seq,
    size=None,
    max_size=default_max_size,
    orders={},
):
    return make_figure(
        args=locals(),
        constructor=go.Scattergeo,
        trace_patch=dict(mode="markers" + ("+text" if text else "")),
        grouped_mappings=["marker.color"],
    )


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
    color_sequence=default_color_seq,
    dash_map={},
    dash_sequence=default_dash_seq,
    orders={},
):
    return make_figure(
        args=locals(),
        constructor=go.Scattergeo,
        trace_patch=dict(mode="lines" + ("+markers+text" if text else "")),
        grouped_mappings=["line.color", "line.dash", "split"],
    )


def scatter_mapbox(
    df,
    lat=None,
    lon=None,
    color=None,
    text=None,
    hover=None,
    color_map={},
    color_sequence=default_color_seq,
    size=None,
    max_size=default_max_size,
    zoom=None,
    orders={},
):
    return make_figure(
        args=locals(),
        constructor=go.Scattermapbox,
        trace_patch=dict(mode="markers" + ("+text" if text else "")),
        grouped_mappings=["marker.color"],
    )


def line_mapbox(
    df,
    lat=None,
    lon=None,
    color=None,
    text=None,
    hover=None,
    split=None,
    color_map={},
    color_sequence=default_color_seq,
    zoom=None,
    orders={},
):
    return make_figure(
        args=locals(),
        constructor=go.Scattermapbox,
        trace_patch=dict(mode="lines" + ("+markers+text" if text else "")),
        grouped_mappings=["line.color", "split"],
    )


def splom(
    df,
    dimensions=None,
    color=None,
    symbol=None,
    color_map={},
    symbol_map={},
    color_sequence=default_color_seq,
    symbol_sequence=default_symbol_seq,
    orders={},
):
    return make_figure(
        args=locals(),
        constructor=go.Splom,
        grouped_mappings=["marker.color", "marker.symbol"],
    )


# TODO continuous color
# TODO parcoords, parcats
# TODO animations
# TODO geo locationmode, projection, etc
# TODO choropleth z vs color
# TODO choropleth has no hovertext?
# TODO 1.44.0 hover templates
# TODO max_size makes no sense?
# TODO regression lines
# TODO secondary Y axis
# TODO histogram weights and calcs
# TODO various box and violin options
# TODO check on dates
# TODO facet wrap
# TODO non-cartesian faceting
# TODO testing of some kind (try Percy)
# TODO gl vs not gl
# TODO validate inputs
# TODO opacity
# TODO color splits in densities
# TODO groupby ignores NaN ... ?
# TODO suppress plotly.py errors... don't show our programming errors?
# TODO optional widget mode
# TODO missing values
# TODO warnings
# TODO maximum number of categories ... what does Seaborn do when too many colors?
