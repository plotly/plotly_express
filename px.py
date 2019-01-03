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
        if not FigurePx.offline_initialized:
            init_notebook_mode()
            FigurePx.offline_initialized = True

    def _ipython_display_(self):
        iplot(self, show_link=False)


default_color_seq = ["#636efa", "#EF553B", "#00cc96", "#ab63fa", "#19d3f3", "#e763fa"]
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


def trace_kwargs_setter(vars, args, **kwargs):
    if "size" in vars and args["size"]:
        sizeref = args["df"][args["size"]].max() / (30 * 30)

    def setter(g):
        result = kwargs or {}
        for k in vars:
            v = args[k]
            if v:
                if k == "size":
                    result["marker"] = dict(size=g[v], sizemode="area", sizeref=sizeref)
                elif k.startswith("error"):
                    error_xy = k[:7]
                    arr = "arrayminus" if k.endswith("minus") else "array"
                    if error_xy not in result:
                        result[error_xy] = {}
                    result[error_xy][arr] = g[v]
                elif k == "hover":
                    result["hovertext"] = g[v]
                else:
                    result[k] = g[v]
        return result

    return setter


def make_cartesian_axes_configurator(args):
    def configure_cartesian_axes(fig, axes):
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
            "grid": {
                "xaxes": [],
                "yaxes": [],
                "xgap": gap,
                "ygap": gap,
                "xside": "bottom",
                "yside": "left",
            }
        }
        for letter in ["x", "y"]:
            for letter_number in set(t[letter + "axis"] for t in fig.data):
                if letter_number not in layout["grid"][letter + "axes"]:
                    layout["grid"][letter + "axes"].append(letter_number)
                    axis = letter_number.replace(letter, letter + "axis")
                    layout[axis] = {}
                    if len(letter_number) > 1:
                        layout[axis]["scaleanchor"] = letter + "1"
                    layout[axis]["title"] = args[letter]
                    if args["log_" + letter]:
                        layout[axis]["type"] = "log"
        layout["grid"]["yaxes"] = [i for i in reversed(layout["grid"]["yaxes"])]

        layout["annotations"] = []
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
    def configure_ternary_axes(fig, axes):
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


def make_3d_axes_configurator(args):
    def configure_ternary_axes(fig, axes):
        return dict(
            layout=dict(
                scene=dict(
                    xaxis=dict(title=args["x"]),
                    yaxis=dict(title=args["y"]),
                    zaxis=dict(title=args["z"]),
                )
            )
        )

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
    df, constructors, mappings=[], axis_configurator=lambda x, y: {}, layout_patch={}
):
    fig = FigurePx()

    def one_group(x):
        return ""

    grouper = [x.grouper or one_group for x in mappings] or [one_group]
    trace_names = set()
    traces = []
    for group_name, group in df.groupby(grouper):
        if len(grouper) == 1:
            group_name = [group_name]
        mapping_str = []
        for col, val, m in zip(grouper, group_name, mappings):
            if col != one_group and m.show_in_trace_name:
                s = "%s=%s" % (col, val)
                if s not in mapping_str:
                    mapping_str.append(s)
        trace_name = ", ".join(mapping_str)

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
                except Exception:
                    if (
                        len(constructors) != 1
                        or constructors[0][0] != go.Scatter
                        or m.variable != "symbol"
                    ):
                        raise
            trace.update(trace_kwargs_by_group(group))
            traces.append(trace)
    fig.add_traces(traces)
    fig.update(axis_configurator(fig, {m.variable: m.val_map for m in mappings}))
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
):
    args = locals()
    return make_figure(
        df,
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
):
    args = locals()
    return make_figure(
        df,
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
):
    args = locals()
    return make_figure(
        df,
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
):
    args = locals()
    return make_figure(
        df,
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
    mode="relative",
    log_x=False,
    log_y=False,
    error_x=None,
    error_x_minus=None,
    error_y=None,
    error_y_minus=None,
):
    args = locals()
    return make_figure(
        df,
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
):
    args = locals()
    return make_figure(
        df,
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
):
    args = locals()
    return make_figure(
        df,
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
):
    args = locals()
    return make_figure(
        df,
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
):
    args = locals()
    return make_figure(
        df,
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
):
    args = locals()
    return make_figure(
        df,
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
):
    args = locals()
    return make_figure(
        df,
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
):
    args = locals()
    return make_figure(
        df,
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
):
    args = locals()
    return make_figure(
        df,
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
):
    args = locals()
    return make_figure(
        df,
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
):
    args = locals()
    return make_figure(
        df,
        [(go.Barpolar, trace_kwargs_setter(["r", "theta", "hover"], args))],
        [make_mapping("color", "marker", args)],
        lambda x, y: {},
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
):
    args = locals()
    return make_figure(
        df,
        [
            (
                go.Splom,
                lambda g: dict(
                    dimensions=[
                        dict(label=name, values=column.values)
                        for name, column in g.iteritems()
                        if (not dimensions) or (name in dimensions)
                    ]
                ),
            )
        ],
        [make_mapping("color", "marker", args), make_mapping("symbol", "marker", args)],
    )


# TODO symbol in line ?
# TODO testing of some kind (try Percy)
# TODO gl vs not gl
# TODO lock ranges on shared axes, including colormap ... shared colormap?
# TODO histogram weights and calcs
# TODO various box and violin options
# TODO check on dates
# TODO facet wrap
# TODO non-cartesian faceting
# TODO validate inputs
# TODO name / hover labels
# TODO opacity
# TODO continuous color
# TODO color splits in densities
# TODO groupby ignores NaN ... ?
# TODO suppress plotly.py errors... don't show our programming errors?
# TODO parcoords, parcats
# TODO optional widget mode
