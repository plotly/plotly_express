import inspect

docs = dict(
    data_frame="A `pandas.DataFrame`",
    x="Name of column to map onto x position",
    y="Name of column to map onto y position",
    z="Name of column to map onto z position",
)


def make_docstring(fn):
    result = (fn.__doc__ or "") + "\nArguments:\n"
    for arg in inspect.getargspec(fn)[0]:
        d = docs[arg] if arg in docs else "(documentation missing)"
        result += f"    {arg}: {d}" + "\n"
    result += "Returns:\n"
    result += "    A `plotly_express.FigurePx` object."
    return result
