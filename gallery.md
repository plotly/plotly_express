---
jupyter:
  jupytext:
    formats: ipynb,md
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.1'
      jupytext_version: 1.1.1
  kernelspec:
    display_name: Python 3
    language: python
    name: python3
---

# Plotly Express Gallery

Plotly Express is a terse, consistent, high-level wrapper around [Plotly.py](https://plot.ly/python) for rapid data exploration and figure generation.

This notebook demonstrates various `plotly_express` features. [Reference documentation](https://plotly.github.io/plotly_express/plotly_express/) and a [step by step walkthrough notebook](https://nbviewer.jupyter.org/github/plotly/plotly_express/blob/gh-pages/walkthrough.ipynb) are also available.

You can also read our [Medium announcement article](https://medium.com/@plotlygraphs/introducing-plotly-express-808df010143d) for more information on this library.

## A single import

```python
import plotly_express as px
```

## Built-in sample datasets

```python
print(px.data.iris.__doc__)
iris = px.data.iris()
```

```python
tips = px.data.tips()
gapminder = px.data.gapminder()
election = px.data.election()
wind = px.data.wind()
carshare = px.data.carshare()
```

## Scatter and Line plots

```python
px.scatter(iris, x="sepal_width", y="sepal_length")
```

```python
px.scatter(iris, x="sepal_width", y="sepal_length", color="species")
```

```python
px.scatter(iris, x="sepal_width", y="sepal_length", color="species", marginal_y="rug", marginal_x="histogram")
```

```python
px.scatter(iris, x="sepal_width", y="sepal_length", color="species", marginal_y="violin",
           marginal_x="box", trendline="ols")
```

```python
iris["e"] = iris["sepal_width"]/100
px.scatter(iris, x="sepal_width", y="sepal_length", color="species", error_x="e", error_y="e")
```

```python
del iris["e"]
```

```python
px.scatter(tips, x="total_bill", y="tip", facet_row="time", facet_col="day", color="smoker", trendline="ols",
          category_orders={"day": ["Thur", "Fri", "Sat", "Sun"], "time": ["Lunch", "Dinner"]})
```

```python
px.scatter_matrix(iris)
```

```python
px.scatter_matrix(iris, dimensions=["sepal_width", "sepal_length", "petal_width", "petal_length"], color="species")
```

```python
px.parallel_coordinates(iris, color="species_id", labels={"species_id": "Species",
                  "sepal_width": "Sepal Width", "sepal_length": "Sepal Length",
                  "petal_width": "Petal Width", "petal_length": "Petal Length", },
                    color_continuous_scale=px.colors.diverging.Tealrose, color_continuous_midpoint=2)
```

```python
px.parallel_categories(tips, color="size", color_continuous_scale=px.colors.sequential.Inferno)
```

```python
px.scatter(tips, x="total_bill", y="tip", color="size", facet_col="sex",
           color_continuous_scale=px.colors.sequential.Viridis, render_mode="webgl")
```

```python
px.scatter(gapminder.query("year==2007"), x="gdpPercap", y="lifeExp", size="pop", color="continent",
           hover_name="country", log_x=True, size_max=60)
```

```python
px.scatter(gapminder, x="gdpPercap", y="lifeExp", animation_frame="year", animation_group="country",
           size="pop", color="continent", hover_name="country", facet_col="continent",
           log_x=True, size_max=45, range_x=[100,100000], range_y=[25,90])
```

```python
px.line(gapminder, x="year", y="lifeExp", color="continent", line_group="country", hover_name="country",
        line_shape="spline", render_mode="svg")
```

```python
px.area(gapminder, x="year", y="pop", color="continent", line_group="country")
```

## Visualize Distributions

```python
px.density_contour(iris, x="sepal_width", y="sepal_length")
```

```python
px.density_contour(iris, x="sepal_width", y="sepal_length", color="species", marginal_x="rug", marginal_y="histogram")
```

```python
px.density_heatmap(iris, x="sepal_width", y="sepal_length", marginal_x="rug", marginal_y="histogram")
```

```python
px.bar(tips, x="sex", y="total_bill", color="smoker", barmode="group")
```

```python
px.bar(tips, x="sex", y="total_bill", color="smoker", barmode="group", facet_row="time", facet_col="day",
       category_orders={"day": ["Thur", "Fri", "Sat", "Sun"], "time": ["Lunch", "Dinner"]})
```

```python
px.histogram(tips, x="total_bill", y="tip", color="sex", marginal="rug", hover_data=tips.columns)
```

```python
px.histogram(tips, x="sex", y="tip", histfunc="avg", color="smoker", barmode="group",
             facet_row="time", facet_col="day", category_orders={"day": ["Thur", "Fri", "Sat", "Sun"],
                                                                "time": ["Lunch", "Dinner"]})
```

```python
px.strip(tips, x="total_bill", y="time", orientation="h", color="smoker")
```

```python
px.box(tips, x="day", y="total_bill", color="smoker", notched=True)
```

```python
px.violin(tips, y="tip", x="smoker", color="sex", box=True, points="all", hover_data=tips.columns)
```

## Ternary Coordinates

```python
px.scatter_ternary(election, a="Joly", b="Coderre", c="Bergeron", color="winner", size="total", hover_name="district",
                   size_max=15, color_discrete_map = {"Joly": "blue", "Bergeron": "green", "Coderre":"red"} )
```

```python
px.line_ternary(election, a="Joly", b="Coderre", c="Bergeron", color="winner", line_dash="winner")
```

## 3D Coordinates

```python
px.scatter_3d(election, x="Joly", y="Coderre", z="Bergeron", color="winner", size="total", hover_name="district",
                  symbol="result", color_discrete_map = {"Joly": "blue", "Bergeron": "green", "Coderre":"red"})
```

```python
px.line_3d(election, x="Joly", y="Coderre", z="Bergeron", color="winner", line_dash="winner")
```

## Polar Coordinates

```python
px.scatter_polar(wind, r="frequency", theta="direction", color="strength", symbol="strength",
            color_discrete_sequence=px.colors.sequential.Plasma[-2::-1])
```

```python
px.line_polar(wind, r="frequency", theta="direction", color="strength", line_close=True,
            color_discrete_sequence=px.colors.sequential.Plasma[-2::-1])
```

```python
px.bar_polar(wind, r="frequency", theta="direction", color="strength", template="plotly_dark",
            color_discrete_sequence= px.colors.sequential.Plasma[-2::-1])
```

## Maps

```python
px.set_mapbox_access_token(open(".mapbox_token").read())
px.scatter_mapbox(carshare, lat="centroid_lat", lon="centroid_lon", color="peak_hour", size="car_hours",
                  color_continuous_scale=px.colors.cyclical.IceFire, size_max=15, zoom=10)
```

```python
px.set_mapbox_access_token(open(".mapbox_token").read())
px.line_mapbox(carshare, lat="centroid_lat", lon="centroid_lon", color="peak_hour")
```

```python
px.scatter_geo(gapminder, locations="iso_alpha", color="continent", hover_name="country", size="pop",
               animation_frame="year", projection="natural earth")
```

```python
px.line_geo(gapminder.query("year==2007"), locations="iso_alpha", color="continent", projection="orthographic")
```

```python
px.choropleth(gapminder, locations="iso_alpha", color="lifeExp", hover_name="country", animation_frame="year",
             color_continuous_scale=px.colors.sequential.Plasma, range_color=[20,80])
```

## Built-in Color Scales and Sequences (and a way to see them!)

```python
px.colors.qualitative.swatches()
```

```python
px.colors.sequential.swatches()
```

```python
px.colors.diverging.swatches()
```

```python
px.colors.cyclical.swatches()
```

```python
px.colors.colorbrewer.swatches()
```

```python
px.colors.cmocean.swatches()
```

```python
px.colors.carto.swatches()
```

# Next steps

Phew, you've made it this far! If you want to use Plotly Express yourself, just `pip install plotly_express` to install it and head on over to our [reference documentation](https://plotly.github.io/plotly_express/plotly_express/) or just copy-paste from the examples above!

```python
print(px.__version__)
```
