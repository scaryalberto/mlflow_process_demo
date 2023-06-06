import dash
import json
from dash import html, dcc
from dash.dependencies import Input, Output,State
import plotly.graph_objs as go
import dash_table as dt
import pandas as pd 
import numpy as np
import pickle


app = dash.Dash()

df = pd.read_csv('attraversamenti_misti_dash.csv' , index_col=0) 
df = df[df['VALORE PRIORITA\''].isna()].copy() #mosta solo attraversamenti non classificati


to_predict = pd.DataFrame(columns=['UBICAZIONE ATTRAVERSAMENTO', 'Flusso', 'Incidenti', 'N. SEGNALAZIONI',
       '1) dopo una curva', '2) su rettilineo', '3) su strada in pendenza',
       '4) v ≤50 km/h', '5) v  > 50 km/h',
       '6) lontano da fonti di illuminazione ', '7) su viale alberato',
       '8) in prospicienza di elementi schermanti ', 'lat', 'lon',
       'VALORE PRIORITA\''])

tab_col = ['UBICAZIONE ATTRAVERSAMENTO', 'Flusso', 'Incidenti', 'N. SEGNALAZIONI',
       '1) dopo una curva', '3) su strada in pendenza',
       '4) v ≤50 km/h', 
       '6) lontano da fonti di illuminazione ', '7) su viale alberato',
       '8) in prospicienza di elementi schermanti ', 'lat', 'lon']

def SetColor(df):
    values = df['VALORE PRIORITA\''].tolist()
    color_list = []
    for i in values:
        if(i < 7.0 ):
            color_list.append("green")
        elif((i >=7.0 )&(i<13.0)):
            color_list.append("yellow")
        elif(i >= 13.0):
            color_list.append("red")
    return color_list

def SetNewColor(df):
    values = df['urgency index'].tolist()
    color_list = []
    for i in values:
        if(i < 7.0 ):
            color_list.append("green")
        elif((i >=7.0 )&(i<13.0)):
            color_list.append("yellow")
        elif(i >= 13.0):
            color_list.append("red")
    return color_list

def double_cols(df, existing):
    if df[existing] == 0:
        return 1
    else:
        return 0
    
loaded_model = pickle.load(open('reg_model.pkl', 'rb'))

mapbox_access_token = open(".mapbox_token").read()

app.layout = html.Div([
                       html.Div(#banner con logo
                                id="banner",
                                className="banner",
                                children=[
                                        html.Div(
                                                className="four columns",
                                                children=[
                                                        html.H6("Citizens and Business Services Optimization") ,
                                                        html.P(
                                                            children="Use Case: Reducing incidents against vulnerable individuals "
                                                              ),
                                                        ],
                                                ),
                        html.Img(src=app.get_asset_url("AI4PublicPolicy.png")), #logo
                                        ],
                                 ),
                        html.H4('Select the crossings to be evaluated'),
                        dcc.Graph( #mappa di Genova
                                 id='genoa-map',
                                 figure={
                                        'data': [
                                                go.Scattermapbox(
                                                                lon = df['lon'],
                                                                lat = df['lat'],
                                                                mode='markers',     
                                                                marker = {
                                                                         'size': 10,
                                                                         'color': SetColor(df)
                                                                        }
                                                                )
                                                ],
                                     'layout': go.Layout(margin=dict(l=2, r=2, t=5, b=2, pad=2),
                                                                    mapbox=dict(
                                                                    accesstoken=mapbox_access_token,
                                                                    bearing=0,
                                                                    style='light',
                                                                    center=dict(
                                                                                lat=44.41,
                                                                                lon=8.93
                                                                               ),
                                                                    pitch=0,
                                                                    zoom=11.5
                                                                                )
                                                                    )
                                        }
                                 ),
                        dcc.Store(id='selected'),
                        html.H4('After the crossing have been selected click on the button below to insert the required informations'),
                        html.Button("Update Features", id="update"),
                        html.Div(
                                dt.DataTable(
                                            id='insert',
                                            columns=[
                                                     {'name':i, 'id':i ,'presentation': 'dropdown'}for i in tab_col #to_predict.drop('VALORE PRIORITA\'', axis=1).columns
                                                    ],
                                            data=[],
                                            editable=True,
                                            dropdown={
                                                      'Flusso': {
                                                                 'options': [
                                                                             {'label' :i ,'value':i} for i in [1,2,3]
                                                                            ]
                                                                },
                                                      'Incidenti': {
                                                          'options': [
                                                              {'label' :i ,'value':i} for i in range(10)
                                                                     ]
                                                                    },
                                                      'N. SEGNALAZIONI': {
                                                                 'options': [
                                                                             {'label' :i ,'value':i} for i in range(10)
                                                                            ]
                                                                },
                                                      '1) dopo una curva': {
                                                                 'options': [
                                                                             {'label' :i ,'value':i} for i in [0,1]
                                                                            ]
                                                                },
                                                    #   '2) su rettilineo': {
                                                    #              'options': [
                                                    #                          {'label' :i ,'value':i} for i in [0,1]
                                                    #                         ]
                                                    #             },
                                                      '3) su strada in pendenza': {
                                                                 'options': [
                                                                             {'label' :i ,'value':i} for i in [0,1]
                                                                            ]
                                                                },
                                                      '4) v ≤50 km/h': {
                                                                 'options': [
                                                                             {'label' :i ,'value':i} for i in [0,1]
                                                                            ]
                                                                },
                                                    #   '5) v  > 50 km/h': {
                                                    #       'options': [
                                                    #           {'label' :i ,'value':i} for i in [0, 1]
                                                    #       ]
                                                    #   },
                                                '6) lontano da fonti di illuminazione ': {
                                                          'options': [
                                                              {'label' :i ,'value':i} for i in [0, 1]
                                                          ]
                                                      },
                                                '7) su viale alberato': {
                                                          'options': [
                                                              {'label' :i ,'value':i} for i in [0, 1]
                                                          ]
                                                      },
                                                '8) in prospicienza di elementi schermanti ': {
                                                          'options': [
                                                              {'label' :i ,'value':i} for i in [0, 1]
                                                          ]
                                                      }
                                                     }
                                             )
                                ), 
                        html.H6('It is possible to edit every cell: use the dropdown in every cell to choose the appropriate value'),                        
                        dcc.Store(id='features-stored'),
                        html.Button('Calculate Ranking', id='predict'),
                        html.H2('Urgency Index Ranking'),
                        html.Div(
                                dt.DataTable(#ospita tabella con i risultati del predict
                                            id='graduatoria',
                                            columns=[
                                                    {'name': 'UBICAZIONE ATTRAVERSAMENTO', 'id': 'UBICAZIONE ATTRAVERSAMENTO'},
                                                    {'name':'lon','id':'lon'},
                                                    {'name':'lat','id':'lat'},
                                                    {'name': 'urgency index', 'id': 'urgency index'}
                                                    ],
                                            data=[]
                                            )
                                ),
                        html.Button('Visualize on the Map', id='reset'),
                        html.Div(id='new-map')       
                        ])

