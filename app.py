# desc: user iface
# auth: cerebnismus
# mail: oguzhan.ince@protonmail.com

import pathlib
import sys
from typing import Any, Dict, Optional, cast
from time import sleep

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

import solara
import solara.express as solara_px  # similar to plotly express, but comes with cross filters
import solara.lab
from solara.components.columns import Columns
from solara.components.file_drop import FileDrop
from solara.website.utils import apidoc


# github_url = solara.util.github_url(__file__)
github_url = solara.util.github_url("cerebnismus/network-monitoring-ui")

# some app state that outlives a single page
app_state = solara.reactive(0)

if sys.platform != "emscripten":
    pycafe_url = solara.util.pycafe_url(path=pathlib.Path(__file__), requirements=["pandas", "plotly"])
else:
    pycafe_url = None
df_sample = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv")


class State:
    size_max = solara.reactive(40.0)
    size = solara.reactive(cast(Optional[str], None))
    color = solara.reactive(cast(Optional[str], None))
    x = solara.reactive(cast(Optional[str], None))
    y = solara.reactive(cast(Optional[str], None))
    logx = solara.reactive(False)
    logy = solara.reactive(False)
    df = solara.reactive(cast(Optional[pd.DataFrame], None))

    @staticmethod
    def load_sample():
        State.df.value = None
        State.x.value = "gdpPercap"
        State.y.value = "lifeExp"
        State.size.value = "pop"
        State.color.value = "continent"
        State.logx.value = True
        State.logx.value = True
        State.df.value = df_sample
        
        RenderLiveUpdatingComponent()

    @staticmethod
    def load_from_file(file):
        df = pd.read_csv(file["file_obj"])
        State.x.value = str(df.columns[0])
        State.y.value = str(df.columns[1])
        State.size.value = str(df.columns[2])
        State.color.value = str(df.columns[3])
        State.df.value = df

    @staticmethod
    def reset():
        State.df.value = None



