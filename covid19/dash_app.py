# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import os
import pathlib
import numpy as np
import datetime as dt
import dash
import dash_core_components as dcc
import dash_html_components as html

from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
    'background': '#393f4d',
    'text': '#d4d4dc',
    'plot_background' : '#1d1e22'
}


#read the state database and clean things up
state_df=pd.read_csv('https://opendata.arcgis.com/datasets/b913e9591eae4912b33dc5b4e88646c5_10.csv?outSR=%7B%22latestWkid%22%3A3857%2C%22wkid%22%3A102100%7D')
state_df['DATE'] = pd.to_datetime(state_df["DATE"])
state_df.set_index("DATE", inplace=True)
state_df.sort_index(ascending = True, inplace=True)
state_df['POS_NEW'] = state_df['POS_NEW'].fillna(0)
state_df['POS_NEW'] = state_df['POS_NEW'].astype(int)

#pull out the data for Marathon County
regional_df=state_df.copy()[state_df["NAME"]=='Marathon']
regional_df = regional_df[["POS_NEW", "POSITIVE"]]
regional_df.columns = ['marathon_new', 'marathon_total']

#grab values for text box on graph
latest_m = regional_df['marathon_new'].iloc[-1]
today_m = regional_df.index[-1]
today_m = today_m.strftime('%b %e')
latest_text_m = today_m +' New Cases' + ': ' + str(latest_m)
week_df=regional_df['marathon_new'].last('7d')
latest_week_m = week_df.sum()
latest_week_text_m = 'Last 7 Days............. ' + str(latest_week_m)
today_total = regional_df['marathon_total'].iloc[-1]
total_text = 'As of ' + today_m + 'Total Cases = ' + str(today_total)


#Draw the graph for Marathon County New Cases

fig = px.bar(x=regional_df.index, 
            y=regional_df.marathon_new, 
            width=800, height=400,
            labels = {"x":'Date',"y":"New Cases" },
            color_discrete_sequence=["#0779e4"],
            template = "plotly_dark",
            
            )


fig.add_trace(
    go.Scatter(
        x=regional_df.index,
        y=regional_df["marathon_new"].rolling(7).mean(),
        mode="lines",
        line=go.scatter.Line(color="#FF5A09", width=4),
        name = "7 Day Average",
        hoverinfo = 'none',
        
        
     )
)

#Styling details
fig.update_layout(xaxis_tickmode = 'linear',
                  xaxis_dtick = 604800000.0,
                  xaxis_tickformat = '%m/%d',
                  xaxis_tick0 = '2020-03-15',
                  xaxis_tickangle = -25,
                  xaxis_ticks = 'outside',
                  xaxis_tickcolor = '#d4d4dc',
                  xaxis_tickfont = dict(size=10),
                  xaxis_title = "",
                  plot_bgcolor=colors['plot_background'],
                  paper_bgcolor=colors['plot_background'],
                  legend=dict(
                    yanchor="top",
                    y=0.75,
                    xanchor="left",
                    x=0.1),
                  annotations=[
                    go.layout.Annotation(
                    text=latest_text_m + '<br>' + latest_week_text_m, 
                    align='left',
                    showarrow=False,
                    xref='paper',
                    yref='paper',
                    x=0.1,
                    y=1,
                    bordercolor='cornsilk',
                    borderwidth=1,
                    bgcolor = 'white',
                    font = dict(color = 'black')
                    )]
                )
fig.update_xaxes(showline=True, linewidth=2, linecolor='cornsilk')
                 

#Draw the figure for Marathon County Total Cases

fig2 = px.bar(x=regional_df.index, y=regional_df.marathon_total,
            width=800, height=400,
            labels = {"x":'Date',"y":"Total Cases" },
            color_discrete_sequence=["#feda6a"],
            template = 'plotly_dark'
             )
fig2.update_layout(xaxis_tickmode = 'linear',
                  xaxis_dtick = 604800000.0,
                  xaxis_tickformat = '%m/%d',
                  xaxis_tick0 = '2020-03-15',
                  xaxis_tickangle = -25,
                  xaxis_ticks = 'outside',
                  xaxis_tickcolor ='#d4d4dc',
                  xaxis_tickfont = dict(size=10),
                  xaxis_title = "",
                  plot_bgcolor=colors['plot_background'],
                  paper_bgcolor=colors['plot_background'],
                  legend=dict(
                    yanchor="top",
                    y=0.75,
                    xanchor="left",
                    x=0.1),
                   annotations=[
                    go.layout.Annotation(
                    text=total_text, 
                    align='left',
                    showarrow=False,
                    xref='paper',
                    yref='paper',
                    x=0.1,
                    y=1,
                    bordercolor='cornsilk',
                    borderwidth=1,
                    bgcolor = 'white',
                    font = dict(color = 'black')
                    )]
                  
                )
