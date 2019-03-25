import plotly.graph_objs as go
from plotly.offline import init_notebook_mode, iplot
from collections import namedtuple, OrderedDict
from .colors.qualitative import Plotly as default_qualitative_seq
import math


MAPBOX_TOKEN = ""


def set_mapbox_access_token(token):
    """
    Arguments:
        token: A Mapbox token to be used in `plotly_express.scatter_mapbox` and \
        `plotly_express.line_mapbox` figures. See \
        https://docs.mapbox.com/help/how-mapbox-works/access-tokens/ for more details
    """
    global MAPBOX_TOKEN
    MAPBOX_TOKEN = token


class ExpressFigure(go.Figure):
    offline_initialized = False
    """
    Boolean that starts out `False` and is set to `True` the first time the
    `_ipython_display_()` method is called (by a Jupyter environment), to indicate that
    subsequent calls to that method that `plotly.offline.init_notebook_mode()` has been
    called once and should not be called again.
    """

    def __init__(self, *args, **kwargs):
        super(ExpressFigure, self).__init__(*args, **kwargs)

    def _ipython_display_(self):
        if not ExpressFigure.offline_initialized:
            init_notebook_mode()
            ExpressFigure.offline_initialized = True
        iplot(self, show_link=False, auto_play=False)


Mapping = namedtuple(
    "Mapping",
    ["show_in_trace_name", "grouper", "val_map", "sequence", "updater", "variable"],
)
TraceSpec = namedtuple("TraceSpec", ["constructor", "attrs", "trace_patch"])


def get_label(args, column):
    try:
        return args["labels"][column]
    except Exception:
        return column


def get_decorated_label(args, column, role):
    label = get_label(args, column)
    if "histfunc" in args and (
        (role == "x" and args["orientation"] == "h")
        or (role == "y" and args["orientation"] == "v")
    ):
        if label:
            return "%s of %s" % (args["histfunc"] or "count", label)
        else:
            return "count"
    else:
        return label


def make_mapping(args, variable):
    if variable == "line_group" or variable == "animation_frame":
        return Mapping(
            show_in_trace_name=False,
            grouper=args[variable],
            val_map={},
            sequence=[""],
            variable=variable,
            updater=(lambda trace, v: v),
        )
    if variable == "facet_row" or variable == "facet_col":
        letter = "x" if variable == "facet_col" else "y"
        return Mapping(
            show_in_trace_name=False,
            variable=letter,
            grouper=args[variable],
            val_map={},
            sequence=[letter + str(i) for i in range(1, 1000)],
            updater=lambda trace, v: trace.update({letter + "axis": v}),
        )
    (parent, variable) = variable.split(".")
    vprefix = variable
    arg_name = variable
    if variable == "color":
        vprefix = "color_discrete"
    if variable == "dash":
        arg_name = "line_dash"
        vprefix = "line_dash"
    return Mapping(
        show_in_trace_name=True,
        variable=variable,
        grouper=args[arg_name],
        val_map=args[vprefix + "_map"].copy(),
        sequence=args[vprefix + "_sequence"],
        updater=lambda trace, v: trace.update({parent: {variable: v}}),
    )


