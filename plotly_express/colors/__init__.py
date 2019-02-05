from . import (  # noqa: F401
    qualitative,
    sequential,
    diverging,
    cyclical,
    cmocean,
    colorbrewer,
    carto,
)


def swatches(mod):
    from .. import _px
    import plotly.graph_objs as go

    sequences = [(k, v) for k, v in mod.__dict__.items() if not k.startswith("__")]

    return _px.FigurePx(
        data=[
            go.Bar(
                orientation="h",
                y=[name] * len(colors),
                x=[1] * len(colors),
                customdata=list(range(len(colors))),
                marker=dict(color=colors),
                hovertemplate="%{y}[%{customdata}] = %{marker.color}<extra></extra>",
            )
            for name, colors in reversed(sequences)
        ],
        layout=dict(
            title=mod.__name__,
            barmode="stack",
            barnorm="fraction",
            bargap=0.5,
            showlegend=False,
            xaxis=dict(range=[-0.02, 1.02], showticklabels=False, showgrid=False),
            height=max(600, 40 * len(sequences)),
        ),
    )