@app.callback(
            Output('selected','data'),
            [Input('genoa-map', 'clickData'),
             Input('selected', 'data')]
             )
def click(clickData, data): #cattura il click sulla mappa e mette il punto nello store "intermediate-value"
    
    if not clickData:
        raise dash.exceptions.PreventUpdate
    to_add  = df[(df['lon'] == clickData['points'][0]['lon']) & (df['lat']==clickData['points'][0]['lat'])] #select clicked points from initial df
    if not data: #if no point has been selected yet
        
        punti = to_predict.append(to_add, ignore_index=True)
        punti.fillna(0, inplace=True)
    else: #if there are allready points in data
        
        punti = pd.read_json(data)
        punti = punti.append(to_add, ignore_index=True)
        punti.fillna(0, inplace=True)
        
    return punti.to_json()

@app.callback(
              Output('insert','data'),
              [Input('update','n_clicks')
               ,Input('selected','data')]
             )
def insert_features(n_clicks, point):
    if n_clicks:
        data  = pd.read_json(point)
        data.drop('VALORE PRIORITA\'', axis=1, inplace=True)
        return data.to_dict(orient='records')
    
@app.callback(
              Output('graduatoria', 'data'),
              [Input('predict','n_clicks'),
            #    Input('selected','data_timestamp'),
            #    State('selected','data')]
              Input('insert','data')])
def calculate_prediction(n_clicks, data):
    if n_clicks:
        df_pred = pd.DataFrame(data)
        df_pred['2) su rettilineo'] = df_pred.apply(lambda row: double_cols(row,'1) dopo una curva'),axis=1)
        df_pred['5) v  > 50 km/h'] = df_pred.apply(lambda row: double_cols(row, '4) v ≤50 km/h'), axis=1)
        df_pred['urgency index'] = np.round(loaded_model.predict(df_pred[['N. SEGNALAZIONI','Incidenti','1) dopo una curva', '2) su rettilineo', 
            '3) su strada in pendenza',
        '4) v ≤50 km/h', '5) v  > 50 km/h',
        '7) su viale alberato','6) lontano da fonti di illuminazione ', 
        'Flusso' ,'8) in prospicienza di elementi schermanti ']]),2)#use the model to predict values for the selected points
        
        risultato = df_pred.sort_values(by="urgency index",ascending=False) #sort the results
        
        return risultato[['UBICAZIONE ATTRAVERSAMENTO','lon','lat','urgency index']].reset_index().to_dict( orient='records')#return the chart into a datatable
       
@app.callback(
              Output('new-map','children'),
              [Input('reset','n_clicks')
              ,Input('graduatoria','data')]
             )
def update_graph(n_clicks,data):
    if n_clicks:
        df_map = pd.DataFrame(data)
        return dcc.Graph( #mappa di Genova
                                 id='genoa-map-2',
                                 figure={
                                        'data': [
                                                go.Scattermapbox(
                                                                lon = df_map['lon'],
                                                                lat = df_map['lat'],
                                                                mode='markers',     
                                                                marker = {
                                                                         'size': 10,
                                                                         'color': SetNewColor(df_map)
                                                                        }
                                                                )
                                                ],
                                     'layout': go.Layout(margin=dict(l=2, r=2, t=5, b=2, pad=2),
                                                                    mapbox=dict(
                                                                    accesstoken=mapbox_access_token,
                                                                    bearing=0,
                                                                    style='light',
                                                                    center=dict(
                                                                                lat=44.41,
                                                                                lon=8.93
                                                                               ),
                                                                    pitch=0,
                                                                    zoom=11.5,
                                                                                )
                                                                    )
                                        })
        
    
    
if __name__ == '__main__':
    app.run_server()