def make_trace_kwargs(args, trace_spec, g, mapping_labels, sizeref, color_range):

    if "line_close" in args and args["line_close"]:
        g = g.append(g.iloc[0])
    result = trace_spec.trace_patch.copy() or {}
    hover_header = ""
    for k in trace_spec.attrs:
        v = args[k]
        v_label = get_decorated_label(args, v, k)
        if k == "dimensions":
            result["dimensions"] = [
                dict(
                    label=get_label(args, name),
                    values=column.values,
                    axis=dict(matches=True),
                )
                if trace_spec.constructor == go.Splom
                else dict(label=get_label(args, name), values=column.values)
                for name, column in g.iteritems()
                if ((not v) or (name in v))
                and (
                    trace_spec.constructor != go.Parcoords
                    or args["data_frame"][name].dtype.kind in "bifc"
                )
                and (
                    trace_spec.constructor != go.Parcats
                    or len(args["data_frame"][name].unique()) <= 20
                )
            ]
        elif v or (trace_spec.constructor == go.Histogram and k in ["x", "y"]):
            if k == "size":
                if "marker" not in result:
                    result["marker"] = dict()
                result["marker"]["size"] = g[v]
                result["marker"]["sizemode"] = "area"
                result["marker"]["sizeref"] = sizeref
                mapping_labels.append(("%s=%%{%s}" % (v_label, "marker.size"), None))
            elif k == "trendline":
                if v in ["ols", "lowess"] and args["x"] and args["y"] and len(g) > 1:
                    import statsmodels.api as sm

                    if v == "lowess":
                        trendline = sm.nonparametric.lowess(g[args["y"]], g[args["x"]])
                        result["x"] = trendline[:, 0]
                        result["y"] = trendline[:, 1]
                        hover_header = "<b>LOWESS trendline</b><br><br>"
                    elif v == "ols":
                        # sorting is bad but trace_specs with "trendline" have no other attrs
                        g2 = g.sort_values(by=args["x"])
                        y = g2[args["y"]]
                        x = g2[args["x"]]
                        result["x"] = x
                        fitted = sm.OLS(y, sm.add_constant(x)).fit()
                        result["y"] = fitted.predict()
                        hover_header = "<b>OLS trendline</b><br>"
                        hover_header += "%s = %f * %s + %f<br>" % (
                            args["y"],
                            fitted.params[1],
                            args["x"],
                            fitted.params[0],
                        )
                        hover_header += "R<sup>2</sup>=%f<br><br>" % fitted.rsquared
                    mapping_labels.append(
                        ("%s=%%{%s}" % (get_label(args, args["x"]), "x"), None)
                    )
                    mapping_labels.append(
                        (
                            "%s=%%{%s} <b>(trend)</b>"
                            % (get_label(args, args["y"]), "y"),
                            None,
                        )
                    )

            elif k.startswith("error"):
                error_xy = k[:7]
                arr = "arrayminus" if k.endswith("minus") else "array"
                if error_xy not in result:
                    result[error_xy] = {}
                result[error_xy][arr] = g[v]
            elif k == "hover_name":
                result["hovertext"] = g[v]
                if hover_header == "":
                    hover_header = "<b>%{hovertext}</b><br><br>"
            elif k == "color":
                colorbar_container = None
                if trace_spec.constructor == go.Choropleth:
                    result["z"] = g[v]
                    colorbar_container = result
                    color_letter = "z"
                    mapping_labels.append(("%s=%%{z}" % (v_label), None))
                else:
                    colorable = "marker"
                    if trace_spec.constructor in [go.Parcats, go.Parcoords]:
                        colorable = "line"
                    if colorable not in result:
                        result[colorable] = dict()
                    result[colorable]["color"] = g[v]
                    colorbar_container = result[colorable]
                    color_letter = "c"
                    mapping_labels.append(
                        ("%s=%%{%s.color}" % (v_label, colorable), None)
                    )
                d = len(args["color_continuous_scale"]) - 1
                colorbar_container["colorscale"] = [
                    [(1.0 * i) / (1.0 * d), x]
                    for i, x in enumerate(args["color_continuous_scale"])
                ]
                if color_range is None:
                    colorbar_container["showscale"] = False
                else:
                    colorbar_container["showscale"] = True
                    colorbar_container["colorbar"] = dict(title=v_label)
                    colorbar_container[color_letter + "min"] = color_range[0]
                    colorbar_container[color_letter + "max"] = color_range[1]
            elif k == "animation_group":
                result["ids"] = g[v]
            elif k == "locations":
                result[k] = g[v]
                mapping_labels.append(("%s=%%{%s}" % (v_label, "location"), None))
            else:
                if v:
                    result[k] = g[v]
                mapping_labels.append(("%s=%%{%s}" % (v_label, k), None))
    if trace_spec.constructor not in [
        go.Box,
        go.Violin,
        go.Histogram2dContour,
        go.Splom,
        go.Parcoords,
        go.Parcats,
    ]:
        hover_header += "<br>".join(s for s, t in mapping_labels) + "<extra></extra>"
        result["hovertemplate"] = hover_header
    return result