fig2.update_xaxes(showline=True, linewidth=2, linecolor='cornsilk')

#Get County data from database

portage_df=state_df.copy()[state_df["NAME"]=='Portage']
portage_df = portage_df[["POS_NEW", "POSITIVE"]]
regional_df = regional_df.assign(portage_new = portage_df['POS_NEW'])
regional_df = regional_df.assign(portage_total = portage_df['POSITIVE'])


wood_df=state_df.copy()[state_df["NAME"]=='Wood']
wood_df = wood_df[["POS_NEW", "POSITIVE"]]
regional_df = regional_df.assign(wood_new = wood_df['POS_NEW'])
regional_df = regional_df.assign(wood_total = wood_df['POSITIVE'])

waupaca_df=state_df.copy()[state_df["NAME"]=='Waupaca']
waupaca_df = waupaca_df[["POS_NEW", "POSITIVE"]]
regional_df = regional_df.assign(waupaca_new = waupaca_df['POS_NEW'])
regional_df = regional_df.assign(waupaca_total = waupaca_df['POSITIVE'])

lincoln_df=state_df.copy()[state_df["NAME"]=='Lincoln']
lincoln_df = lincoln_df[["POS_NEW", "POSITIVE"]]
regional_df = regional_df.assign(lincoln_new = lincoln_df['POS_NEW'])
regional_df = regional_df.assign(lincoln_total = lincoln_df['POSITIVE'])


total_col_list = ['marathon_total', 'portage_total', 'wood_total', 'waupaca_total', 'lincoln_total']
regional_df['total_cases'] = regional_df[total_col_list].sum(axis=1)
new_col_list = ['marathon_new', 'portage_new', 'wood_new', 'waupaca_new', 'lincoln_total']
regional_df['new_cases'] = regional_df[new_col_list].sum(axis=1)

#Get dates and totals for graph annotation

latest = regional_df['new_cases'].iloc[-1]
today = regional_df.index[-1]
today = today.strftime('%b %e')
latest_text = today +' New Cases' + ': ' + str(latest)
week_df=regional_df['new_cases'].last('7d')
latest_week = week_df.sum()
latest_week_text = 'Last 7 Days............. ' + str(latest_week)
today_total_r = regional_df['total_cases'].iloc[-1]
total_text_r = 'As of ' + today + 'Total Cases = ' + str(today_total_r)

#Draw the figure for New Central Wisconsin Cases


fig3 = px.bar(x=regional_df.index, 
            y=regional_df.new_cases, 
            width=800, height=400,
            labels = {"x":'Date',"y":"New Cases" },
            color_discrete_sequence=["#ec7f37"],
            template = "plotly_dark",
            
            )


fig3.add_trace(
    go.Scatter(
        x=regional_df.index,
        y=regional_df['new_cases'].rolling(7).mean(),
        mode="lines",
        line=go.scatter.Line(color="#0779e4", width=4),
        name = "7 Day Average",
        hoverinfo = 'none',
        
        
     )
)

#Styling details

fig3.update_layout(xaxis_tickmode = 'linear',
                  xaxis_dtick = 604800000.0,
                  xaxis_tickformat = '%m/%d',
                  xaxis_tick0 = '2020-03-15',
                  xaxis_tickangle = -25,
                  xaxis_ticks = 'outside',
                  xaxis_tickcolor = '#d4d4dc',
                  xaxis_tickfont = dict(size=10),
                  xaxis_title = "",
                  plot_bgcolor=colors['plot_background'],
                  paper_bgcolor=colors['plot_background'],
                  legend=dict(
                    yanchor="top",
                    y=0.75,
                    xanchor="left",
                    x=0.1),
                  annotations=[
                    go.layout.Annotation(
                    text=latest_text + '<br>' + latest_week_text, 
                    align='left',
                    showarrow=False,
                    xref='paper',
                    yref='paper',
                    x=0.1,
                    y=1,
                    bordercolor='cornsilk',
                    borderwidth=1,
                    bgcolor = 'white',
                    font = dict(color = 'black')
                    )]
                )
fig3.update_xaxes(showline=True, linewidth=2, linecolor='cornsilk')

#Draw figure for Central Wisconsin Cumulative

fig4 = px.bar(x=regional_df.index, y=regional_df.total_cases,
            width=800, height=400,
            labels = {"x":'Date',"y":"Total Cases" },
            color_discrete_sequence=["#be4f0c"],
            template = 'plotly_dark'
             )
