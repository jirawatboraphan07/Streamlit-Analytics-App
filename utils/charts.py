
import plotly.express as px
import pandas as pd

def line(df: pd.DataFrame, x, y, color=None, title=None):
    return px.line(df, x=x, y=y, color=color, title=title)

def bar(df: pd.DataFrame, x, y, color=None, title=None, barmode="group"):
    return px.bar(df, x=x, y=y, color=color, title=title, barmode=barmode)

def scatter(df: pd.DataFrame, x, y, color=None, size=None, title=None):
    return px.scatter(df, x=x, y=y, color=color, size=size, title=title)

def heatmap_from_corr(corr, title=None):
    import plotly.graph_objects as go
    fig = go.Figure(data=go.Heatmap(
        z=corr.values,
        x=corr.columns,
        y=corr.index
    ))
    fig.update_layout(title=title or "Correlation Heatmap")
    return fig