def configure_axes(args, constructor, fig, axes, orders):
    configurators = {
        go.Scatter: configure_cartesian_axes,
        go.Scattergl: configure_cartesian_axes,
        go.Bar: configure_cartesian_axes,
        go.Box: configure_cartesian_axes,
        go.Violin: configure_cartesian_axes,
        go.Histogram: configure_cartesian_axes,
        go.Histogram2dContour: configure_cartesian_axes,
        go.Histogram2d: configure_cartesian_axes,
        go.Scatter3d: configure_3d_axes,
        go.Scatterternary: configure_ternary_axes,
        go.Scatterpolar: configure_polar_axes,
        go.Scatterpolargl: configure_polar_axes,
        go.Barpolar: configure_polar_axes,
        go.Scattermapbox: configure_mapbox,
        go.Scattergeo: configure_geo,
        go.Choropleth: configure_geo,
    }
    if constructor in configurators:
        fig.update(layout=configurators[constructor](args, fig, axes, orders))


def set_cartesian_axis_opts(args, layout, letter, axis, orders):
    log_key = "log_" + letter
    range_key = "range_" + letter
    if log_key in args and args[log_key]:
        layout[axis]["type"] = "log"
        if range_key in args and args[range_key]:
            layout[axis]["range"] = [math.log(r, 10) for r in args[range_key]]
    elif range_key in args and args[range_key]:
        layout[axis]["range"] = args[range_key]

    if args[letter] in orders:
        layout[axis]["categoryorder"] = "array"
        layout[axis]["categoryarray"] = (
            orders[args[letter]]
            if axis.startswith("x")
            else list(reversed(orders[args[letter]]))
        )


def configure_cartesian_marginal_axes(args, orders):
    layout = dict(barmode="overlay", violinmode="overlay")
    for letter in ["x", "y"]:
        layout[letter + "axis1"] = dict(title=get_label(args, args[letter]))
        set_cartesian_axis_opts(args, layout, letter, letter + "axis1", orders)
    for letter in ["x", "y"]:
        otherletter = "x" if letter == "y" else "y"
        if args["marginal_" + letter]:
            if args["marginal_" + letter] == "histogram" or (
                "color" in args and args["color"]
            ):
                main_size = 0.74
            else:
                main_size = 0.84
            layout[otherletter + "axis1"]["domain"] = [0, main_size]
            layout[otherletter + "axis1"]["showgrid"] = True
            layout[otherletter + "axis2"] = {
                "domain": [main_size + 0.005, 1],
                "showticklabels": False,
            }
    return layout


def configure_cartesian_axes(args, fig, axes, orders):
    if ("marginal_x" in args and args["marginal_x"]) or (
        "marginal_y" in args and args["marginal_y"]
    ):
        return configure_cartesian_marginal_axes(args, orders)

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

    for letter, direction, row in (("x", "facet_col", False), ("y", "facet_row", True)):
        for letter_number in [t[letter + "axis"] for t in fig.data]:
            if letter_number not in layout["grid"][letter + "axes"]:
                layout["grid"][letter + "axes"].append(letter_number)
                axis = letter_number.replace(letter, letter + "axis")

                layout[axis] = dict(
                    title=get_decorated_label(args, args[letter], letter)
                )
                if len(letter_number) == 1:
                    set_cartesian_axis_opts(args, layout, letter, axis, orders)
                else:
                    layout[axis]["matches"] = letter
                    log_key = "log_" + letter
                    if log_key in args and args[log_key]:
                        layout[axis]["type"] = "log"

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
    return layout


