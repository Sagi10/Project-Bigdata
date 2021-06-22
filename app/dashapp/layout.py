import dash_core_components as dcc
from dash_extensions import Download
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash_html_components.Hr import Hr
import pandas as pd
from app.dashapp.helpers import perform_query

# Navbar Component
PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"
navbar = dbc.Navbar(
    [
        html.A(
            # Use row and col to control vertical alignment of logo / brand
            dbc.Row(
                [
                    dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),
                    dbc.Col(dbc.NavbarBrand("IDO-LAAD Reporting", className="ml-2", style={'font-size': '23px'})),
                ],
                align="center",
                no_gutters=True,
            ),
            href="/",
        ),
        dbc.NavLink("Logout", href="/logout"),
    ],
    color="#367fa9",
    dark=True,
)


# Setup the Layout and send back to __init__.py to create Dash App
def get_Layout(db):
    # for now hardcoded query for testing.
    allStates = perform_query('SELECT distinct(State) FROM CHG_SNP_LOCATION_TIME_COMBI', db)
    allCities = perform_query('SELECT distinct(City) FROM CHG_SNP_LOCATION_TIME_COMBI', db)
    allDistricts = perform_query('SELECT DISTINCT(District) FROM CHG_SNP_LOCATION_TIME_COMBI',
                                 db)
    allStates.sort()
    allCities.sort()
    allDistricts.sort()
    allStates.insert(0, 'Alle')
    allCities.insert(0, 'Alle')
    allDistricts.insert(0, 'Alle')

    return html.Div([
        # Navbar
        html.Div([
            navbar
        ], className='row', style={'background': '#3c8dbc'}),

        # Main Row / Grid
        html.Div([

            # Div for dropdowns, location filtering
            html.Div([
                html.Label('Provincie', className='text-light font-weight-bold m-2'),
                dcc.Dropdown(
                    id='dropdown-provincie',
                    options=
                    [{'label': state, 'value': state} for state in allStates],
                    value='NH',
                    multi=True,
                    className='text-dark m-2'
                ),
                html.Label('Gemeente', className='text-light font-weight-bold m-2'),
                dcc.Dropdown(
                    id='dropdown-gemeente',
                    options=
                    [{'label': city, 'value': city} for city in allCities]
                    ,
                    value='Amsterdam',
                    multi=True,
                    className='text-dark m-2'
                ),
                html.Label('Deelgemeente/Stadsdeel', className='text-light font-weight-bold m-2'),
                dcc.Dropdown(
                    id='dropdown-deelgemeente',
                    options=
                    [{'label': district, 'value': district} for district in allDistricts]
                    ,
                    multi=True,
                    className='text-dark m-2'
                ),
                html.Label('Plaats/wijk', className='text-light font-weight-bold m-2'),
                dcc.Dropdown(
                    id='dropdown-plaats',
                    options=[],
                    multi=True,
                    className='text-dark m-2'
                ),
                html.Label('Buurt', className='text-light font-weight-bold m-2'),
                dcc.Dropdown(
                    id='dropdown-buurt',
                    options=[],
                    multi=True,
                    className='text-dark m-2'
                ),
                html.Label('SubBuurt', className='text-light font-weight-bold m-2'),
                dcc.Dropdown(
                    id='dropdown-subbuurt',
                    options=[],
                    multi=True,
                    className='text-dark m-2'
                ),
                html.Label('Adres', className='text-light font-weight-bold m-2'),
                dcc.Dropdown(
                    id='dropdown-adres',
                    options=[],
                    multi=True,
                    className='text-dark m-2'
                ),
                html.Label('Laadstations', className='text-light font-weight-bold m-2'),
                dcc.Dropdown(
                    id='dropdown-laadstations',
                    options=[],
                    multi=True,
                    className='text-dark m-2'
                ),
                html.Br(),
                dcc.Checklist(
                    id='snellaad',
                    options=[
                        {'label': 'Alleen Snelladers', 'value': 'SNELLADERS'},
                    ],
                    style={'color': 'white'},
                    className='m-2'
                ),
                html.Button('Selectie wissen', id='selectieWissen', className='btn btn-secondary m-2', n_clicks=0),
            ], className='col-md-2 bg-dark'),

            # Graphs
            html.Div([

                # Tabs and Plots
                html.Div([
                    html.Div(
                        dcc.Tabs(id='tabs', vertical=False, value='kpi', children=[
                            dcc.Tab(label='KPI laadpunten', value='kpi',
                                    children=[dcc.Tabs(id='subtabsKPI', vertical=False, value='kwh',
                                                       children=[
                                                           dcc.Tab(label='Som kWh', value='kwh',
                                                                   className='detail-tabs',
                                                                   selected_className='detail-tabs--selected'),
                                                           dcc.Tab(label='Aantal Sessies', value='sessies',
                                                                   className='detail-tabs',
                                                                   selected_className='detail-tabs--selected'),
                                                           dcc.Tab(label="Aantal Unieke RFID's", value='rfdi',
                                                                   className='detail-tabs',
                                                                   selected_className='detail-tabs--selected'),
                                                           dcc.Tab(label="Maandelijks gemiddelde kWh per laadstation",
                                                                   value='gemmideld',
                                                                   className='detail-tabs',
                                                                   selected_className='detail-tabs--selected'),
                                                           dcc.Tab(label="% sessies >24uur", value='klevers',
                                                                   className='detail-tabs',
                                                                   selected_className='detail-tabs--selected'),
                                                           dcc.Tab(label="Aantal vaste bezoekers",
                                                                   value='vasteBezoekers',
                                                                   className='detail-tabs',
                                                                   selected_className='detail-tabs--selected'),
                                                       ])
                                              ], className='KPI-tabs', selected_className='KPI-tabs--selected'),
                            dcc.Tab(label='Bezettingsgraad', value='bez',
                                    children=[dcc.Tabs(id='subtabsBez', vertical=False, value='bezSub',
                                                       children=[
                                                           dcc.Tab(label='Maandelijks %', value='1',
                                                                   className='detail-tabs',
                                                                   selected_className='detail-tabs--selected'),
                                                           dcc.Tab(label='Maandelijkse uur % ', value='2',
                                                                   className='detail-tabs',
                                                                   selected_className='detail-tabs--selected'),
                                                           dcc.Tab(label="Maandelijks uur % per werkdag", value='3',
                                                                   className='detail-tabs',
                                                                   selected_className='detail-tabs--selected'),
                                                           dcc.Tab(label="Jaarlijks uur %", value='4',
                                                                   className='detail-tabs',
                                                                   selected_className='detail-tabs--selected'),
                                                           dcc.Tab(label="Jaarlijks uur % per werkdag", value='5',
                                                                   className='detail-tabs',
                                                                   selected_className='detail-tabs--selected'),
                                                       ])
                                              ], className='KPI-tabs', selected_className='KPI-tabs--selected'),
                            dcc.Tab(label='Tops en Flops', value='top',
                                    children=[dcc.Tabs(id='subtabsTop', vertical=False, value='topSub',
                                                       children=[
                                                           dcc.Tab(label='Top of Flop', value='1',
                                                                   className='detail-tabs',
                                                                   selected_className='detail-tabs--selected'),
                                                       ])
                                              ], className='KPI-tabs', selected_className='KPI-tabs--selected'),
                            dcc.Tab(label='Aantal laadpunten', value='laad',
                                    children=[dcc.Tabs(id='subtabsPunt', vertical=False, value='laadSub',
                                                       children=[
                                                           dcc.Tab(label='Aantal laadpunten per maand', value='1',
                                                                   className='detail-tabs',
                                                                   selected_className='detail-tabs--selected'),
                                                           dcc.Tab(label='Aantal laadpunten per jaar', value='2',
                                                                   className='detail-tabs',
                                                                   selected_className='detail-tabs--selected'),
                                                           dcc.Tab(
                                                               label="Voorschrijnend gemiddelde aantal laadpunten per maand",
                                                               value='3',
                                                               className='detail-tabs',
                                                               selected_className='detail-tabs--selected'),
                                                       ])
                                              ], className='KPI-tabs', selected_className='KPI-tabs--selected'),
                            dcc.Tab(label='Download', value='download',
                                    children=[dcc.Tabs(id='subtabsLoad', vertical=False, value='downSub',
                                                       children=[
                                                           dcc.Tab(label='KPI Laadpunt', value='1',
                                                                   className='detail-tabs',
                                                                   selected_className='detail-tabs--selected'),
                                                           dcc.Tab(label='Bezettingsgraad', value='2',
                                                                   className='detail-tabs',
                                                                   selected_className='detail-tabs--selected'),
                                                           dcc.Tab(label='Tableau data', value='3',
                                                                   className='detail-tabs',
                                                                   selected_className='detail-tabs--selected'),
                                                       ])
                                              ], className='KPI-tabs', selected_className='KPI-tabs--selected'),
                            dcc.Tab(label='Ingeladen data', value='inlaad',
                                    children=[dcc.Tabs(id='subtabsGeladen', vertical=False, value='geladenSub',
                                                       children=[
                                                           dcc.Tab(label='Maandelijkse data files', value='1',
                                                                   className='detail-tabs',
                                                                   selected_className='detail-tabs--selected'),
                                                           dcc.Tab(label='Dagelijkse data files', value='2',
                                                                   className='detail-tabs',
                                                                   selected_className='detail-tabs--selected'),
                                                           dcc.Tab(label='Export/berekende datums vanuit DWH',
                                                                   value='3',
                                                                   className='detail-tabs',
                                                                   selected_className='detail-tabs--selected'),
                                                       ])
                                              ], className='KPI-tabs', selected_className='KPI-tabs--selected'),
                            dcc.Tab(label='Publicatie data', value='publiek',
                                    children=[dcc.Tabs(id='subtabsPubliek', vertical=False, value='publiekData',
                                                       children=[
                                                           dcc.Tab(label='Jaar totaal kWh', value='1',
                                                                   className='detail-tabs',
                                                                   selected_className='detail-tabs--selected'),
                                                           dcc.Tab(label='Jaar totaal aantal sessies', value='2',
                                                                   className='detail-tabs',
                                                                   selected_className='detail-tabs--selected'),
                                                           dcc.Tab(label='Jaar totaal gesignaleerde laadpunten',
                                                                   value='3',
                                                                   className='detail-tabs',
                                                                   selected_className='detail-tabs--selected'),
                                                           dcc.Tab(label='Jaar totaal unieke RFIDs', value='4',
                                                                   className='detail-tabs',
                                                                   selected_className='detail-tabs--selected'),
                                                       ])
                                              ], className='KPI-tabs', selected_className='KPI-tabs--selected'),
                            dcc.Tab(label='KPI-definities', value='def',
                                    children=[dcc.Tabs(id='subtabsDef', vertical=False, value='defData',
                                                       children=[
                                                           dcc.Tab(label='KPI-definities', value='1',
                                                                   className='detail-tabs',
                                                                   selected_className='detail-tabs--selected'),
                                                       ])
                                              ], className='KPI-tabs', selected_className='KPI-tabs--selected'),
                        ], className='col-sm-auto'),
                    ),
                    html.Hr(),

                    # Years selection and Toon grafiek Button
                    html.Div([
                        html.Label('Aantal getoonde jaren', style={"font-weight": "bold"}),
                        dcc.Dropdown(
                            id='yearsCount',
                            options=[{'label': i + 1, 'value': i + 1, } for i in range(12)],
                            # List comprehesion, values 1-12
                            searchable=False,  # Disable Search
                            clearable=False,
                            # placeholder="Kies jaar",
                            value='1',
                        ),
                    ], className='col-md-3 mr-5'),

                    html.Button('Toon Grafiek', id='toonGrafiek', className='btn btn-secondary m-1', n_clicks=0),

                    # Here is where the graphs comes and the table
                    html.Div(id='tabs-content'),  # Graphs
                    html.Div(className='hrCustom'),  # Custom Horitzontal Line
                    html.Div([  # Download buttons Csv and Excell
                        html.Button('CSV', id='toCsv', className='btn btn-info m-1', n_clicks=0),
                        html.Button('Excel', id='toExcel', className='btn btn-info m-1', n_clicks=0),
                    ], className='downloadSection'),
                    html.Div(id='graph-table'),  # Table

                    dcc.Store(id='intermediate-value'),
                    # Hidden div to store the finalDataFrame produced when 'Toon Grafiek' is pressed, this for the download
                    Download(id="download")  # Download dash component

                ], className='col-12 mt-2')

            ], className='col-md-10'),

        ], className='row'),
    ], className='container-fluid')
