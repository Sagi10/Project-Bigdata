import pandas as pd
from dash.exceptions import PreventUpdate
import dash_table
import plotly.graph_objs as go
import sys


# Function for calling stored procedures 
def call_stored_procedure(db, function_name, params):
    connection = db.engine.raw_connection()
    paramString = ''
    for param in params:
        paramString = paramString + str(param) + ','
    paramString = paramString[:-1]
    try:
        sql_query = "SET NOCOUNT ON; EXEC {} {}".format(function_name, paramString)
        df = pd.read_sql_query(sql_query, connection)
        # print(df)
        return df
    finally:
        connection.close()


# Logic for Creating A DASH navigatable Table
def create_data_table(df):
    tableDf = df[df['YearMonth'] != 'Alle']  # Use only rows where YearMonth is not equal to Alle for table
    table = dash_table.DataTable(  # Create Dash Datatable
        id="database-table",
        columns=[{'name': i, 'id': i} for i in tableDf.columns],  # Set header columns of table
        filter_action="native",  # allow filtering of data by user ('native') or not ('none')
        data=tableDf.to_dict("records"),  # Set Data of the DataTable
        sort_action="native",
        sort_mode="native",
        page_size=10,  # The Default number of rows in one table page
        style_cell_conditional=[  # Style Table to be striped
            {
                'if': {'column_id': c},
                'textAlign': 'left'
            } for c in ['Date', 'Region']
        ],
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(248, 248, 248)'
            }
        ],
        # style_header={
        #     'backgroundColor': 'rgb(230, 230, 230)',
        #     'fontWeight': 'bold'
        # }
    )
    return table  # Returned the created table


sequence = ['Year', 'YearMonth', 'Region', 'District', 'SubDistrict', 'SubSubDistrict', 'SubSubSubDistrict', 'Address',
            'ChargePoint']


