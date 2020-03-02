import dash
from dash.exceptions import PreventUpdate
import dash_table.FormatTemplate as FormatTemplate
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html

import sqlite3 
import pandas as pd
import numpy as np
import sqlalchemy 
from datetime import datetime as dt

# Read SQL  
def read_sql():
	conn = sqlite3.connect('test.db')
	c = conn.cursor()
	query = """ SELECT * FROM invoice """
	df = pd.read_sql(query, conn)
	return df
df = read_sql()

selector = dbc.Row([
	dbc.Col([
		dbc.Label('Aggregate By'),
		dbc.RadioItems(
			id='tab_1_view',
			inline = True,
			value = 'daily',
			style = { 'font-size': 15, 'margin-top': 12},
			options= [
				{'label' : 'Max' , 'value' : 'daily'}, 
				{'label' : 'Week', 'value' : 'weekly'},
				{'label' : 'Month', 'value' : 'monthly'},
				{'label' : 'Year', 'value': 'yearly'},
			])
		], width = 4
		),

	dbc.Col([
		dbc.Label('Shop'),
		dcc.Dropdown(
			id="tab_1_shop",
			options=[{'label': i, 'value': i} for i in df['Shop'].unique()],
			multi = True,
			style = {'height': '45px', 'width': '300px', 'font-size': 18, 'margin-top':2},
			value= df['Shop'].unique()
			),
		], width = 4
		),

	dbc.Col([
		dbc.Label('Time Period'),
		dcc.DatePickerRange(
			id ='tab_1_time',
			month_format = 'MMMM Y', 
			start_date_placeholder_text = 'Start Date',
			end_date_placeholder_text = 'End Date',
			clearable= True,
			),
		], width =4,
		),
	], form = True, style= {'margin-left':30}
	)

card= dbc.Row([
	dbc.CardDeck([
		dbc.Card(
			dbc.CardBody([
				html.H6("Total Revenue", className="card-title"),
				html.H3( id="card1", style ={'textAlign': 'center', 'margin-top': 18}),
				]),
			color="dark", 
			outline=True,
			style = {'width': '12rem', 'height': '8rem'}
			),

		dbc.Card(
			dbc.CardBody([
				html.H6("Avg/ Invoice", className="card-title"),
				html.H3( id="card2",  style ={'textAlign': 'center', 'margin-top': 18}),
				]),
			color="dark", 
			outline=True,
			style = {'width': '12rem', 'height': '8rem'}
			),

		dbc.Card(
			dbc.CardBody([
				html.H6("Invoice", className="card-title"),
				html.H3(id="card3",  style ={'textAlign': 'center', 'margin-top': 18}),
				]),
			color="dark", 
			outline=True,
			style = {'width': '12rem', 'height': '8rem'}
			),


		dbc.Card(
			dbc.CardBody([
				html.H6("Clients", className="card-title"),
				html.H3(id = 'card4',  style ={'textAlign': 'center', 'margin-top': 18}),
				]),
			color="dark", 
			outline=True,
			style = {'width': '12rem', 'height': '8rem'}
			),
		]),
	], 
	justify = 'around'
	)
		
graph_overview = dbc.Row([
		dbc.Col(dcc.Graph('daily-revenue'), width = 8),
		dbc.Col(dcc.Graph('piechart'), width = 4)
	])

graph_row2 = dbc.Row([
	dbc.Col(dcc.Graph('revenue-by-shop'), width = 7),
	dbc.Col(dcc.Graph('scatterplot'), width = 5)
	])

# DashBoard Layout
body = dbc.Container([
	selector,
	html.Br(),
	card,
	html.Br(),
	graph_overview,
	html.Br(),
	graph_row2
	],
	className='mt-4'
)

tab_1_layout = html.Div([body])