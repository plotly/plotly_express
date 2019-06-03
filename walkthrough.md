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

# Plotly Express: a Walkthrough

This notebook is the executable version of the example we walk through in our [Medium announcement article](https://medium.com/@plotlygraphs/introducing-plotly-express-808df010143d) introducing [Plotly Express](https://plotly.github.io/plotly_express): a terse, consistent, high-level wrapper around Plotly.py for rapid data exploration and figure generation.


Once you import Plotly Express (aka `px`), most plots are made with just one function call that accepts a [tidy Pandas data frame](http://www.jeannicholashould.com/tidy-data-in-python.html), and a simple description of the plot you want to make. For example if you want a simple scatter plot, it’s just `px.scatter(data, x="column_name", y="column_name")`. Here’s an example with the [Gapminder dataset](https://www.gapminder.org/tools/#$state$time$value=2007;;&chart-type=bubbles) – which comes built-in! – showing life expectancy vs GPD per capita by country for 2007:


```python
import plotly_express as px
gapminder = px.data.gapminder()
gapminder2007 = gapminder.query("year == 2007")

px.scatter(gapminder2007, x="gdpPercap", y="lifeExp")
```

If you want to break that down by continent, you can color your points with the `color` argument and `px` takes care of the details:

```python
px.scatter(gapminder2007, x="gdpPercap", y="lifeExp", color="continent")
```

Each point here is a country, so maybe we want to scale the points by the country population… no problem: there’s an arg for that too!


```python
px.scatter(gapminder2007, x="gdpPercap", y="lifeExp", color="continent", size="pop", size_max=60)
```

Curious about which point is which country? Add a `hover_name` and you can easily identify any point: never again wonder “what *is* that outlier?”... just mouse over the point you're interested in!

```python
px.scatter(gapminder2007, x="gdpPercap", y="lifeExp", color="continent", size="pop", size_max=60, hover_name="country")
```

You could facet your plots, just as easily as coloring your points with `facet_col="continent"`, and let's make the x-axis logarithmic to see things more clearly.

```python
px.scatter(gapminder2007, x="gdpPercap", y="lifeExp", color="continent", size="pop", size_max=60,
          hover_name="country", facet_col="continent", log_x=True)
```

Maybe you're interested in more than just 2007 and you want to see how this chart evolved over time. You can animate it by setting `animation_frame="year"` and `animation_group="country"` to identify which circles match which ones across frames. In this final version, let's tweak some of the display here, as text like "gdpPercap" is kind of ugly even though it's the name of our data frame column. We can provide prettier `labels` that get applied throughout the figure, in legends, axis titles and hovers. We can also provide some manual bounds so the animation looks nice throughout:

```python
px.scatter(gapminder, x="gdpPercap", y="lifeExp",size="pop", size_max=60, color="continent", hover_name="country",
           animation_frame="year", animation_group="country", log_x=True, range_x=[100,100000], range_y=[25,90],
           labels=dict(pop="Population", gdpPercap="GDP per Capita", lifeExp="Life Expectancy"))
```

Because this is geographic data, we can also represent it as an animated map, which makes it clear that `px` can make way more than just scatterplots, and that this dataset is missing data for the former Soviet Union.

```python
px.choropleth(gapminder, locations="iso_alpha", color="lifeExp", hover_name="country", animation_frame="year",
              color_continuous_scale=px.colors.sequential.Plasma, projection="natural earth")
```

A major part of data exploration is understanding the distribution of values in a dataset, and how those distributions relate to each other. Plotly Express includes a number of functions to do just that.
Visualize univariate distributions with histograms, box-and-whisker or violin plots:

```python
tips = px.data.tips()
```

```python
px.histogram(tips, x="total_bill", y="tip", histfunc="sum", color="smoker")
```

```python
px.box(tips, x="total_bill", y="day", orientation="h", color="smoker", notched=True,
       category_orders={"day": ["Thur", "Fri", "Sat", "Sun"]})
```

```python
px.violin(tips, y="tip", x="smoker", color="sex", box=True, points="all")
```

You can also visualize bivariate distributions with marginal rugs, histograms, boxes or violins, and you can add trendlines too. px even helpfully adds the line's equation and R² in the hover box for you! It uses `statsmodels` under the hood to do either Ordinary Least Squares (OLS) regression or Locally Weighted Scatterplot Smoothing (LOWESS).

```python
px.scatter(tips, x="total_bill", y="tip", color="smoker", trendline="ols", marginal_x="violin", marginal_y="box")
```

# Next steps

Phew, you've made it this far! If you want to use Plotly Express yourself, just `pip install plotly_express` to install it and head on over to our [reference documentation](https://plotly.github.io/plotly_express/plotly_express/) or just copy-paste from the examples above!

Or you could go back to our [Medium announcement article](https://medium.com/@plotlygraphs/introducing-plotly-express-808df010143d) for more details on this library.

```python
print(px.__version__)
```