# TODO fix the 'Alle' selection bug.
# Filter the dataframe for location and add trace/bar chart for each location level
def filter_location_and_add_bartrace(deelgemeente, plaats, buurt, subbuurt, adres, laadstations, data, focusColumn,
                                     fig):
    finalDataframe = pd.DataFrame()
    isFiltered = False
    checkNext = True

    if laadstations is not None:
        if len(laadstations) >= 1:
            isFiltered = True
            checkNext = False
            for value in laadstations:
                # NumberOfStickySessions
                locationFiltered = data[data['ChargePoint'].isin([value])]

                if focusColumn == 'MonthlyOccupancyPercentage' or focusColumn == 'AverageKwhChargeStation':
                    crimpedData = locationFiltered.groupby(sequence, as_index=False)[focusColumn].mean()
                else:
                    crimpedData = locationFiltered.groupby(sequence, as_index=False)[focusColumn].sum()

                if focusColumn == 'NumberOfStickySessions':
                    numberOfSession = locationFiltered.groupby(sequence, as_index=False)["NumberOfSessions"].sum()
                    crimpedData[focusColumn] = (crimpedData[focusColumn] / numberOfSession["NumberOfSessions"]) * 100

                fig.add_trace(go.Bar(name=value, x=crimpedData["YearMonth"], y=crimpedData[focusColumn]))
                finalDataframe = finalDataframe.append(crimpedData, ignore_index=True)
        else:
            checkNext = True  # if array is empty check next
    if adres is not None and checkNext:
        if len(adres) >= 1:
            isFiltered = True
            checkNext = False
            for value in adres:
                locationFiltered = data[data['Address'].isin([value])]

                if focusColumn == 'MonthlyOccupancyPercentage' or focusColumn == 'AverageKwhChargeStation':
                    crimpedData = locationFiltered.groupby(sequence[:-1], as_index=False)[focusColumn].mean()
                else:
                    crimpedData = locationFiltered.groupby(sequence[:-1], as_index=False)[focusColumn].sum()

                if focusColumn == 'NumberOfStickySessions':
                    numberOfSession = locationFiltered.groupby(sequence[:-1], as_index=False)["NumberOfSessions"].sum()
                    crimpedData[focusColumn] = (crimpedData[focusColumn] / numberOfSession["NumberOfSessions"]) * 100

                fig.add_trace(go.Bar(name=value, x=crimpedData["YearMonth"], y=crimpedData[focusColumn]))
                finalDataframe = finalDataframe.append(crimpedData, ignore_index=True)
        else:
            checkNext = True
    if subbuurt is not None and checkNext:
        if len(subbuurt) >= 1:
            isFiltered = True
            checkNext = False
            for value in subbuurt:
                locationFiltered = data[data['SubSubSubDistrict'].isin([value])]

                if focusColumn == 'MonthlyOccupancyPercentage' or focusColumn == 'AverageKwhChargeStation':
                    crimpedData = locationFiltered.groupby(sequence[:-2], as_index=False)[focusColumn].mean()
                else:
                    crimpedData = locationFiltered.groupby(sequence[:-2], as_index=False)[focusColumn].sum()

                if focusColumn == 'NumberOfStickySessions':
                    numberOfSession = locationFiltered.groupby(sequence[:-2], as_index=False)["NumberOfSessions"].sum()
                    crimpedData[focusColumn] = (crimpedData[focusColumn] / numberOfSession["NumberOfSessions"]) * 100

                fig.add_trace(go.Bar(name=value, x=crimpedData["YearMonth"], y=crimpedData[focusColumn]))
                finalDataframe = finalDataframe.append(crimpedData, ignore_index=True)
        else:
            checkNext = True
    if buurt is not None and checkNext:
        if len(buurt) >= 1:
            isFiltered = True
            checkNext = False
            for value in buurt:
                locationFiltered = data[data['SubSubDistrict'].isin([value])]

                if focusColumn == 'MonthlyOccupancyPercentage' or focusColumn == 'AverageKwhChargeStation':
                    crimpedData = locationFiltered.groupby(sequence[:-3], as_index=False)[focusColumn].mean()
                else:
                    crimpedData = locationFiltered.groupby(sequence[:-3], as_index=False)[focusColumn].sum()

                if focusColumn == 'NumberOfStickySessions':
                    numberOfSession = locationFiltered.groupby(sequence[:-3], as_index=False)["NumberOfSessions"].sum()
                    crimpedData[focusColumn] = (crimpedData[focusColumn] / numberOfSession["NumberOfSessions"]) * 100

                fig.add_trace(go.Bar(name=value, x=crimpedData["YearMonth"], y=crimpedData[focusColumn]))
                finalDataframe = finalDataframe.append(crimpedData, ignore_index=True)
        else:
            checkNext = True
    if plaats is not None and checkNext:
        if len(plaats) >= 1:
            isFiltered = True
            checkNext = False
            for value in plaats:
                locationFiltered = data[data['SubDistrict'].isin([value])]

                if focusColumn == 'MonthlyOccupancyPercentage' or focusColumn == 'AverageKwhChargeStation':
                    crimpedData = locationFiltered.groupby(sequence[:-4], as_index=False)[focusColumn].mean()
                else:
                    crimpedData = locationFiltered.groupby(sequence[:-4], as_index=False)[focusColumn].sum()

                if focusColumn == 'NumberOfStickySessions':
                    numberOfSession = locationFiltered.groupby(sequence[:-4], as_index=False)["NumberOfSessions"].sum()
                    crimpedData[focusColumn] = (crimpedData[focusColumn] / numberOfSession["NumberOfSessions"]) * 100

                fig.add_trace(go.Bar(name=value, x=crimpedData["YearMonth"], y=crimpedData[focusColumn]))
                finalDataframe = finalDataframe.append(crimpedData, ignore_index=True)
        else:
            checkNext = True
    if (deelgemeente is not None and checkNext):
        if (len(deelgemeente) >= 1):
            isFiltered = True
            checkNext = False
            for value in deelgemeente:
                locationFiltered = data[data['District'].isin([value])]
                if (focusColumn == 'MonthlyOccupancyPercentage' or focusColumn == 'AverageKwhChargeStation'):
                    crimpedData = locationFiltered.groupby(sequence[:-5], as_index=False)[focusColumn].mean()
                else:
                    crimpedData = locationFiltered.groupby(sequence[:-5], as_index=False)[focusColumn].sum()

                if focusColumn == 'NumberOfStickySessions':
                    numberOfSession = locationFiltered.groupby(sequence[:-5], as_index=False)["NumberOfSessions"].sum()
                    crimpedData[focusColumn] = (crimpedData[focusColumn] / numberOfSession["NumberOfSessions"]) * 100

                fig.add_trace(go.Bar(name=value, x=crimpedData["YearMonth"], y=crimpedData[focusColumn]))
                finalDataframe = finalDataframe.append(crimpedData, ignore_index=True)
        else:
            checkNext = True
    if (isFiltered == False and checkNext == True):  # Default
        # print('DEFAULT')
        defaultSequence = ['Year', 'YearMonth', 'Region']
        locationFiltered = data[data['Region'] == 'Amsterdam']  # Get only the rows with region Amsterdam
        if (focusColumn == 'MonthlyOccupancyPercentage' or focusColumn == 'AverageKwhChargeStation'):
            crimpedData = locationFiltered.groupby(['Year', 'YearMonth', 'Region'], as_index=False)[focusColumn].mean()
        else:
            crimpedData = locationFiltered.groupby(['Year', 'YearMonth', 'Region'], as_index=False)[
                focusColumn].sum()  # Group by the rows that are needed for the graph and table

        # Extra Calculation for sticky session percentage calculation
        if focusColumn == 'NumberOfStickySessions':
            numberOfSession = locationFiltered.groupby(defaultSequence, as_index=False)[
                "NumberOfSessions"].sum()  # Get total sessions
            crimpedData[focusColumn] = (crimpedData[focusColumn] / numberOfSession[
                "NumberOfSessions"]) * 100  # Get percentage sticky sessions out total sessions

        fig.add_trace(go.Bar(name="Amsterdam", x=crimpedData["YearMonth"],
                             y=crimpedData[focusColumn]))  # Add Bar Chart with the filtered dataframe
        finalDataframe = crimpedData  # Add the filtered dataframe to the finalDataframe that will be displayed in the table

    finalDataframe[focusColumn] = finalDataframe[focusColumn].round(2)
    finalDataframe = finalDataframe.sort_values(['YearMonth'],
                                                ascending=[False])  # Sort the values descending before returning
    return finalDataframe  # Return the finalDataframe