def configure_ternary_axes(args, fig, axes, orders):
    return dict(
        ternary=dict(
            aaxis=dict(title=get_label(args, args["a"])),
            baxis=dict(title=get_label(args, args["b"])),
            caxis=dict(title=get_label(args, args["c"])),
        )
    )


def configure_polar_axes(args, fig, axes, orders):
    layout = dict(
        polar=dict(
            angularaxis=dict(direction=args["direction"], rotation=args["start_angle"]),
            radialaxis=dict(),
        )
    )

    for var, axis in [("r", "radialaxis"), ("theta", "angularaxis")]:
        if args[var] in orders:
            layout["polar"][axis]["categoryorder"] = "array"
            layout["polar"][axis]["categoryarray"] = orders[args[var]]

    radialaxis = layout["polar"]["radialaxis"]
    if args["log_r"]:
        radialaxis["type"] = "log"
        if args["range_r"]:
            radialaxis["range"] = [math.log(x, 10) for x in args["range_r"]]
    else:
        if args["range_r"]:
            radialaxis["range"] = args["range_r"]
    return layout


def configure_3d_axes(args, fig, axes, orders):
    layout = dict(
        scene=dict(
            xaxis=dict(title=get_label(args, args["x"])),
            yaxis=dict(title=get_label(args, args["y"])),
            zaxis=dict(title=get_label(args, args["z"])),
        )
    )

    for letter in ["x", "y", "z"]:
        axis = layout["scene"][letter + "axis"]
        if args["log_" + letter]:
            axis["type"] = "log"
            if args["range_" + letter]:
                axis["range"] = [math.log(x, 10) for x in args["range_" + letter]]
        else:
            if args["range_" + letter]:
                axis["range"] = args["range_" + letter]
        if args[letter] in orders:
            axis["categoryorder"] = "array"
            axis["categoryarray"] = orders[args[letter]]
    return layout


def configure_mapbox(args, fig, axes, orders):
    return dict(
        mapbox=dict(
            accesstoken=MAPBOX_TOKEN,
            center=dict(
                lat=args["data_frame"][args["lat"]].mean(),
                lon=args["data_frame"][args["lon"]].mean(),
            ),
            zoom=args["zoom"],
        )
    )


def configure_geo(args, fig, axes, orders):
    return dict(
        geo=dict(
            center=args["center"],
            scope=args["scope"],
            projection=dict(type=args["projection"]),
        )
    )


def configure_animation_controls(args, constructor, fig):
    def frame_args(duration):
        return {
            "frame": {"duration": duration, "redraw": constructor != go.Scatter},
            "mode": "immediate",
            "fromcurrent": True,
            "transition": {"duration": duration, "easing": "linear"},
        }

    if "animation_frame" in args and args["animation_frame"] and len(fig.frames) > 1:
        fig.layout.updatemenus = [
            {
                "buttons": [
                    {
                        "args": [None, frame_args(500)],
                        "label": "&#9654;",
                        "method": "animate",
                    },
                    {
                        "args": [[None], frame_args(0)],
                        "label": "&#9724;",
                        "method": "animate",
                    },
                ],
                "direction": "left",
                "pad": {"r": 10, "t": 70},
                "showactive": False,
                "type": "buttons",
                "x": 0.1,
                "xanchor": "right",
                "y": 0,
                "yanchor": "top",
            }
        ]
        fig.layout.sliders = [
            {
                "active": 0,
                "yanchor": "top",
                "xanchor": "left",
                "currentvalue": {
                    "prefix": get_label(args, args["animation_frame"]) + "="
                },
                "pad": {"b": 10, "t": 60},
                "len": 0.9,
                "x": 0.1,
                "y": 0,
                "steps": [
                    {
                        "args": [[f.name], frame_args(0)],
                        "label": f.name,
                        "method": "animate",
                    }
                    for f in fig.frames
                ],
            }
        ]


