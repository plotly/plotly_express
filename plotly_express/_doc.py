import inspect

docs = dict(
    df="A `pandas.DataFrame` object.",
    x="Name of column to map onto x position",
    y="Name of column to map onto y position",
    z="Name of column to map onto z position",
)


def make_docstring(fn):
    result = fn.__doc__ + "\nArgs:\n"
    for arg in inspect.getargspec(fn)[0]:
        d = docs[arg] if arg in docs else "(documentation missing)"
        result += f"    {arg}: {d}" + "\n"
    result += "Returns:\n"
    result += "    A `plotly.graph_objs.Figure` object, augmented to display itself "
    "in Jupyter notebooks by calling `init_notebook_mode()` itself once."
    return result