def perform_query(query, db):
    dbResult = db.engine.execute(query)
    result = list(pd.DataFrame(dbResult).iloc[:, 0])
    return result


# Dit wordt gebruikt om de verschillende filter mogelijkheid te vullen aan de hand van wat er is geselecteerd.
def filter_dropdown(df, filterColumn, conditionName, wantedResult):
    if conditionName is None:
        raise PreventUpdate
    if len(conditionName) == 0:
        raise PreventUpdate
    elif len(conditionName) == 1:
        filter = df[filterColumn] == conditionName[0]
        results = list(df.loc[filter, wantedResult].unique())
        results.sort()
        results.insert(0, 'Alle')
        return results
    else:
        result = list()
        for name in conditionName:
            filterdis = (df[filterColumn] == name)
            results = df.loc[filterdis, wantedResult].unique()
            for item in results:
                if item not in result:
                    result.append(item)
            result.sort()
            alle_optie = 'Alle'
            if alle_optie not in result:
                result.insert(0, alle_optie)
        return result


# Hiermee worden alle waardes opgeslagen in een lijst wanneer 'Alle' in de filter is geselecteerd.
def get_all_values(dataframe, items, colum_name_filter, wanted_result):
    filter_results = []
    for item in items:
        filter = dataframe[colum_name_filter] == item
        filter_results.extend(list(dataframe.loc[filter, wanted_result].unique()))
    filter_results.insert(0, 'Alle')
    return filter_results
