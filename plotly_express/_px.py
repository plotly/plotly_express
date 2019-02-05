import plotly.graph_objs as go
from plotly.offline import init_notebook_mode, iplot
from collections import namedtuple
import plotly.io as pio
from .colors.qualitative import Plotly as default_qualitative_seq
from .colors.sequential import Plotly as default_sequential_seq


MAPBOX_TOKEN = ""


def set_mapbox_access_token(token):
    global MAPBOX_TOKEN
    MAPBOX_TOKEN = token


pio.templates["px"] = dict(
    layout=dict(margin={"t": 60}, height=600, legend={"tracegroupgap": 0})
)


class FigurePx(go.Figure):
    offline_initialized = False

    def __init__(self, *args, **kwargs):
        super(FigurePx, self).__init__(*args, **kwargs)
        self.update(layout={"template": "plotly+px"})

    def _ipython_display_(self):
        if not FigurePx.offline_initialized:
            init_notebook_mode()
            FigurePx.offline_initialized = True
        iplot(self, show_link=False)


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


def make_trace_kwargs(args, trace_spec, g, mapping_labels, sizeref, color_range):

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
                if ((not v) or (name in v))
                and (
                    trace_spec.constructor != go.Parcoords
                    or args["df"][name].dtype.kind in "bifc"
                )
                and (
                    trace_spec.constructor != go.Parcats
                    or len(args["df"][name].unique()) <= 20
                )
            ]
        elif v:
            if k == "size":
                if "marker" not in result:
                    result["marker"] = dict()
                result["marker"]["size"] = g[v]
                result["marker"]["sizemode"] = "area"
                result["marker"]["sizeref"] = sizeref
                mapping_labels.append(("%s=%%{%s}" % (v, "marker.size"), None))
            elif k.startswith("error"):
                error_xy = k[:7]
                arr = "arrayminus" if k.endswith("minus") else "array"
                if error_xy not in result:
                    result[error_xy] = {}
                result[error_xy][arr] = g[v]
            elif k == "hover":
                if trace_spec.constructor == go.Choropleth:
                    result["text"] = g[v]
                    hover_header = "<b>%{text}</b><br><br>"
                else:
                    result["hovertext"] = g[v]
                    hover_header = "<b>%{hovertext}</b><br><br>"
            elif k == "color":
                colorbar_container = None
                if trace_spec.constructor == go.Choropleth:
                    result["z"] = g[v]
                    colorbar_container = result
                    color_letter = "z"
                    mapping_labels.append(("%s=%%{z}" % (v), None))
                else:
                    colorable = "marker"
                    if trace_spec.constructor in [go.Parcats, go.Parcoords]:
                        colorable = "line"
                    if colorable not in result:
                        result[colorable] = dict()
                    result[colorable]["color"] = g[v]
                    colorbar_container = result[colorable]
                    color_letter = "c"
                    mapping_labels.append(("%s=%%{%s.color}" % (v, colorable), None))
                if color_range is None:
                    colorbar_container["showscale"] = False
                else:
                    colorbar_container["showscale"] = True
                    d = len(args["color_sequence"]) - 1
                    colorbar_container["colorscale"] = [
                        [i / d, x] for i, x in enumerate(args["color_sequence"])
                    ]
                    colorbar_container["colorbar"] = dict(title=v)
                    colorbar_container[color_letter + "min"] = color_range[0]
                    colorbar_container[color_letter + "max"] = color_range[1]
            else:
                result[k] = g[v]
                mapping_labels.append(
                    ("%s=%%{%s}" % (v, k.replace("locations", "location")), None)
                )
    if trace_spec.constructor in [
        go.Scatter,
        go.Bar,
        go.Scatterpolar,
        go.Barpolar,
        go.Scatterternary,
        go.Scattergeo,
        go.Scattermapbox,
        go.Choropleth,
    ]:
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
                zoom=args["zoom"],
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
    ["x", "y", "z", "a", "b", "c", "r", "theta", "color", "size"]
    + ["dimensions", "hover", "text", "error_x", "error_x_minus"]
    + ["error_y", "error_y_minus", "error_z", "error_z_minus"]
    + ["lat", "lon", "locations"]
)


def make_figure(
    args, constructor, vars=None, grouped_mappings=[], trace_patch={}, layout_patch={}
):
    if vars is None:
        vars = [
            k for k in available_vars if k in args and (args[k] or k == "dimensions")
        ]

    sizeref = 0
    if "size" in args and args["size"]:
        sizeref = args["df"][args["size"]].max() / (args["max_size"] * args["max_size"])

    if "color" in args and args["color"]:
        if "line.color" in grouped_mappings or constructor in [
            go.Box,
            go.Violin,
            go.Histogram,
        ]:
            vars.remove("color")
        elif "marker.color" in grouped_mappings:
            if args["df"][args["color"]].dtype.kind in "bifc":
                grouped_mappings.remove("marker.color")
            else:
                vars.remove("color")

    color_range = None
    if "color" in vars:
        if args["color"]:
            color_range = [
                args["df"][args["color"]].min(),
                args["df"][args["color"]].max(),
            ]
        if "color_sequence" in args and not args["color_sequence"]:
            args["color_sequence"] = default_sequential_seq
    else:
        if "color_sequence" in args and not args["color_sequence"]:
            args["color_sequence"] = default_qualitative_seq

    grouped_mappings = [make_mapping(args, g) for g in grouped_mappings]
    grouper = [x.grouper or one_group for x in grouped_mappings] or [one_group]
    grouped = args["df"].groupby(grouper, sort=False)
    orders = {} if "orders" not in args else args["orders"].copy()
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
            trace = trace_spec.constructor(name=trace_name or " ")
            if trace_spec.constructor != go.Parcats:
                trace.update(
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
                make_trace_kwargs(
                    args, trace_spec, group, mapping_labels, sizeref, color_range
                )
            )
            color_range = None
            traces.append(trace)

    fig = FigurePx(data=traces, layout=layout_patch)
    axes = {m.variable: m.val_map for m in grouped_mappings}
    configure_axes(args, constructor, fig, axes, orders)
    return fig


# TODO codegen?
# TODO 3d log scales
# TODO parcoords, parcats orders
# TODO animations
# TODO geo locationmode, projection, etc
# TODO histogram weights and calcs
# TODO various box and violin options
# TODO regression lines
# TODO secondary Y axis
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