@solara.component
def Page():
    df = State.df.value
    dark_effective = solara.lab.use_dark_effective()

    # the .scatter will set this cross filter
    filter, _set_filter = solara.use_cross_filter(id(df))

    # only apply the filter if the filter or dataframe changes
    def filter_df():
        if filter is not None and df is not None:
            return df.loc[filter]

    dff = solara.use_memo(filter_df, dependencies=[df, filter])


    with solara.AppBarTitle():
      solara.Text("Network Monitoring", classes=["mx-0"])

    with solara.AppBar():
        solara.lab.ThemeToggle()

    with solara.Sidebar():

        '''
        with solara.Card("", style={"max-width": "500px"}, margin=0, elevation=0, classes=["my-2"]):
            with solara.Column(style={"max-width": "400px"}):
                solara.Button(label="Components", icon_name="mdi-monitor-multiple", attributes={"target": "_blank"}, text=True, outlined=False)
                solara.Markdown(
                    f"""
                    ⚠ Development branch 
                    
                    Made at where a change was committed. 
                    Its sometimes have serious bugs. 
                    The change log may be seen on Github.
                    Let me know if you encounter any issues
                    """
                )
        '''

        with solara.Card("", margin=0, elevation=0):
            with solara.Column(style={"max-width": "400px"}):
                solara.Button(label="Manage Nodes", icon_name="mdi-network", attributes={"target": "_blank"}, text=True, outlined=False)

        with solara.Card("", margin=0, elevation=0):
            with solara.Column():
                with solara.Row():
                    solara.Button("Node Details", color="primary", text=True, outlined=True, on_click=State.load_sample, disabled=df is not None)
                    solara.Button("", icon_name="mdi-refresh", text=True, outlined=True, on_click=State.reset)
                with solara.Row():
                    solara.Button("Add", color="primary", text=True, outlined=True, on_click=State.reset)
                    solara.Button("Edit", color="info", text=True, outlined=True, on_click=State.reset)
                    solara.Button("Delete", color="error", text=True, outlined=True, on_click=State.reset)

                if sys.platform != "emscripten":
                    FileDrop(on_file=State.load_from_file, on_total_progress=lambda *args: None, label="Drag File Here * Bulk Node Operations")
                else:
                    solara.Info("File upload not supported in this environment")

                if df is not None:
                    solara.SliderFloat(label="Size", value=State.size_max, min=1, max=100)
                    solara.Checkbox(label="Log x", value=State.logx)
                    solara.Checkbox(label="Log y", value=State.logy)
                    columns = list(map(str, df.columns))
                    solara.Select("Column x", values=columns, value=State.x)
                    solara.Select("Column y", values=columns, value=State.y)
                    solara.Select("Size", values=columns, value=State.size)
                    solara.Select("Color", values=columns, value=State.color)
                    if filter is None:
                        solara.Info("If you select points in the scatter plot, you can download the points here.")
                    else:

                        def get_data():
                            return dff.to_csv(index=False)

                        solara.FileDownload(get_data, label=f"Download {len(dff):,} selected points", filename="selected.csv")


        with solara.Card("", style={"max-width": "500px"}, margin=0, elevation=0, classes=["my-2"]):
            with solara.Column(style={"max-width": "400px"}):
                solara.Button(label="Network Discovery", icon_name="mdi-lan", attributes={"target": "_blank"}, text=True, outlined=False)



                solara.Button(label="Increment app_state", icon_name="mdi-plus", on_click=lambda: app_state.set(app_state.value + 1), outlined=False)
                solara.Markdown(
                    f"""
                    This component 🤘 uses the `app_state` [reactive variable](https://solara.dev/documentation/api/utilities/reactive)
                    so that the state outlives each page. [app_state: {app_state.value}]
                    """
                )

                if sys.platform != "emscripten":
                    solara.Button(
                        label="Edit this app live on py.cafe",
                        icon_name="mdi-coffee-to-go-outline",
                        attributes={"href": pycafe_url, "target": "_blank"},
                        text=True,
                        outlined=True,
                    )

    if df is not None:
        with solara.Column(style={"max-width": "1400px"}):
            with solara.Row():
                RenderLiveUpdatingComponent()
                RenderLiveUpdatingComponent()
                RenderLiveUpdatingComponent() 

        with solara.Column(style={"max-width": "1400px"}):
            with Columns(widths=[2, 4]):
                # RenderLiveUpdatingComponent()
                if State.x.value and State.y.value:
                    solara_px.scatter(
                        df,
                        State.x.value,
                        State.y.value,
                        size=State.size.value,
                        color=State.color.value,
                        size_max=State.size_max.value,
                        log_x=State.logx.value,
                        log_y=State.logy.value,
                        template="plotly_dark" if dark_effective else "plotly_white",
                    )
                else:
                    solara.Warning("Select x and y columns")

    else: # HOME SCREEN
        solara.Info("Development branch 👊👊")

    # STATIC FOOTAGE ADDITION
    with solara.Column(style={"max-width": "400px"}):
        with solara.Row():
            solara.Button(label="View code", icon_name="mdi-github-circle", attributes={"href": github_url, "target": "_blank"}, text=True, outlined=True)
            if sys.platform != "emscripten":
                solara.Button(
                    label="Edit code",
                    icon_name="mdi-coffee-to-go-outline",
                    attributes={"href": pycafe_url, "target": "_blank"},
                    text=True,
                    outlined=True,
                )


@solara.component
def RenderLiveUpdatingComponent():

    # define some state which will be updated regularly in a separate thread
    counter = solara.use_reactive(0)

    def render():
        """Infinite loop regularly mutating counter state"""
        while True:
            sleep(0.2)
            counter.value += 1

    # run the render loop in a separate thread
    result: solara.Result[bool] = solara.use_thread(render)
    if result.error:
        raise result.error

    # create the LiveUpdatingComponent, this component depends on the counter
    # value so will be redrawn whenever counter value changes
    LiveUpdatingComponent(counter.value)


@solara.component
def LiveUpdatingComponent(counter):
    """Component which will be redrawn whenever the counter value changes."""
    fig, ax = plt.subplots()
    ax.plot(np.arange(10), np.random.random(10))
    solara.FigureMatplotlib(fig)


@solara.component
def Layout(children):
    """Function for multi page but I do not prefer."""
    route, routes = solara.use_route()
    dark_effective = solara.lab.use_dark_effective()
    return solara.AppLayout(children=children, toolbar_dark=dark_effective, color=None)  # if dark_effective else "primary")
