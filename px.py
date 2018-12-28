import plotly.graph_objs as go

from collections import namedtuple


default_color_seq = ["#3366cc", "#dc3912", "#ff9900", "#109618",
                     "#990099", "#0099c6", "#dd4477", "#66aa00",
                     "#b82e2e", "#316395", "#994499", "#22aa99",
                     "#aaaa11", "#6633cc", "#e67300", "#8b0707",
                     "#651067", "#329262", "#5574a6", "#3b3eac"]
default_symbol_seq = ["circle", "triangle-down", "square", "x", "cross"]
default_dash_seq = ["solid", "dot", "dash",
                    "longdash", "dashdot", "longdashdot"]
Mapping = namedtuple('Mapping', ['grouper', 'val_map', 'sequence', 'updater'])


def make_mapping(variable, parent, args):
    return Mapping(
        grouper=args[variable],
        val_map=args[variable+"_map"].copy(),
        sequence=args[variable+"_sequence"],
        updater=lambda x: {parent: {variable: x}},
    )


def make_figure(df, constructor, trace_kwargs_by_group, mappings):
    fig = go.FigureWidget(
        {"layout": {'template': 'plotly', 'hovermode': 'closest'}})

    def one_group(x): return ""
    grouper = [x.grouper or one_group for x in mappings] or [one_group]
    for group_name, group in df.groupby(grouper):
        if len(grouper) == 1:
            group_name = [group_name]
        mapping_str = []
        for col, val in zip(grouper, group_name):
            if col != one_group:
                s = "%s=%s" % (col, val)
                if s not in mapping_str:
                    mapping_str.append(s)
        trace = constructor(name=", ".join(mapping_str))
        for i, m in enumerate(mappings):
            val = group_name[i]
            if val not in m.val_map:
                m.val_map[val] = m.sequence[len(m.val_map) % len(m.sequence)]
            trace.update(m.updater(m.val_map[val]))
        trace.update(trace_kwargs_by_group(group))
        fig.add_trace(trace)
    return fig


def cartesian_axes(fig, args):
    fig.layout.xaxis.title = args["x"]
    fig.layout.yaxis.title = args["y"]
    if args["log_x"]:
        fig.layout.xaxis.type = "log"
    if args["log_y"]:
        fig.layout.yaxis.type = "log"


def scatter(df, x, y, color=None, symbol=None, size=None, name=None,
            color_map={}, symbol_map={},
            color_sequence=default_color_seq,
            symbol_sequence=default_symbol_seq,
            log_x=False, log_y=False):
    if size:
        sizeref = df[size].max() / (45*45)
    fig = make_figure(
        df, go.Scatter,
        lambda g: dict(mode='markers', x=g[x], y=g[y],
                       hovertext=name and g[name],
                       marker=size and dict(
                           size=g[size], sizemode="area", sizeref=sizeref)
                       ),
        [
            make_mapping("color", "marker", locals()),
            make_mapping("symbol", "marker", locals())
        ]
    )
    cartesian_axes(fig, locals())
    return fig


def density_heatmap(df, x, y, log_x=False, log_y=False):
    fig = make_figure(
        df, go.Histogram2d,
        lambda g: dict(x=g[x], y=g[y]),
        []
    )
    cartesian_axes(fig, locals())
    return fig


def density_contour(df, x, y, log_x=False, log_y=False):
    fig = make_figure(
        df, go.Histogram2dContour,
        lambda g: dict(x=g[x], y=g[y]),
        []
    )
    cartesian_axes(fig, locals())
    return fig


def line(df, x, y, color=None, dash=None,
         color_map={}, dash_map={},
         color_sequence=default_color_seq,
         dash_sequence=default_dash_seq, log_x=False, log_y=False):
    fig = make_figure(
        df, go.Scatter,
        lambda g: dict(mode='lines', x=g[x], y=g[y]),
        [
            make_mapping("color", "marker", locals()),
            make_mapping("dash", "line", locals())
        ]
    )
    cartesian_axes(fig, locals())
    return fig


