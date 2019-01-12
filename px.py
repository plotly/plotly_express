import plotly.graph_objs as go
from plotly.offline import init_notebook_mode, iplot
from collections import namedtuple
import plotly.io as pio


pio.templates["px"] = dict(
    layout=dict(margin={"t": 60}, height=600, legend={"tracegroupgap": 0})
)


class FigurePx(go.Figure):
    offline_initialized = False

    def __init__(self, *args, **kwargs):
        super(FigurePx, self).__init__(
            *args, layout={"template": "plotly+px"}, **kwargs
        )

    def _ipython_display_(self):
        if not FigurePx.offline_initialized:
            init_notebook_mode()
            FigurePx.offline_initialized = True
        iplot(self, show_link=False)


default_max_size = 20
default_color_seq = [
    "#636efa",
    "#EF553B",
    "#00cc96",
    "#ab63fa",
    "#19d3f3",
    "#e763fa",
    "#fecb52",
    "#ffa15a",
    "#ff6692",
    "#b6e880",
]
default_symbol_seq = ["circle", "diamond", "square", "x", "cross"]
default_dash_seq = ["solid", "dot", "dash", "longdash", "dashdot", "longdashdot"]
Mapping = namedtuple(
    "Mapping",
    ["show_in_trace_name", "grouper", "val_map", "sequence", "updater", "variable"],
)


def make_mapping(variable, parent, args):
    return Mapping(
        show_in_trace_name=True,
        variable=variable,
        grouper=args[variable],
        val_map=args[variable + "_map"].copy(),
        sequence=args[variable + "_sequence"],
        updater=lambda trace, v: trace.update({parent: {variable: v}}),
    )


def make_cartesian_facet_mapping(letter, column):
    return Mapping(
        show_in_trace_name=False,
        variable=letter,
        grouper=column,
        val_map={},
        sequence=[letter + str(i) for i in range(1, 1000)],
        updater=lambda trace, v: trace.update({letter + "axis": v}),
    )


def trace_kwargs_setter(vars, args, hovertemplate=False, **kwargs):
    if "size" in vars and args["size"]:
        sizeref = args["df"][args["size"]].max() / (args["max_size"] * args["max_size"])

    def setter(g, mapping_labels):
        if "close_lines" in args and args["close_lines"]:
            g = g.append(g.iloc[0])
        result = kwargs or {}
        hover_header = ""
        for k in vars:
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
        if hovertemplate:
            result["hovertemplate"] = hover_header + (
                "<br>".join(s for s, t in mapping_labels) + "<extra></extra>"
            )
        return result

    return setter


def make_cartesian_axes_configurator(args):
    def configure_cartesian_axes(fig, axes, orders):
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

    return configure_cartesian_axes


def make_ternary_axes_configurator(args):
    def configure_ternary_axes(fig, axes, orders):
        return dict(
            layout=dict(
                ternary=dict(
                    aaxis=dict(title=args["a"]),
                    baxis=dict(title=args["b"]),
                    caxis=dict(title=args["c"]),
                )
            )
        )

    return configure_ternary_axes


def make_polar_axes_configurator(args):
    def configure_polar_axes(fig, axes, orders):
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

    return configure_polar_axes


def make_3d_axes_configurator(args):
    def configure_ternary_axes(fig, axes, orders):
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

    return configure_ternary_axes


def make_marginals_definition(letter, args):
    axis_map = dict(
        xaxis="x1" if letter == "x" else "x2", yaxis="y1" if letter == "y" else "y2"
    )
    if args["marginal_" + letter] == "histogram":
        return (
            go.Histogram,
            trace_kwargs_setter([letter], args, opacity=0.5, **axis_map),
        )
    if args["marginal_" + letter] == "violin":
        return (go.Violin, trace_kwargs_setter([letter], args, **axis_map))
    if args["marginal_" + letter] == "box":
        return (go.Box, trace_kwargs_setter([letter], args, notched=True, **axis_map))
    if args["marginal_" + letter] == "rug":
        return (
            go.Box,
            trace_kwargs_setter(
                [letter],
                args,
                fillcolor="rgba(255,255,255,0)",
                line={"color": "rgba(255,255,255,0)"},
                boxpoints="all",
                jitter=0,
                hoveron="points",
                marker={"symbol": "line-ew-open" if letter == "y" else "line-ns-open"},
                **axis_map
            ),
        )
    return (None, None)


