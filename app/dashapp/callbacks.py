import datetime
from dash.dependencies import Input, Output
from dash_extensions.snippets import send_data_frame
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import dash
from dash.exceptions import PreventUpdate
from app.dashapp.helpers import call_stored_procedure, filter_dropdown, create_data_table, \
    filter_location_and_add_bartrace, get_all_values


# Function that handles all functions within the dash application
def register_callbacks(dashapp, db):
    bridge_location = db.Table('CHG_SNP_LOCATION_TIME_COMBI', db.metadata, autoload=True, autoload_with=db.engine)  # Receive table one from database in the String
    results = db.session.query(bridge_location).all()                                                               # equal to 'SELECT * FROM CHG_BRIDGE_LOCATION_CHARGEPOINT'
    df = pd.DataFrame(results)                                                                                      # Convert Result into Datatype pandas DataFrame
   
    # Query Data by calling the Stored procedure with default year parameter
    function_name = 'CHG_09_LOCATION_TIME_COMBI'
    params = [9, 1, 1]
    kpiData = call_stored_procedure(db, function_name, params)
    # OPTIONAL: When Quering show loading Icon

    # Renders filter content to fill graphs and tables
    @dashapp.callback(
        [Output('tabs-content', 'children'), Output('graph-table', 'children'), Output('intermediate-value', 'data')],
        [Input('tabs', 'value'),
         Input('subtabsBez', 'value'),
         Input('subtabsKPI', 'value'),
         Input('toonGrafiek', 'n_clicks'),
         Input('yearsCount', 'value'),
         Input(component_id='dropdown-deelgemeente', component_property='value'),
         Input(component_id='dropdown-plaats', component_property='value'),
         Input(component_id='dropdown-buurt', component_property='value'),
         Input(component_id='dropdown-subbuurt', component_property='value'),
         Input(component_id='dropdown-adres', component_property='value'),
         Input(component_id='dropdown-laadstations', component_property='value'),
         Input(component_id='snellaad', component_property='value')])
    def render_content(mainTab, tabBez, tab, toonGrafiekButton, yearsCount, deelgemeente, plaats, buurt, subbuurt,
                       adres, laadstations,
                       snellaad):

        data = kpiData
        # Only calls stored procedure again if multiple years shown are required to improve application speed
        if (yearsCount != '1'):
            print("Changed Year")
            params = [9, 1, yearsCount]
            data = call_stored_procedure(db, function_name, params)
            # OPTIONAL: When Quering show loading Icon 

        # If Button with id toonGrafiek is pressed load the graph and table
        changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
        if 'toonGrafiek' in changed_id:

            if tabBez == '1' and mainTab == 'bez':
                fig = go.Figure()
                finalDataframe = filter_location_and_add_bartrace(deelgemeente, plaats, buurt, subbuurt, adres,
                                                                  laadstations, data, 'MonthlyOccupancyPercentage', fig)
                fig.update_layout(barmode='group', title_text='Maandelijkse bezettingsgraad',
                                  xaxis={'categoryorder': 'category ascending'})

                # Create alternate dataframe for y axis range
                dfYAxis = finalDataframe[finalDataframe[
                                             'YearMonth'] != 'Alle']  # Exclude year sum amount
                axis_req_column = dfYAxis["MonthlyOccupancyPercentage"]
                axis_req_value = axis_req_column.max() * 1.05  # Small addition to max value for increasing y axis range slightly
                fig.update_traces(hovertemplate='Bezettingsgraad: %%{y}')
                fig.update_layout(barmode='group', title_text='Maandelijkse bezettingsgraad', title_x=0.5,
                                  xaxis=dict(
                                      {'categoryorder': 'category ascending'},
                                      tickformat='%Y-%B',
                                      dtick='M1'),
                                  yaxis=dict(
                                      dtick=axis_req_value / 5 # Specify Y axis ticks
                                  ),
                                  yaxis_range=[0, axis_req_value],
                                  hovermode='x',
                                  template="plotly_white")  # Layout of the figure/bar chart

                # Return the graph_object (go) Figure/Bar chart and the datatable
                return html.Div([
                    dcc.Graph(
                        id='graph-month1',
                        figure=fig
                    ),
                ]), create_data_table(
                    finalDataframe), finalDataframe.to_json(date_format='iso', orient='split')

            if tab == 'kwh' and mainTab == 'kpi':
                fig = go.Figure()
                finalDataframe = filter_location_and_add_bartrace(deelgemeente, plaats, buurt, subbuurt, adres,
                                                                  laadstations, data, 'SumKwh',
                                                                  fig)  # Proces the Location Filter Dataframe
                # Create alternate dataframe for y axis range
                dfYAxis = finalDataframe[finalDataframe[
                                             'YearMonth'] != 'Alle']  # Exclude year sum amount
                axis_req_column = dfYAxis["SumKwh"]
                axis_req_value = axis_req_column.max() * 1.05  # Small addition to max value for increasing y axis range slightly
                fig.update_traces(hovertemplate='Som Kwh: %{y}')
                fig.update_layout(barmode='group', title_text='Som Kwh', title_x=0.5,
                                  xaxis=dict(
                                      {'categoryorder': 'category ascending'},
                                      tickformat='%Y-%B',
                                      dtick='M1'),
                                  yaxis=dict(
                                      dtick=axis_req_value / 5 # Specify Y axis ticks
                                  ),
                                  yaxis_range=[0, axis_req_value],
                                  hovermode='x')  # Layout of the figure/bar chart
                # Return the graph_object (go) Figure/Bar chart and the datatable
                return html.Div([
                    dcc.Graph(
                        id='graph-kwi-tabs',
                        figure=fig
                    )
                ]), create_data_table(finalDataframe), finalDataframe.to_json(date_format='iso',
                                                                              orient='split')  # Finally put the Dataframe object in the method create_data_table() to create a table under the graph and save finalDataframe in hidden div intermediate-value

            elif tab == 'sessies':
                fig = go.Figure()
                finalDataframe = filter_location_and_add_bartrace(deelgemeente, plaats, buurt, subbuurt, adres,
                                                                  laadstations, data, 'NumberOfSessions', fig)
                dfYAxis = finalDataframe[finalDataframe['YearMonth'] != 'Alle']
                axis_req_column = dfYAxis["NumberOfSessions"]
                axis_req_value = axis_req_column.max() * 1.05
                fig.update_traces(hovertemplate='Aantal sessies: %{y}')
                fig.update_layout(barmode='group', title_text='Aantal Sessies', title_x=0.5,
                                  xaxis=dict(
                                      {'categoryorder': 'category ascending'},
                                      tickformat='%Y-%B',
                                      dtick='M1'),
                                  yaxis=dict(
                                      dtick=axis_req_value / 5
                                  ),
                                  yaxis_range=[0, axis_req_value],
                                  hovermode='x')
                return html.Div([
                    dcc.Graph(
                        id='graph-sessies',
                        figure=fig
                    )
                ]), create_data_table(finalDataframe), finalDataframe.to_json(date_format='iso', orient='split')
            elif tab == 'rfdi':

                fig = go.Figure()
                finalDataframe = filter_location_and_add_bartrace(deelgemeente, plaats, buurt, subbuurt, adres,
                                                                  laadstations, data, 'NumberOfUniqueRFIDs', fig)
                dfYAxis = finalDataframe[finalDataframe['YearMonth'] != 'Alle']
                axis_req_column = dfYAxis["NumberOfUniqueRFIDs"]
                axis_req_value = axis_req_column.max() * 1.05
                fig.update_traces(hovertemplate='Aantal unieke RFIDs: %{y}')
                fig.update_layout(barmode='group', title_text='Aantal unieke RFIDs', title_x=0.5,
                                  xaxis=dict(
                                      {'categoryorder': 'category ascending'},
                                      tickformat='%Y-%B',
                                      dtick='M1'),
                                  yaxis=dict(
                                      dtick=axis_req_value / 5
                                  ),
                                  yaxis_range=[0, axis_req_value],
                                  hovermode='x')
                return html.Div([
                    dcc.Graph(
                        id='graph-rfdi',
                        figure=fig
                    )
                ]), create_data_table(finalDataframe), finalDataframe.to_json(date_format='iso', orient='split')
            elif tab == 'gemmideld':

                fig = go.Figure()
                finalDataframe = filter_location_and_add_bartrace(deelgemeente, plaats, buurt, subbuurt, adres,
                                                                  laadstations, data, 'AverageKwhChargeStation', fig)
                dfYAxis = finalDataframe[finalDataframe['YearMonth'] != 'Alle']
                axis_req_column = dfYAxis["AverageKwhChargeStation"]
                axis_req_value = axis_req_column.max() * 1.05
                fig.update_traces(hovertemplate='Gemiddeld kWh per laadstation: %{y}')
                fig.update_layout(barmode='group', title_text='Gemiddelde kWh in een sessie per laadstation',
                                  title_x=0.5,
                                  xaxis=dict(
                                      {'categoryorder': 'category ascending'},
                                      tickformat='%Y-%B',
                                      dtick='M1'),
                                  yaxis=dict(
                                      dtick=axis_req_value / 5
                                  ),
                                  yaxis_range=[0, axis_req_value],
                                  hovermode='x')
                return html.Div([
                    dcc.Graph(
                        id='graph-gemiddeld',
                        figure=fig
                    )
                ]), create_data_table(finalDataframe), finalDataframe.to_json(date_format='iso', orient='split')
            elif tab == 'klevers':
                fig = go.Figure()
                finalDataframe = filter_location_and_add_bartrace(deelgemeente, plaats, buurt, subbuurt, adres,
                                                                  laadstations, data, 'NumberOfStickySessions', fig)
                dfYAxis = finalDataframe[finalDataframe['YearMonth'] != 'Alle']
                axis_req_column = dfYAxis["NumberOfStickySessions"]
                axis_req_value = axis_req_column.max()
                fig.update_traces(hovertemplate='Percentage Kleefsessies: %%{y}')
                fig.update_layout(barmode='group', title_text='& sessies > 24', title_x=0.5,
                                  xaxis=dict(
                                      {'categoryorder': 'category ascending'},
                                      tickformat='%Y-%B',
                                      dtick='M1'),
                                  yaxis=dict(
                                      dtick=axis_req_value / 5
                                  ),
                                  yaxis_range=[0, axis_req_value],
                                  hovermode='x')
                return html.Div([
                    dcc.Graph(
                        id='graph-klever',
                        figure=fig
                    )
                ]), create_data_table(finalDataframe), finalDataframe.to_json(date_format='iso', orient='split')
            elif tab == 'vasteBezoekers':
                return html.Div([
                    dcc.Graph(
                        id='graph-2-tabs',
                        figure={
                            'data': [{
                                'x': [6, 12, 23],
                                'y': [7, 10, 36],
                                'type': 'bar'
                            }],
                            'layout': {
                                'title': 'Vaste Bezoekers'
                            }
                        },

                    )
                ]), create_data_table(test_df), test_df.to_json(date_format='iso', orient='split')

        else:
            raise PreventUpdate

    # Download CSV Callback 
    @dashapp.callback(Output("download", "data"),
                      [Input('intermediate-value', 'data'),
                       Input('toCsv', 'n_clicks'),
                       Input('toExcel', 'n_clicks')])
    def downloadData(jsonified_cleaned_data, toCsv, toExcel):
        if jsonified_cleaned_data is not None:
            dff = pd.read_json(jsonified_cleaned_data, orient='split')
            changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
            if 'toCsv' in changed_id:
                # Download Csv button is pressed and download as CSV
                return send_data_frame(dff.to_csv, filename="IDO-LAAD Reporting ServiceCSV.csv", index=False)
            elif 'toExcel' in changed_id:
                # Download Excell button is pressed and download as Excell
                return send_data_frame(dff.to_excel, filename="IDO-LAAD Reporting ServiceExcell.xlsx", index=False)
        return ''  # Emtpy Output

    # Multiple callbacks to change filter options responsively
    @dashapp.callback(
        Output(component_id='dropdown-plaats', component_property='options'),
        Input(component_id='dropdown-provincie', component_property='value'),
        Input(component_id='dropdown-gemeente', component_property='value'),
        Input(component_id='dropdown-deelgemeente', component_property='value')
    )
    def set_dropdown_plaatswijk(provincie, gemeente, deelgemeente):
        if deelgemeente is None:
            raise PreventUpdate
        if str(deelgemeente) == "['Alle']":
            results = list(df.loc[:, 'SubDistrict'].unique())

            # this is the list that contains all the values when 'Alle' is selected.
            alle_deelgemeentes = list(df.loc[:, 'District'].unique())

            results.insert(0, 'Alle')
            return [{'label': i, 'value': i} for i in results]
        else:
            alle_deelgemeentes = deelgemeente

            results = filter_dropdown(df, 'District', deelgemeente, 'SubDistrict')
            return [{'label': i, 'value': i} for i in results]

    @dashapp.callback(
        Output(component_id='dropdown-buurt', component_property='options'),
        Input(component_id='dropdown-provincie', component_property='value'),
        Input(component_id='dropdown-gemeente', component_property='value'),
        Input(component_id='dropdown-deelgemeente', component_property='value'),
        Input(component_id='dropdown-plaats', component_property='value'),
    )
    def set_dropdown_buurt(provincie, gemeente, deelgemeente, plaats):
        # checks if there are values above this dropdown and set the correct results.
        if deelgemeente and plaats is None or []:
            filter_results = filter_dropdown(df, 'District', deelgemeente, 'SubSubDistrict')
            return [{'label': i, 'value': i} for i in filter_results]

        if str(plaats) == "['Alle']":
            # this is the list that contains all the values when 'Alle' is selected.
            alle_plaatsen = list(df.loc[df['District'] == deelgemeente[0], 'SubDistrict'].unique())
            filter_results = get_all_values(df, alle_plaatsen, 'SubDistrict', 'SubSubDistrict')
            return [{'label': i, 'value': i} for i in filter_results]
        else:
            alle_plaatsen = plaats
            filter_results = filter_dropdown(df, 'SubDistrict', plaats, 'SubSubDistrict')
            return [{'label': i, 'value': i} for i in filter_results]

    @dashapp.callback(
        Output(component_id='dropdown-subbuurt', component_property='options'),
        Input(component_id='dropdown-provincie', component_property='value'),
        Input(component_id='dropdown-gemeente', component_property='value'),
        Input(component_id='dropdown-deelgemeente', component_property='value'),
        Input(component_id='dropdown-plaats', component_property='value'),
        Input(component_id='dropdown-buurt', component_property='value'),
    )
    def set_dropdown_subbuurt(provincie, gemeente, deelgemeente, plaats, buurt):
        # checks if there are values above this dropdown and set the correct results.
        if plaats and buurt is None or []:
            filter_results = filter_dropdown(df, 'SubDistrict', plaats, 'SubSubSubDistrict')
            return [{'label': i, 'value': i} for i in filter_results]
        if deelgemeente and plaats is None or [] and buurt is None or []:
            filter_results = filter_dropdown(df, 'District', deelgemeente, 'SubSubSubDistrict')
            return [{'label': i, 'value': i} for i in filter_results]

        if str(buurt) == "['Alle']":
            # this is the list that contains all the values when 'Alle' is selected.
            alle_buurten = list(df.loc[df['SubDistrict'] == plaats[0], 'SubSubDistrict'].unique())
            filter_results = get_all_values(df, alle_buurten, 'SubSubDistrict', 'SubSubSubDistrict')
            return [{'label': i, 'value': i} for i in filter_results]
        else:
            alle_buurten = buurt
            filter_results = filter_dropdown(df, 'SubSubDistrict', buurt, 'SubSubSubDistrict')
            return [{'label': i, 'value': i} for i in filter_results]

    @dashapp.callback(
        Output(component_id='dropdown-adres', component_property='options'),
        Input(component_id='dropdown-provincie', component_property='value'),
        Input(component_id='dropdown-gemeente', component_property='value'),
        Input(component_id='dropdown-deelgemeente', component_property='value'),
        Input(component_id='dropdown-plaats', component_property='value'),
        Input(component_id='dropdown-buurt', component_property='value'),
        Input(component_id='dropdown-subbuurt', component_property='value'),
    )
    def set_dropdown_adres(provincie, gemeente, deelgemeente, plaats, buurt, subbuurt):
        # checks if there are values above this dropdown and set the correct results.
        if subbuurt:
            filter_results = filter_dropdown(df, 'SubSubSubDistrict', subbuurt, 'Address')
            return [{'label': i, 'value': i} for i in filter_results]
        if buurt and subbuurt is None or []:
            filter_results = filter_dropdown(df, 'SubSubDistrict', buurt, 'Address')
            return [{'label': i, 'value': i} for i in filter_results]
        if plaats and buurt is None or [] and subbuurt is None or []:
            filter_results = filter_dropdown(df, 'SubDistrict', plaats, 'Address')
            return [{'label': i, 'value': i} for i in filter_results]
        if deelgemeente and buurt is None or [] and subbuurt is None and []:
            filter_results = filter_dropdown(df, 'District', deelgemeente, 'Address')
            return [{'label': i, 'value': i} for i in filter_results]

        if str(subbuurt) == "['Alle']":
            # this is the list that contains all the values when 'Alle' is selected.
            alle_subbuurten = list(df.loc[df['SubSubDistrict'] == buurt[0], 'SubSubSubDistrict'].unique())
            filter_results = get_all_values(df, alle_subbuurten, 'SubSubSubDistrict', 'Address')

            return [{'label': i, 'value': i} for i in filter_results]
        else:
            alle_subbuurten = subbuurt
            filter_results = filter_dropdown(df, 'SubSubSubDistrict', subbuurt, 'Address')
            return [{'label': i, 'value': i} for i in filter_results]

    @dashapp.callback(
        Output(component_id='dropdown-laadstations', component_property='options'),
        Input(component_id='dropdown-provincie', component_property='value'),
        Input(component_id='dropdown-gemeente', component_property='value'),
        Input(component_id='dropdown-deelgemeente', component_property='value'),
        Input(component_id='dropdown-plaats', component_property='value'),
        Input(component_id='dropdown-buurt', component_property='value'),
        Input(component_id='dropdown-subbuurt', component_property='value'),
        Input(component_id='dropdown-adres', component_property='value'),
        Input(component_id='dropdown-laadstations', component_property='value'),
    )
    def set_dropdown_laadstations(provincie, gemeente, deelgemeente, plaats, buurt, subbuurt, adres, laadstation):
        # checks if there are values above this dropdown and set the correct results.
        if adres:
            filter_results = filter_dropdown(df, 'Address', adres, 'ChargePoint_ID')
            return [{'label': i, 'value': i} for i in filter_results]
        if subbuurt and adres is None or []:
            filter_results = filter_dropdown(df, 'SubSubSubDistrict', subbuurt, 'ChargePoint_ID')
            return [{'label': i, 'value': i} for i in filter_results]
        if buurt and adres is None or [] and subbuurt is None or []:
            filter_results = filter_dropdown(df, 'SubSubDistrict', buurt, 'ChargePoint_ID')
            return [{'label': i, 'value': i} for i in filter_results]
        if plaats and buurt is None or [] and subbuurt is None or [] and adres is None:
            filter_results = filter_dropdown(df, 'SubDistrict', plaats, 'ChargePoint_ID')
            return [{'label': i, 'value': i} for i in filter_results]
        if deelgemeente and subbuurt is None or [] and adres is None or []:
            filter_results = filter_dropdown(df, 'District', deelgemeente, 'ChargePoint_ID')
            return [{'label': i, 'value': i} for i in filter_results]

        if str(adres) == "['Alle']":
            # this is the list that contains all the values when 'Alle' is selected.
            alle_adressen = list(df.loc[df['SubSubSubDistrict'] == subbuurt[0], 'Address'].unique())
            filter_results = get_all_values(df, alle_adressen, 'Address', 'ChargePoint_ID')

            return [{'label': i, 'value': i} for i in filter_results]
        else:
            alle_adressen = adres
            filter_results = filter_dropdown(df, 'Address', adres, 'ChargePoint_ID')
            return [{'label': i, 'value': i} for i in filter_results]
    
    # Button event for clearing filter values
    @dashapp.callback(
        [
            Output('dropdown-laadstations', 'value'),
            Output('dropdown-adres', 'value'),
            Output('dropdown-subbuurt', 'value'),
            Output('dropdown-buurt', 'value'),
            Output('dropdown-plaats', 'value'),
            Output('dropdown-deelgemeente', 'value'),
            Output('dropdown-gemeente', 'value'),
            Output('dropdown-provincie', 'value')
        ],
        [Input('selectieWissen', 'n_clicks')]
    )
    def remove_filter_selection(n_clicks):
        # Prevents event from triggering upon loading the page
        changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
        if 'selectieWissen' in changed_id:
            return ["", "", "", "", "", "", "", ""] # Returns a list of empty strings to replace all filter values
        else:
            raise PreventUpdate