fig4.update_layout(xaxis_tickmode = 'linear',
                  xaxis_dtick = 604800000.0,
                  xaxis_tickformat = '%m/%d',
                  xaxis_tick0 = '2020-03-15',
                  xaxis_tickangle = -25,
                  xaxis_ticks = 'outside',
                  xaxis_tickcolor ='#d4d4dc',
                  xaxis_tickfont = dict(size=10),
                  xaxis_title = "",
                  plot_bgcolor=colors['plot_background'],
                  paper_bgcolor=colors['plot_background'],
                  legend=dict(
                    yanchor="top",
                    y=0.75,
                    xanchor="left",
                    x=0.1),
                   annotations=[
                    go.layout.Annotation(
                    text=total_text_r, 
                    align='left',
                    showarrow=False,
                    xref='paper',
                    yref='paper',
                    x=0.1,
                    y=1,
                    bordercolor='cornsilk',
                    borderwidth=1,
                    bgcolor = 'white',
                    font = dict(color = 'black')
                    )]
                  
                )
fig4.update_xaxes(showline=True, linewidth=2, linecolor='cornsilk')



#Generate HTML to display graphs

app.layout = html.Div(style={'backgroundColor': colors['background']},
    children=[#body

#HTML for New Marathon County Cases
        
    html.Div(style={'backgroundColor': colors['background']}, children=[
        html.H4(
        children='Marathon County: New Confirmed COVID Cases by Date and 7-Day Average',
        style={
            'textAlign': 'center',
            'color': colors['text'],
            'paddingTop' : 50,
        }
    ),

    html.Div(style={
        'width': '100%',
        'display': 'flex',
        'align-items': 'center',
        'justify-content': 'center'
    }, children=[
    

    dcc.Graph(
        id='Marathon_New',
        figure=fig
    )]
             ),
    html.Div(style = {
                    'textAlign' : 'center',
                    'color': colors['text'],
                    'paddingTop' : 20,
                    },
        children=[
            html.P('Data from the Wisconsin Department of Health Services.  Data is updated once daily.')
            ]),
        
]),

#HTML for Marathon County Cumulative Cases
    
html.Div(style={'backgroundColor': colors['background']}, children=[
        html.H4(
        children='Marathon County: Cumulative Total COVID-19 Cases by Date Confirmed',
        style={
            'textAlign': 'center',
            'color': colors['text'],
            'paddingTop' : 50,
        }
    ),
    html.Div(style={
        'width': '100%',
        'display': 'flex',
        'align-items': 'center',
        'justify-content': 'center'
    }, children=[
    

    dcc.Graph(
        id='Marathon_Total',
        figure=fig2
    )]
             ),
        
    ]),
    
    html.Div(style = {
                    'textAlign' : 'center',
                    'color': colors['text'],
                    'paddingTop' : 20,
                    },
        children=[
            html.P('Data from the Wisconsin Department of Health Services.  Data is updated once daily.')
            ]),


#HTML for graph of Central Wisconsin New Cases

html.Div(style={'backgroundColor': colors['background']}, children=[
        html.H4(
        children='Central Wisconsin: New Confirmed COVID Cases by Date and 7-Day Average',
        style={
            'textAlign': 'center',
            'color': colors['text'],
            'paddingTop' : 50,
        }
    ),
    html.Div(style = {
                    'textAlign' : 'center',
                    'color': colors['text'],
                     },
        children=[
            html.P('Central Wisconsin data is combined from Marathon, Lincoln, Wood, Waupaca and Portage Counties')
            ]),
    
    html.Div(style={
        'width': '100%',
        'display': 'flex',
        'align-items': 'center',
        'justify-content': 'center'
    }, children=[
    

    dcc.Graph(
        id='CW-New',
        figure=fig3
    )]
             ),
    html.Div(style = {
                    'textAlign' : 'center',
                    'color': colors['text'],
                    'paddingTop' : 20,
                    },
        children=[
            html.P('Data from the Wisconsin Department of Health Services.  Data is updated once daily.')
            ]),
        
    ]),
#HTML for Central Wisconsin Cumulative Cases
    
    html.Div(style={'backgroundColor': colors['background']}, children=[
        html.H4(
        children='Central Wisconsin: Cumulative Total COVID-19 Cases by Date Confirmed',
        style={
            'textAlign': 'center',
            'color': colors['text'],
            'paddingTop' : 50,
        }
    ),
    html.Div(style = {
                    'textAlign' : 'center',
                    'color': colors['text'],
                     },
        children=[
            html.P('Central Wisconsin data is combined from Marathon, Lincoln, Wood, Waupaca and Portage Counties')
            ]),

    html.Div(style={
        'width': '100%',
        'display': 'flex',
        'align-items': 'center',
        'justify-content': 'center'
    }, children=[
    

    dcc.Graph(
        id='CW_total',
        figure=fig4
    )]
             ),
        
    ]),
    
    html.Div(style = {
                    'textAlign' : 'center',
                    'color': colors['text'],
                    'paddingTop' : 20,
                    },
        children=[
            html.P('Data from the Wisconsin Department of Health Services.  Data is updated once daily.')
            ]),
])
 




if __name__ == '__main__':
    app.run_server(debug=True)