##########################################
# MAKE_FIGURE
##########################################


def make_figure(
    df,
    args,
    constructors,
    mappings=[],
    axis_configurator=lambda x, y, z: {},
    layout_patch={},
):
    fig = FigurePx()

    def one_group(x):
        return ""

    grouper = [x.grouper or one_group for x in mappings] or [one_group]
    trace_names = set()
    traces = []
    grouped = df.groupby(grouper, sort=False)
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

    for group_name in group_names:
        group = grouped.get_group(group_name if len(group_name) > 1 else group_name[0])
        mapping_labels = []
        for col, val, m in zip(grouper, group_name, mappings):
            if col != one_group:
                s = ("%s=%s" % (col, val), m.show_in_trace_name)
                if s not in mapping_labels:
                    mapping_labels.append(s)
        trace_name = ", ".join(s for s, t in mapping_labels if t)

        for constructor, trace_kwargs_by_group in constructors:
            if not constructor:
                continue
            trace = constructor(
                name=trace_name,
                legendgroup=trace_name,
                showlegend=(trace_name != "" and trace_name not in trace_names),
            )
            trace_names.add(trace_name)
            for i, m in enumerate(mappings):
                val = group_name[i]
                if val not in m.val_map:
                    m.val_map[val] = m.sequence[len(m.val_map) % len(m.sequence)]
                try:
                    m.updater(trace, m.val_map[val])
                except ValueError:
                    if (
                        len(constructors) == 1
                        or constructors[0][0] != go.Scatter
                        or m.variable != "symbol"
                    ):
                        raise
            trace.update(trace_kwargs_by_group(group, mapping_labels))
            traces.append(trace)
    fig.add_traces(traces)
    fig.update(
        axis_configurator(fig, {m.variable: m.val_map for m in mappings}, orders)
    )
    fig.layout.update(layout_patch)
    return fig