def make_trace_spec(args, constructor, attrs, trace_patch):
    result = [TraceSpec(constructor, attrs, trace_patch)]
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
                    attrs=[letter],
                    trace_patch=dict(opacity=0.5, **axis_map),
                )
            elif args["marginal_" + letter] == "violin":
                trace_spec = TraceSpec(
                    constructor=go.Violin, attrs=[letter], trace_patch=axis_map
                )
            elif args["marginal_" + letter] == "box":
                trace_spec = TraceSpec(
                    constructor=go.Box,
                    attrs=[letter],
                    trace_patch=dict(notched=True, **axis_map),
                )
            elif args["marginal_" + letter] == "rug":
                symbols = {"x": "line-ns-open", "y": "line-ew-open"}
                trace_spec = TraceSpec(
                    constructor=go.Box,
                    attrs=[letter],
                    trace_patch=dict(
                        fillcolor="rgba(255,255,255,0)",
                        line={"color": "rgba(255,255,255,0)"},
                        boxpoints="all",
                        jitter=0,
                        hoveron="points",
                        marker={"symbol": symbols[letter]},
                        **axis_map
                    ),
                )
            if "color" in attrs:
                if "marker" not in trace_spec.trace_patch:
                    trace_spec.trace_patch["marker"] = dict()
                trace_spec.trace_patch["marker"]["color"] = default_qualitative_seq[0]
            result.append(trace_spec)
    if "trendline" in args and args["trendline"]:
        trace_spec = TraceSpec(
            constructor=go.Scatter, attrs=["trendline"], trace_patch=dict(mode="lines")
        )
        if args["trendline_color_override"]:
            trace_spec.trace_patch["line"] = dict(
                color=args["trendline_color_override"]
            )
        result.append(trace_spec)
    return result


def one_group(x):
    return ""


def infer_config(args, constructor, trace_patch):
    attrables = (
        ["x", "y", "z", "a", "b", "c", "r", "theta", "size"]
        + ["dimensions", "hover_name", "text", "error_x", "error_x_minus"]
        + ["error_y", "error_y_minus", "error_z", "error_z_minus"]
        + ["lat", "lon", "locations", "animation_group"]
    )

    groupables = ["animation_frame", "facet_row", "facet_col", "line_group"]

    attrs = [k for k in attrables if k in args]
    grouped_attrs = [k for k in groupables if k in args]

    sizeref = 0
    if "size" in args and args["size"]:
        sizeref = args["data_frame"][args["size"]].max() / (
            args["size_max"] * args["size_max"]
        )

    color_range = None
    if "color" in args:
        if "color_continuous_scale" in args:
            if "color_discrete_sequence" not in args:
                attrs.append("color")
            else:
                if (
                    args["color"]
                    and args["data_frame"][args["color"]].dtype.kind in "bifc"
                ):
                    attrs.append("color")
                else:
                    grouped_attrs.append("marker.color")
        elif "line_group" in args or constructor == go.Histogram2dContour:
            grouped_attrs.append("line.color")
        else:
            grouped_attrs.append("marker.color")

        if "color" in attrs and args["color"]:
            cmin = args["data_frame"][args["color"]].min()
            cmax = args["data_frame"][args["color"]].max()
            if args["color_continuous_midpoint"]:
                cmid = args["color_continuous_midpoint"]
                delta = max(cmax - cmid, cmid - cmin)
                color_range = [cmid - delta, cmid + delta]
            else:
                color_range = [cmin, cmax]

    if "line_dash" in args:
        grouped_attrs.append("line.dash")

    if "symbol" in args:
        grouped_attrs.append("marker.symbol")

    trace_patch = trace_patch.copy()
    if "opacity" in args:
        trace_patch["marker"] = dict(opacity=args["opacity"])
    if "line_group" in args:
        trace_patch["mode"] = "lines" + ("+markers+text" if args["text"] else "")
    elif constructor != go.Splom and (
        "symbol" in args or constructor == go.Scattermapbox
    ):
        trace_patch["mode"] = "markers" + ("+text" if args["text"] else "")

    if "line_shape" in args:
        trace_patch["line"] = dict(shape=args["line_shape"])

    grouped_mappings = [make_mapping(args, a) for a in grouped_attrs]
    trace_specs = make_trace_spec(args, constructor, attrs, trace_patch)
    return trace_specs, grouped_mappings, sizeref, color_range


