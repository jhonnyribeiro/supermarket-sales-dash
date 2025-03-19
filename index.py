import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

import pandas as pd
import numpy as np

import plotly.express as px
import plotly.graph_objects as go

# app = dash.Dash(__name__)
app = dash.Dash(
    external_stylesheets=[dbc.themes.MINTY]
)
server = app.server

df_data = pd.read_csv("supermarket_sales.csv", sep=",")
df_data["Date"] = pd.to_datetime(df_data["Date"])

#Layout
app.layout = html.Div(children=[
        dbc.Row([
                dbc.Col([
                    dbc.Card([
                        html.H2("Conecta Tecnologia", style={"font-family": "Voltaire", "font-size": "23px"}),
                        html.Hr(),
                        
                        html.H5("Cidades:"),
                        dcc.Checklist(df_data["City"].value_counts().index,
                                    df_data["City"].value_counts().index, id="check_city", inputStyle={"margin-right": "5px", "margin-left": "5px" }),

                        html.H5("Variável de análise:", style={"margin-top":"30px"}),
                        dcc.RadioItems(["gross income","Rating"], "gross income", id="main_variable",
                        inputStyle={"margin-right": "5px", "margin-left": "5px" }),
                        ], style={"height": "90vh", "margin": "20px", "padding": "20px"})
            ], sm=2),

            dbc.Col([
                dbc.Row([
                    dbc.Col([dcc.Graph(id="city_fig")], sm=4),
                    dbc.Col([dcc.Graph(id="gender_fig")], sm=4),
                    dbc.Col([dcc.Graph(id="pay_fig")], sm=4),
                ]),
                dbc.Row([dcc.Graph(id="income_per_date_fig")]),
                dbc.Row([dcc.Graph(id="income_per_product_fig")]),


      
             
            ], sm=10),
        ])




    
    ]
)

#Callbacks
@app.callback([
    Output('city_fig', 'figure'),
    Output('pay_fig', 'figure'),
    Output('income_per_product_fig', 'figure'),
    ],
    [
        Input('check_city', 'value'),
        Input('main_variable', 'value'),
    ]
)
def render_graphs(cities, main_variable):
    # cities = ['Yangon']
    # main_variable = "gross income"
    operation = np.sum if main_variable == "gross income" else np.mean
    df_filtered = df_data[df_data["City"].isin(cities)]

    df_city = df_filtered.groupby("City")[main_variable].apply(operation).to_frame().reset_index()
    df_payment = df_filtered.groupby("Payment")[main_variable].apply(operation).to_frame().reset_index()
    df_product_income = df_filtered.groupby(["Product line","City"])[main_variable].apply(operation).to_frame().reset_index()
   
    fig_city = px.bar(df_city, x="City", y=main_variable)
    fig_payment= px.bar(df_payment, y="Payment", x=main_variable, orientation='h')
    fig_product_income  = px.bar(df_product_income, x=main_variable, y='Product line', color='City',  orientation='h', barmode='group')

    fig_city.update_layout(margin=dict(l=0,r=0,t=20,b=20), height=200)
    fig_payment.update_layout(margin=dict(l=0,r=0,t=20,b=20), height=200)
    fig_product_income.update_layout(margin=dict(l=0,r=0,t=20,b=20), height=500)

    return fig_city, fig_payment, fig_product_income
    
#Run server
if __name__ == "__main__":
    app.run_server(host='0.0.0.0',port=8051, debug=True)