import plotly.graph_objs as go
from plotly.offline import init_notebook_mode, iplot
from collections import namedtuple


class FigurePx(go.Figure):
    offline_initialized = False

    def __init__(self, *args, **kwargs):
        super(FigurePx, self).__init__(*args, **kwargs)
        if not FigurePx.offline_initialized:
            init_notebook_mode()
            FigurePx.offline_initialized = True

    def _ipython_display_(self):
        iplot(self, show_link=False)


default_color_seq = ["#3366cc", "#dc3912", "#ff9900", "#109618",
                     "#990099", "#0099c6", "#dd4477", "#66aa00",
                     "#b82e2e", "#316395", "#994499", "#22aa99",
                     "#aaaa11", "#6633cc", "#e67300", "#8b0707",
                     "#651067", "#329262", "#5574a6", "#3b3eac"]
default_symbol_seq = ["circle", "triangle-down", "square", "x", "cross"]
default_dash_seq = ["solid", "dot", "dash",
                    "longdash", "dashdot", "longdashdot"]
Mapping = namedtuple(
    'Mapping', ['facet', 'grouper', 'val_map', 'sequence', 'updater'])


def make_mapping(variable, parent, args):
    return Mapping(
        facet=False,
        grouper=args[variable],
        val_map=args[variable+"_map"].copy(),
        sequence=args[variable+"_sequence"],
        updater=lambda trace, v: trace.update({parent: {variable: v}}),
    )


def make_cartesian_facet_mapping(letter, column, facet_map):
    return Mapping(
        facet=True,
        grouper=column,
        val_map=facet_map,
        sequence=[letter+str(i) for i in range(1, 1000)],
        updater=lambda trace, v: trace.update({letter+"axis": v}),
    )


def make_figure(df, constructor, trace_kwargs_by_group, mappings):
    fig = FigurePx(
        layout={'template': 'plotly', 'height': 600,
                'margin': {'t': 40},
                'hovermode': 'closest', 'legend': {'tracegroupgap': 0}}
    )

    def one_group(x): return ""
    grouper = [x.grouper or one_group for x in mappings] or [one_group]
    trace_names = set()
    traces = []
    for group_name, group in df.groupby(grouper):
        if len(grouper) == 1:
            group_name = [group_name]
        mapping_str = []
        for col, val, m in zip(grouper, group_name, mappings):
            if col != one_group and not m.facet:
                s = "%s=%s" % (col, val)
                if s not in mapping_str:
                    mapping_str.append(s)
        trace_name = ", ".join(mapping_str)

        trace = constructor(name=trace_name, legendgroup=trace_name,
                            showlegend=(
                                trace_name != '' and trace_name not in trace_names),
                            **trace_kwargs_by_group(group))
        trace_names.add(trace_name)
        for i, m in enumerate(mappings):
            val = group_name[i]
            if val not in m.val_map:
                m.val_map[val] = m.sequence[len(m.val_map) % len(m.sequence)]
            m.updater(trace, m.val_map[val])
        traces.append(trace)
    fig.add_traces(traces)
    return fig


def auto_sizeref(df, size):
    return size and df[size].max() / (45*45)


def configure_cartesian_axes(fig, axes, args):
    gap = 0.1
    layout = {"grid": {"xaxes": [], "yaxes": [], "xgap": gap, "ygap": gap,
                       "xside": "bottom", "yside": "left"}}
    for letter in ["x", "y"]:
        for letter_number in set(t[letter+"axis"] for t in fig.data):
            if letter_number not in layout["grid"][letter+"axes"]:
                layout["grid"][letter+"axes"].append(letter_number)
                axis = letter_number.replace(letter, letter+"axis")
                layout[axis] = {}
                if len(letter_number) > 1:
                    layout[axis]["scaleanchor"] = letter+"1"
                layout[axis]["title"] = args[letter]
                if args["log_"+letter]:
                    layout[axis]["type"] = "log"
    layout["grid"]["yaxes"] = [i for i in reversed(layout["grid"]["yaxes"])]

    layout["annotations"] = []
    for letter, direction, row in (("x", "col", False), ("y", "row", True)):
        if args[direction]:
            step = 1.0/(len(layout["grid"][letter+"axes"])-gap)
            for key, value in axes[letter].items():
                i = int(value[1:])
                if row:
                    i = len(layout["grid"][letter+"axes"])-i
                else:
                    i -= 1
                layout["annotations"].append({
                    "xref": "paper", "yref": "paper", "showarrow": False,
                    "xanchor": "center", "yanchor": "middle",
                    "text": args[direction]+"="+str(key),
                    "x": 1.01 if row else step*(i+(0.5-gap/2)),
                    "y": step*(i+(0.5-gap/2))if row else 1.02,
                    "textangle": 90 if row else 0
                })
    fig.layout.update(layout)