def make_figure(args, constructor, trace_patch={}, layout_patch={}):
    trace_specs, grouped_mappings, sizeref, color_range = infer_config(
        args, constructor, trace_patch
    )
    grouper = [x.grouper or one_group for x in grouped_mappings] or [one_group]
    grouped = args["data_frame"].groupby(grouper, sort=False)
    orders = {} if "category_orders" not in args else args["category_orders"].copy()
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

    trace_names_by_frame = {}
    frames = OrderedDict()
    for group_name in group_names:
        group = grouped.get_group(group_name if len(group_name) > 1 else group_name[0])
        mapping_labels = []
        frame_name = ""
        for col, val, m in zip(grouper, group_name, grouped_mappings):
            if col != one_group:
                s = ("%s=%s" % (get_label(args, col), val), m.show_in_trace_name)
                if s not in mapping_labels:
                    mapping_labels.append(s)
                if m.variable == "animation_frame":
                    frame_name = str(val)
        trace_name = ", ".join(s for s, t in mapping_labels if t)
        if frame_name not in trace_names_by_frame:
            trace_names_by_frame[frame_name] = set()
        trace_names = trace_names_by_frame[frame_name]

        for trace_spec in trace_specs:
            constructor = trace_spec.constructor
            if constructor in [go.Scatter, go.Scatterpolar]:
                if "render_mode" in args and (
                    args["render_mode"] == "webgl"
                    or (
                        args["render_mode"] == "auto"
                        and len(args["data_frame"]) > 1000
                        and args["animation_frame"] is None
                    )
                ):
                    constructor = (
                        go.Scattergl if constructor == go.Scatter else go.Scatterpolargl
                    )
            trace = trace_spec.constructor(name=trace_name or " ")
            if trace_spec.constructor != go.Parcats:
                trace.update(
                    legendgroup=trace_name,
                    showlegend=(trace_name != "" and trace_name not in trace_names),
                )
            if trace_spec.constructor in [go.Bar, go.Violin, go.Box, go.Histogram]:
                trace.update(alignmentgroup=True, offsetgroup=trace_name)
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
                        or trace_specs[0].constructor not in [go.Scatter, go.Scattergl]
                        or m.variable != "symbol"
                    ):
                        raise
            trace.update(
                make_trace_kwargs(
                    args,
                    trace_spec,
                    group,
                    mapping_labels[:],
                    sizeref,
                    color_range=color_range if frame_name not in frames else None,
                )
            )
            if frame_name not in frames:
                frames[frame_name] = dict(data=[], name=frame_name)
            frames[frame_name]["data"].append(trace)
    frame_list = [f for _, f in frames.items()]
    layout_patch = layout_patch.copy()
    for v in ["title", "height", "width", "template"]:
        if args[v]:
            layout_patch[v] = args[v]
    layout_patch["legend"] = {"tracegroupgap": 0}
    if "title" not in layout_patch:
        layout_patch["margin"] = {"t": 60}
    fig = ExpressFigure(
        data=frame_list[0]["data"] if len(frame_list) > 0 else [],
        layout=layout_patch,
        frames=frame_list if len(frames) > 1 else [],
    )
    axes = {m.variable: m.val_map for m in grouped_mappings}
    configure_axes(args, constructor, fig, axes, orders)
    configure_animation_controls(args, constructor, fig)
    return fig