##########################################
# PLOT TYPES
##########################################


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
    args = locals()
    return make_figure(
        df,
        args,
        [
            (
                go.Scatter,
                trace_kwargs_setter(
                    [
                        "x",
                        "y",
                        "hover",
                        "size",
                        "text",
                        "error_x",
                        "error_x_minus",
                        "error_y",
                        "error_y_minus",
                    ],
                    args,
                    hovertemplate=True,
                    mode="markers" + ("+text" if text else ""),
                ),
            ),
            make_marginals_definition("y", args),
            make_marginals_definition("x", args),
        ],
        [
            make_cartesian_facet_mapping("x", col),
            make_cartesian_facet_mapping("y", row),
            make_mapping("color", "marker", args),
            make_mapping("symbol", "marker", args),
        ],
        make_cartesian_axes_configurator(args),
        dict(barmode="overlay", violinmode="overlay"),  # for marginals
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
    args = locals()
    return make_figure(
        df,
        args,
        [
            (go.Histogram2d, trace_kwargs_setter(["x", "y"], args)),
            make_marginals_definition("y", args),
            make_marginals_definition("x", args),
        ],
        [
            make_cartesian_facet_mapping("x", col),
            make_cartesian_facet_mapping("y", row),
        ],
        make_cartesian_axes_configurator(args),
        dict(barmode="overlay", violinmode="overlay"),  # for marginals
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
    args = locals()
    return make_figure(
        df,
        args,
        [
            (
                go.Histogram2dContour,
                trace_kwargs_setter(["x", "y"], args, contours=dict(coloring="none")),
            ),
            make_marginals_definition("y", args),
            make_marginals_definition("x", args),
        ],
        [
            make_cartesian_facet_mapping("x", col),
            make_cartesian_facet_mapping("y", row),
            make_mapping("color", "line", args),
        ],
        make_cartesian_axes_configurator(args),
        dict(barmode="overlay", violinmode="overlay"),  # for marginals
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
    args = locals()
    return make_figure(
        df,
        args,
        [
            (
                go.Scatter,
                trace_kwargs_setter(
                    [
                        "x",
                        "y",
                        "hover",
                        "text",
                        "error_x",
                        "error_x_minus",
                        "error_y",
                        "error_y_minus",
                    ],
                    args,
                    hovertemplate=True,
                    mode="lines" + ("+markers+text" if text else ""),
                ),
            )
        ],
        [
            make_cartesian_facet_mapping("x", col),
            make_cartesian_facet_mapping("y", row),
            make_mapping("color", "line", args),
            make_mapping("dash", "line", args),
            Mapping(
                show_in_trace_name=False,
                grouper=split,
                val_map={},
                sequence=[""],
                variable="split",
                updater=(lambda trace, v: v),
            ),
        ],
        make_cartesian_axes_configurator(args),
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
    args = locals()
    return make_figure(
        df,
        args,
        [
            (
                go.Bar,
                trace_kwargs_setter(
                    [
                        "x",
                        "y",
                        "hover",
                        "text",
                        "error_x",
                        "error_x_minus",
                        "error_y",
                        "error_y_minus",
                    ],
                    args,
                    hovertemplate=True,
                    orientation=orientation,
                    textposition="auto",
                ),
            )
        ],
        [
            make_cartesian_facet_mapping("x", col),
            make_cartesian_facet_mapping("y", row),
            make_mapping("color", "marker", args),
        ],
        make_cartesian_axes_configurator(args),
        dict(barnorm=normalization, barmode=mode),
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
    args = locals()
    return make_figure(
        df,
        args,
        [
            (
                go.Histogram,
                trace_kwargs_setter(
                    ["x", "y"], args, orientation=orientation, histnorm=normalization
                ),
            )
        ],
        [
            make_cartesian_facet_mapping("x", col),
            make_cartesian_facet_mapping("y", row),
            make_mapping("color", "marker", args),
        ],
        make_cartesian_axes_configurator(args),
        dict(barmode=mode),
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
    args = locals()
    return make_figure(
        df,
        args,
        [(go.Violin, trace_kwargs_setter(["x", "y"], args, orientation=orientation))],
        [
            make_cartesian_facet_mapping("x", col),
            make_cartesian_facet_mapping("y", row),
            make_mapping("color", "marker", args),
        ],
        make_cartesian_axes_configurator(args),
        dict(violinmode=mode),
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
    args = locals()
    return make_figure(
        df,
        args,
        [(go.Box, trace_kwargs_setter(["x", "y"], args, orientation=orientation))],
        [
            make_cartesian_facet_mapping("x", col),
            make_cartesian_facet_mapping("y", row),
            make_mapping("color", "marker", args),
        ],
        make_cartesian_axes_configurator(args),
        dict(boxmode=mode),
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
    args = locals()
    return make_figure(
        df,
        args,
        [
            (
                go.Scatter3d,
                trace_kwargs_setter(
                    [
                        "x",
                        "y",
                        "z",
                        "hover",
                        "text",
                        "size",
                        "error_x",
                        "error_x_minus",
                        "error_y",
                        "error_y_minus",
                        "error_z",
                        "error_z_minus",
                    ],
                    args,
                    mode="markers" + ("+text" if text else ""),
                ),
            )
        ],
        [make_mapping("color", "marker", args), make_mapping("symbol", "marker", args)],
        make_3d_axes_configurator(args),
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
    args = locals()
    return make_figure(
        df,
        args,
        [
            (
                go.Scatter3d,
                trace_kwargs_setter(
                    [
                        "x",
                        "y",
                        "z",
                        "hover",
                        "text",
                        "error_x",
                        "error_x_minus",
                        "error_y",
                        "error_y_minus",
                        "error_z",
                        "error_z_minus",
                    ],
                    args,
                    mode="lines" + ("+markers+text" if text else ""),
                ),
            )
        ],
        [make_mapping("color", "line", args), make_mapping("dash", "line", args)],
        make_3d_axes_configurator(args),
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
    args = locals()
    return make_figure(
        df,
        args,
        [
            (
                go.Scatterternary,
                trace_kwargs_setter(
                    ["a", "b", "c", "hover", "text", "size"],
                    args,
                    mode="markers" + ("+text" if text else ""),
                ),
            )
        ],
        [make_mapping("color", "marker", args), make_mapping("symbol", "marker", args)],
        make_ternary_axes_configurator(args),
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
    args = locals()
    return make_figure(
        df,
        args,
        [
            (
                go.Scatterternary,
                trace_kwargs_setter(
                    ["a", "b", "c", "hover", "text"],
                    args,
                    mode="lines" + ("+markers+text" if text else ""),
                ),
            )
        ],
        [
            make_mapping("color", "marker", args),
            make_mapping("dash", "line", args),
            Mapping(
                show_in_trace_name=False,
                grouper=split,
                val_map={},
                sequence=[""],
                variable="split",
                updater=(lambda trace, v: v),
            ),
        ],
        make_ternary_axes_configurator(args),
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
    args = locals()
    return make_figure(
        df,
        args,
        [
            (
                go.Scatterpolar,
                trace_kwargs_setter(
                    ["r", "theta", "hover", "size", "text"],
                    args,
                    mode="markers" + ("+text" if text else ""),
                ),
            )
        ],
        [make_mapping("color", "marker", args), make_mapping("symbol", "marker", args)],
        make_polar_axes_configurator(args),
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
    args = locals()
    return make_figure(
        df,
        args,
        [
            (
                go.Scatterpolar,
                trace_kwargs_setter(
                    ["r", "theta", "hover", "text"],
                    args,
                    mode="lines" + ("+markers+text" if text else ""),
                ),
            )
        ],
        [
            make_mapping("color", "marker", args),
            make_mapping("dash", "line", args),
            Mapping(
                show_in_trace_name=False,
                grouper=split,
                val_map={},
                sequence=[""],
                variable="split",
                updater=(lambda trace, v: v),
            ),
        ],
        make_polar_axes_configurator(args),
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
    args = locals()
    return make_figure(
        df,
        args,
        [(go.Barpolar, trace_kwargs_setter(["r", "theta", "hover"], args))],
        [make_mapping("color", "marker", args)],
        make_polar_axes_configurator(args),
        dict(barnorm=normalization, barmode=mode),
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
    args = locals()
    return make_figure(
        df,
        args,
        [(go.Splom, trace_kwargs_setter(["dimensions"], args))],
        [make_mapping("color", "marker", args), make_mapping("symbol", "marker", args)],
    )


# TODO extend the palette
# TODO animations!!!
# TODO histogram weights and calcs
# TODO various box and violin options
# TODO check on dates
# TODO continuous color
# TODO parcoords, parcats
# TODO facet wrap
# TODO non-cartesian faceting
# TODO testing of some kind (try Percy)
# TODO gl vs not gl
# TODO lock ranges on shared axes, including colormap ... shared colormap?
# TODO validate inputs
# TODO opacity
# TODO color splits in densities
# TODO groupby ignores NaN ... ?
# TODO suppress plotly.py errors... don't show our programming errors?
# TODO optional widget mode
# TODO missing values
# TODO warnings
# TODO maximum number of categories ... what does Seaborn do when too many colors?

# TODO grid react bugs