def scatter(df, x=None, y=None, color=None, symbol=None, size=None, name=None,
            color_map={}, symbol_map={},
            color_sequence=default_color_seq,
            symbol_sequence=default_symbol_seq,
            row=None, col=None,
            log_x=False, log_y=False):
    sizeref = auto_sizeref(df, size)
    axes = {"x": {}, "y": {}}
    fig = make_figure(
        df, go.Scatter,
        lambda g: dict(mode='markers', x=x and g[x], y=y and g[y],
                       hovertext=name and g[name],
                       marker=size and dict(
                           size=g[size], sizemode="area", sizeref=sizeref)
                       ),
        [
            make_cartesian_facet_mapping("x", col, axes["x"]),
            make_cartesian_facet_mapping("y", row, axes["y"]),
            make_mapping("color", "marker", locals()),
            make_mapping("symbol", "marker", locals())
        ]
    )
    configure_cartesian_axes(fig, axes, locals())
    return fig


def density_heatmap(df, x=None, y=None,  row=None, col=None, log_x=False, log_y=False):
    axes = {"x": {}, "y": {}}
    fig = make_figure(
        df, go.Histogram2d,
        lambda g: dict(x=x and g[x], y=y and g[y]),
        [
            make_cartesian_facet_mapping("x", col, axes["x"]),
            make_cartesian_facet_mapping("y", row, axes["y"])
        ]
    )
    configure_cartesian_axes(fig, axes, locals())
    return fig


def density_contour(df, x=None, y=None, color=None, color_map={},
                    color_sequence=default_color_seq,
                    row=None, col=None, log_x=False, log_y=False):
    axes = {"x": {}, "y": {}}
    fig = make_figure(
        df, go.Histogram2dContour,
        lambda g: dict(x=x and g[x], y=y and g[y],
                       contours=dict(coloring="none")),
        [
            make_cartesian_facet_mapping("x", col, axes["x"]),
            make_cartesian_facet_mapping("y", row, axes["y"]),
            make_mapping("color", "line", locals()),
        ]
    )
    configure_cartesian_axes(fig, axes, locals())
    return fig


def line(df, x=None, y=None, color=None, dash=None, split=None, name=None,
         color_map={}, dash_map={},
         color_sequence=default_color_seq,
         dash_sequence=default_dash_seq,
         row=None, col=None,
         log_x=False, log_y=False):
    axes = {"x": {}, "y": {}}
    fig = make_figure(
        df, go.Scatter,
        lambda g: dict(mode='lines', x=x and g[x], y=y and g[y],
                       hovertext=name and g[name],),
        [
            make_cartesian_facet_mapping("x", col, axes["x"]),
            make_cartesian_facet_mapping("y", row, axes["y"]),
            make_mapping("color", "line", locals()),
            make_mapping("dash", "line", locals()),
            Mapping(facet=True, grouper=split, val_map={}, sequence=[''],
                    updater=lambda trace, v: v
                    )
        ]
    )
    configure_cartesian_axes(fig, axes, locals())
    return fig


def bar(df, x=None, y=None, color=None, color_map={}, color_sequence=default_color_seq,
        row=None, col=None,
        orientation='v', normalization="", mode="relative", log_x=False, log_y=False):
    axes = {"x": {}, "y": {}}
    fig = make_figure(
        df, go.Bar,
        lambda g: dict(x=x and g[x], y=y and g[y], orientation=orientation),
        [
            make_cartesian_facet_mapping("x", col, axes["x"]),
            make_cartesian_facet_mapping("y", row, axes["y"]),
            make_mapping("color", "marker", locals())
        ]
    )
    configure_cartesian_axes(fig, axes, locals())
    fig.layout.barnorm = normalization
    fig.layout.barmode = mode
    return fig


def histogram(df, x=None, y=None, color=None, color_map={}, color_sequence=default_color_seq,
              row=None, col=None,
              orientation='v', mode="stack", normalization=None,
              log_x=False, log_y=False):
    axes = {"x": {}, "y": {}}
    fig = make_figure(
        df, go.Histogram,
        lambda g: dict(x=x and g[x], y=y and g[y], orientation=orientation,
                       histnorm=normalization),
        [
            make_cartesian_facet_mapping("x", col, axes["x"]),
            make_cartesian_facet_mapping("y", row, axes["y"]),
            make_mapping("color", "marker", locals())
        ]
    )
    configure_cartesian_axes(fig, axes, locals())
    fig.layout.barmode = mode
    return fig


def violin(df, x=None, y=None, color=None, color_map={}, color_sequence=default_color_seq,
           orientation='v', mode="group",
           row=None, col=None, log_x=False, log_y=False):
    axes = {"x": {}, "y": {}}
    fig = make_figure(
        df, go.Violin,
        lambda g: dict(x=x and g[x], y=y and g[y], orientation=orientation),
        [
            make_cartesian_facet_mapping("x", col, axes["x"]),
            make_cartesian_facet_mapping("y", row, axes["y"]),
            make_mapping("color", "marker", locals())
        ]
    )
    configure_cartesian_axes(fig, axes, locals())
    fig.layout.update(dict(violinmode=mode))
    return fig


