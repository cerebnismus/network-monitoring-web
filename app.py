# desc: user iface
# auth: cerebnismus
# mail: oguzhan.ince@protonmail.com

# deps: solara:1.37.0 solara_enterprise:1.37.0
# deps: httpx authlib numpy pandas plotly matplotlib typing

import sys
import pathlib
import pprint
from types import ModuleType
from time import sleep
from typing import Any, Dict, Optional, cast

import plotly
import numpy as np
import pandas as pd
import reacton.ipyvuetify as v
from matplotlib import pyplot as plt

import solara
import solara.lab
import solara.express as solara_px  # similar to plotly express, but comes with cross filters

from solara.components.columns import Columns
from solara.components.file_drop import FileDrop

from solara.website.utils import apidoc
from solara_enterprise.search.search import Search

auth: Optional[ModuleType]
try:
    from solara_enterprise import auth
except ImportError:
    auth = None


# Custom column header info data sample
df = plotly.data.iris()

# Cross Filter Data Frame
df_gapminder = plotly.data.gapminder()


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
def UserCards():
    assert auth is not None
    user = auth.user.value
    if user:
        user_info = user.get("userinfo")
        if user_info:
            # based on https://v2.vuetifyjs.com/en/components/cards/#props

            with solara.Row():

                    with v.Card(width="400px"):
                        solara.Button(label="", icon_name="mdi-network", text=True)

                    with v.Card(width="400px"):
                        solara.Button(label="", icon_name="mdi-network", text=True)

                    with v.Card(width="300px"):
                        solara.Button(label="", icon_name="mdi-network", text=True)

                    with v.Card(width="400px"):
                        with v.ListItem(three_line=True):
                            with v.ListItemContent():
                                solara.Div("Logged in", class_="text-overline mb-4")
                                v.ListItemTitle(children=[user_info["email"]])
                                v.ListItemSubtitle(children=["You are now logged in, log out via the app bar, or the button below"])
                            with v.ListItemAvatar():
                                auth.Avatar()

                        with v.CardActions():
                            solara.Button("User Settings", icon_name="mdi-account-cog", text=True)
                            solara.Button("logout", icon_name="mdi-logout", href=auth.get_logout_url(), text=True)
        else:
            solara.Error("No user info")
    else:
        solara.Error("No user")


@solara.component
def CustomColumnHeaderInfo():
    """Use the column_header_info argument to display a custom component on the column header when the user hover above it."""
    """In this case we display the value counts for the column."""
    column_hover, set_column_hover = solara.use_state(None)

    with solara.Column(margin=4) as column_header_info:
        if column_hover:
            solara.Text("Value counts for " + column_hover)
            display(df[column_hover].value_counts())
        # if no column is hovered above, we provide an empty container
        # so we always see the triple dot icon on the column header

    solara.DataFrame(df, column_header_info=column_header_info, on_column_header_hover=set_column_hover)


@solara.component
def RenderLiveUpdatingComponent_PING():

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
    LiveUpdatingComponent_PING(counter.value)


@solara.component
def LiveUpdatingComponent_PING(counter):
    """Component which will be redrawn whenever the counter value changes."""
    fig, ax = plt.subplots()
    ax.plot(np.arange(10), np.random.random(10))
    solara.FigureMatplotlib(fig)

    # adding title and labels
    ax.set_title('Live Updating PING Chart')
    ax.set_xlabel('X-axis Label')
    ax.set_ylabel('Y-axis Label')

    # adding grid for better readability
    ax.grid(True)


@solara.component
def RenderLiveUpdatingComponent_SNMP():

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
    LiveUpdatingComponent_SNMP(counter.value)


@solara.component
def LiveUpdatingComponent_SNMP(counter):
    """Component which will be redrawn whenever the counter value changes."""
    fig, ax = plt.subplots()
    ax.plot(np.arange(10), np.random.random(10))
    solara.FigureMatplotlib(fig)

    # adding title and labels
    ax.set_title('Live Updating SNMP Chart')
    ax.set_xlabel('X-axis Label')
    ax.set_ylabel('Y-axis Label')

    # adding grid for better readability
    ax.grid(True)


@solara.component
def Layout(children):
    """Function for multi page but I do not prefer."""
    route, routes = solara.use_route()
    dark_effective = solara.lab.use_dark_effective()
    return solara.AppLayout(children=children, toolbar_dark=dark_effective, color=None)  # if dark_effective else "primary")



