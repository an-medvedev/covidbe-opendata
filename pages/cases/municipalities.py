import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from flask_babel import get_locale, gettext, lazy_gettext

from graphs.cases_per_municipality import map_communes, barplot_communes, map_communes_per_inhabitant
from pages import AppLink
from pages.sources import *


def municipalities():
    return [
        html.H2(gettext("Municipalities")),
        html.H3(gettext("Where are the epidemic focuses?")),
        dcc.Graph(id='cases-overview-map-communes-p', figure=map_communes_per_inhabitant(), config=dict(locale=str(get_locale()))),
        html.H3(gettext("Cases per municipality")),
        html.H4(gettext("Click on a municipality to see a plot of its cases over time")),
        dbc.Row([
            dbc.Col(dcc.Graph(id='cases-overview-map-communes', figure=map_communes(),
                              config=dict(locale=str(get_locale()))))
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(id='cases-overview-histogram', figure=barplot_communes(),
                              style={"display": "none"}, config=dict(locale=str(get_locale()))))
        ]),
        display_source_providers(source_sciensano, source_map_communes, source_pop)
    ]


def municipalities_callbacks(app):
    @app.callback(
        Output("cases-overview-histogram", "figure"),
        [Input('cases-overview-map-communes', 'clickData')])
    def callback_barplot(clickData):
        if clickData is None:
            return barplot_communes()
        nis = clickData['points'][0]['customdata'][2]
        return barplot_communes(commune_nis=nis)

    @app.callback(
        Output("cases-overview-histogram", "style"),
        [Input('cases-overview-map-communes', 'clickData')])
    def callback_barplot_style(clickData):
        if clickData is None:
            return {"display": "none"}
        return {"display": "block"}


municipalities_link = AppLink(lazy_gettext("Per municipality"), "/municipalities", municipalities, municipalities_callbacks)