def box(df, x=None, y=None, color=None, color_map={}, color_sequence=default_color_seq,
        orientation='v', mode="group",
        row=None, col=None, log_x=False, log_y=False):
    axes = {"x": {}, "y": {}}
    fig = make_figure(
        df, go.Box,
        lambda g: dict(x=x and g[x], y=y and g[y], orientation=orientation),
        [
            make_cartesian_facet_mapping("x", col, axes["x"]),
            make_cartesian_facet_mapping("y", row, axes["y"]),
            make_mapping("color", "marker", locals())
        ]
    )
    configure_cartesian_axes(fig, axes, locals())
    fig.layout.boxmode = mode
    return fig


def scatter_ternary(df, a=None, b=None, c=None, color=None, symbol=None, size=None,
                    color_map={}, symbol_map={},
                    color_sequence=default_color_seq,
                    symbol_sequence=default_symbol_seq):
    sizeref = auto_sizeref(df, size)
    fig = make_figure(
        df, go.Scatterternary,
        lambda g: dict(mode='markers', a=a and g[a], b=b and g[b], c=c and g[c],
                       marker=size and dict(
                           size=g[size], sizemode="area", sizeref=sizeref)
                       ),
        [
            make_mapping("color", "marker", locals()),
            make_mapping("symbol", "marker", locals())
        ]
    )
    fig.layout.ternary.aaxis.title = a
    fig.layout.ternary.baxis.title = b
    fig.layout.ternary.caxis.title = c
    return fig


def line_ternary(df, a=None, b=None, c=None, color=None, dash=None,
                 color_map={}, dash_map={},
                 color_sequence=default_color_seq,
                 dash_sequence=default_dash_seq):
    fig = make_figure(
        df, go.Scatterternary,
        lambda g: dict(mode='lines', a=a and g[a], b=b and g[b], c=c and g[c]),
        [
            make_mapping("color", "marker", locals()),
            make_mapping("dash", "line", locals())
        ]
    )
    fig.layout.ternary.aaxis.title = a
    fig.layout.ternary.baxis.title = b
    fig.layout.ternary.caxis.title = c
    return fig


def scatter_polar(df, r, theta, color=None, symbol=None, size=None,
                  color_map={}, symbol_map={},
                  color_sequence=default_color_seq,
                  symbol_sequence=default_symbol_seq):
    sizeref = auto_sizeref(df, size)
    fig = make_figure(
        df, go.Scatterpolar,
        lambda g: dict(mode='markers', r=r and g[r], theta=theta and g[theta],
                       marker=size and dict(
                           size=g[size], sizemode="area", sizeref=sizeref)
                       ),
        [
            make_mapping("color", "marker", locals()),
            make_mapping("symbol", "marker", locals())
        ]
    )
    return fig


def line_polar(df, r, theta, color=None, dash=None,
               color_map={}, dash_map={},
               color_sequence=default_color_seq,
               dash_sequence=default_dash_seq):
    fig = make_figure(
        df, go.Scatterpolar,
        lambda g: dict(mode='lines', r=r and g[r], theta=theta and g[theta]),
        [
            make_mapping("color", "marker", locals()),
            make_mapping("dash", "line", locals())
        ]
    )
    return fig


def bar_polar(df, r=None, theta=None, color=None, color_map={}, color_sequence=default_color_seq,
              normalization="", mode="relative"):
    fig = make_figure(
        df, go.Barpolar,
        lambda g: dict(r=r and g[r], theta=theta and g[theta]),
        [
            make_mapping("color", "marker", locals())
        ]
    )
    fig.layout.barnorm = normalization
    fig.layout.barmode = mode
    return fig


def splom(df, dimensions=None, color=None, symbol=None,
          color_map={}, symbol_map={},
          color_sequence=default_color_seq,
          symbol_sequence=default_symbol_seq):
    fig = make_figure(
        df, go.Splom,
        lambda g: dict(dimensions=[
            dict(label=name, values=column.values)
            for name, column in g.iteritems()
            if (
                (dimensions and name in dimensions) or
                (not dimensions)
            )
        ]),
        [
            make_mapping("color", "marker", locals()),
            make_mapping("symbol", "marker", locals())
        ]
    )
    return fig

# TODO cartesian_axes doesn't need fig, could return a delta object
# TODO pass in more arguments to make_figure such that it returns the whole figure
# TODO gl vs not gl
# TODO violin infers extra categories for traces, doesn't honor legendgroup
# TODO lock ranges on shared axes, including colormap ... shared colormap?
# TODO canonical examples ... needed now!
# TODO test with none, all, any mappings
# TODO test each plot
# TODO test defaults
# TODO histogram weights and calcs
# TODO various box and violin options
# TODO log scales in SPLOM
# TODO check on dates
# TODO facet wrap
# TODO non-cartesian faceting
# TODO marginals
# TODO validate inputs
# TODO name / hover labels
# TODO opacity
# TODO continuous color
# TODO color splits in densities
# TODO groupby ignores NaN ... ?
# TODO suppress plotly.py errors... don't show our programming errors?
# TODO parcoords, parcats