@solara.component
def Page():
    ############################ META ###########################
    with solara.VBox() as main:
        with solara.Head():
            solara.Title("Network Monitoring")
            solara.Meta(
                name="description",
                content="The Meta component can be used to set the description of a page. This is useful for SEO, or crawlers that index your page.",
            )
    ############################ META ###########################

    ############################ LOGIN ###########################
    assert auth is not None
    solara.Title("Login using OAuth")
    with solara.AppBar():
        solara.lab.ThemeToggle()
        if auth.user.value:
            auth.AvatarMenu()
        else:
            solara.Button(icon_name="mdi-login", href=auth.get_login_url(), icon=True)

    with solara.Column():
        if auth.user.value:
            # STATIC  HOME PAGE [USE FOR ANNOUNCEMENTS !]
            with solara.Row():
                solara.Button("", icon_name="mdi-home-outline", href="http://localhost:8765", height="48px")
                solara.Button("", icon_name="mdi-restart", height="48px", on_click=State.reset)

                with solara.Details(" 📌 This is the raw user data from the auth provider. "):
                    solara.Markdown(
                        """ 
                        ##### We use the `picture` field to display an avatar in the [AppBar](/documentation/components/layout/app_bar). 
                        *Note: do not share this data with anyone, it contains sensitive information.*
                    """
                    )
                    solara.Preformatted(pprint.pformat(auth.user.value))
        else:
            solara.Markdown(
                """
            ### Login
            ##### We are using [Auth0](https://auth0.com/) as an OAuth provider.
            ##### You can login with your google account, github account or with a username and password.
            """
            )
            with solara.Row():
                solara.Button("login", icon_name="mdi-login", href=auth.get_login_url())
    ############################ LOGIN ###########################


    ############################ AUTH ###########################
    if auth.user.value:

        df = State.df.value
        # dark_effective = solara.lab.use_dark_effective()

        # the .scatter will set this cross filter
        filter, _set_filter = solara.use_cross_filter(id(df))

        # only apply the filter if the filter or dataframe changes
        def filter_df():
            if filter is not None and df is not None:
                return df.loc[filter]

        dff = solara.use_memo(filter_df, dependencies=[df, filter])


        with solara.AppBarTitle():
            solara.Text("Network Monitoring", classes=["mx-0"])
            


        with solara.Sidebar():

            # with solara.Card("", margin=0, elevation=0):
            with v.Card(width="200px", margin=0, elevation=0):
                with solara.Column(style={"max-width": "200px"}):
                    with solara.Row():
                        solara.Button(label="Overview", icon_name="mdi-view-dashboard", attributes={"target": "_blank"}, on_click=State.load_sample, text=True, outlined=True)
                    with solara.Row():
                        solara.Button(label="Event Management", icon_name="mdi-message-text-outline", attributes={"target": "_blank"}, text=True, outlined=True)
                    with solara.Row():
                        solara.Button(label="Network Discovery", icon_name="mdi-lan", attributes={"target": "_blank"}, text=True, outlined=True)
                    with solara.Row():
                        solara.Button(label="Inventory", icon_name="mdi-hexagon-multiple", attributes={"target": "_blank"}, text=True, outlined=True)
                    with solara.Row():
                        solara.Button(label="Extensions", icon_name="mdi-orbit", attributes={"target": "_blank"}, text=True, outlined=True)
                    with solara.Row():
                        solara.Button(label="Integrations", icon_name="mdi-google-physical-web", attributes={"target": "_blank"}, text=True, outlined=True)
                    with solara.Row():
                        solara.Button(label="Configuration", icon_name="mdi-wrench", attributes={"target": "_blank"}, text=True, outlined=True)


                    '''
                    with v.Card(width="400px"):
                        solara.Button(label="Node Management", icon_name="mdi-network", text=True)
                    '''

            """
            with solara.Card("", margin=0, elevation=0):
                with solara.Column():
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
            """



        if df is not None:

            with solara.Column():
                UserCards()

                '''
                # move this to inventory onclick def
                solara.provide_cross_filter()
                with solara.VBox() as main:
                    solara.CrossFilterReport(df_gapminder, classes=["py-2"])
                    solara.CrossFilterSelect(df_gapminder, "year")
                    solara.CrossFilterSelect(df_gapminder, "country")
                    solara.CrossFilterDataFrame(df_gapminder)
                '''

                # non-filtered sheet
                with v.Card(width="800px", height="400px"):
                    solara.Markdown(
                        f"""
                        This uses the `app_state` [reactive variable](https://solara.dev/documentation/api/utilities/reactive)
                        so that the state outlives each page. [app_state: {app_state.value}]
                        """
                    )
                    CustomColumnHeaderInfo()

                with v.Card(width="800px", height="400px"):
                    with solara.Row():
                        RenderLiveUpdatingComponent_PING()
                        RenderLiveUpdatingComponent_SNMP()





        # STATIC FOOTAGE ADDITION
        with solara.Column(style={"max-width": "400px"}):
            with solara.Row():
                solara.Button(label="View code on github", icon_name="mdi-github-circle", attributes={"href": github_url, "target": "_blank"}, text=True, outlined=True)
                if sys.platform != "emscripten":
                    solara.Button(
                        label="Edit code on py.cafe",
                        icon_name="mdi-coffee-to-go-outline",
                        attributes={"href": pycafe_url, "target": "_blank"},
                        text=True,
                        outlined=True,
                    )
        with solara.Column():
            with solara.Row():
                solara.Markdown(""" *Note: do not share this data with anyone, it contains sensitive information.* """)

    #    return main

if auth is None:
    del Page