def bar(df, x, y, color=None, color_map={}, color_sequence=default_color_seq,
        orientation='v', normalization="", mode="relative", log_x=False, log_y=False):
    fig = make_figure(
        df, go.Bar,
        lambda g: dict(x=g[x], y=g[y], orientation=orientation),
        [make_mapping("color", "marker", locals())]
    )
    cartesian_axes(fig, locals())
    fig.layout.barnorm = normalization
    fig.layout.barmode = mode
    return fig


def histogram(df, x, y, color=None, color_map={}, color_sequence=default_color_seq,
              orientation='v', mode="stack", normalization=None, log_x=False, log_y=False):
    fig = make_figure(
        df, go.Histogram,
        lambda g: dict(x=g[x], y=g[y], orientation=orientation,
                       histnorm=normalization),
        [make_mapping("color", "marker", locals())]
    )
    cartesian_axes(fig, locals())
    fig.layout.barmode = mode
    return fig


def violin(df, x, y, color=None, color_map={}, color_sequence=default_color_seq,
           orientation='v', mode="group", log_x=False, log_y=False):
    fig = make_figure(
        df, go.Violin,
        lambda g: dict(x=g[x], y=g[y], orientation=orientation),
        [make_mapping("color", "marker", locals())]
    )
    cartesian_axes(fig, locals())
    fig.layout.violinmode = mode
    return fig


def box(df, x, y, color=None, color_map={}, color_sequence=default_color_seq,
        orientation='v', mode="group", log_x=False, log_y=False):
    fig = make_figure(
        df, go.Box,
        lambda g: dict(x=g[x], y=g[y], orientation=orientation),
        [make_mapping("color", "marker", locals())]
    )
    cartesian_axes(fig, locals())
    fig.layout.boxmode = mode
    return fig


def scatter_ternary(df, a, b, c, color=None, symbol=None, size=None,
                    color_map={}, symbol_map={},
                    color_sequence=default_color_seq,
                    symbol_sequence=default_symbol_seq):
    if size:
        sizeref = df[size].max() / (45*45)
    fig = make_figure(
        df, go.Scatterternary,
        lambda g: dict(mode='markers', a=g[a], b=g[b], c=g[c],
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


def line_ternary(df, a, b, c, color=None, dash=None,
                 color_map={}, dash_map={},
                 color_sequence=default_color_seq,
                 dash_sequence=default_dash_seq):
    fig = make_figure(
        df, go.Scatter,
        lambda g: dict(mode='lines', a=g[a], b=g[b], c=g[c]),
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
    if size:
        sizeref = df[size].max() / (45*45)
    fig = make_figure(
        df, go.Scatterpolar,
        lambda g: dict(mode='markers', r=g[r], theta=g[theta],
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
        df, go.Scatter,
        lambda g: dict(mode='lines', r=g[r], theta=g[theta]),
        [
            make_mapping("color", "marker", locals()),
            make_mapping("dash", "line", locals())
        ]
    )
    return fig


def bar_polar(df, r, theta, color=None, color_map={}, color_sequence=default_color_seq,
              normalization="", mode="relative"):
    fig = make_figure(
        df, go.Barpolar,
        lambda g: dict(r=g[r], theta=g[theta]),
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
                (not dimensions and column.dtype in ["int64", "float64"])
            )
        ]),
        [
            make_mapping("color", "marker", locals()),
            make_mapping("symbol", "marker", locals())
        ]
    )
    return fig

# TODO canonical examples ... needed now!
# TODO test with none, all, any mappings
# TODO test each plot
# TODO test defaults
# TODO histogram weights and calcs
# TODO various box and violin options
# TODO log scales in SPLOM and generally in facets
# TODO check on dates
# TODO facets
# TODO marginals
# TODO validate inputs
# TODO name / hover labels
# TODO opacity
# TODO continuous color
# TODO color splits in densities
# TODO groupby ignores NaN ... ?
# TODO suppress plotly.py errors... don't show our programming errors?
# TODO parcoords, parcats
