import dash
import dash_table
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import dash_table.FormatTemplate as FormatTemplate
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from plotly.subplots import make_subplots

import sqlite3 
import pandas as pd
from datetime import datetime as dt
from datetime import date
import numpy as np
import sqlalchemy 

# query table and get dataframe
def read_table():
    conn = sqlite3.connect('test.db')
    c = conn.cursor()

    query = """ SELECT * FROM invoice """
    df = pd.read_sql(query, conn)
    df['Transaction_Date'] = pd.to_datetime(df['Transaction_Date'], dayfirst=True).dt.date
    df['Transfer_Date'] = pd.to_datetime(df['Transfer_Date'], dayfirst=True).dt.date
    df = df[['Shop','Transaction_Date','Invoice','Amount_Due','Transfer_Date', 'Amount_Paid']]
    return df

df = read_table()

bill_from = dbc.Row([
	dbc.Col([
		html.H5('Bill From:'),
		html.Br(),
		html.H6('Your Company', style ={'font-size': 18}),
		],
		width = {'size': 6}
		),
	
	dbc.Col([
		html.H5('Billing Date:'),
		dcc.DatePickerSingle(
			id = 'billing_date',
			display_format='DD/MM/YYYY',
			date = dt.today().strftime('%Y-%m-%d')
			),

		html.H5('Statement Period:', style = {'margin-top': 20}),
		dcc.DatePickerRange(
			id = 'statement_period',
			display_format='DD/MM/YYYY',
			start_date_placeholder_text = 'Start Date',
			end_date_placeholder_text = 'End Date',
			clearable= True,
			),
		],
		width = {'size': 6}
		),
	], 
	justify = 'start',
	align = 'start' 
	)

bill_to = dbc.Row([
	dbc.Col([
		html.H5('Bill To:'),
		dbc.Select(
			id="tab_2_bill_to",
			options=[{'label': i, 'value': i} for i in df['Shop'].unique()],
			style = {'width': 350, 'font-size': 20}
			),
		],
		width = {'size': 6}
		),

	dbc.Col([
		html.H5('Total Payable'),
		dbc.InputGroup([
			dbc.InputGroupAddon("$", addon_type="prepend"),
			dbc.Input(type="number", id='total_payable', style = {'font-size': 20}),
			], style = {'width': 350}
			)
		],
		width = {'size': 6}
		),
	], 
	justify = 'start',
	align = 'start' 
	)

selector = dbc.Row([
	dbc.Col([
		html.H6('Show Columns'),
		dcc.Dropdown(
			id="show_columns",
			options=[{'label': i, 'value': i} for i in df.columns.values],
			multi = True,
			style = {'max-height': '45px', 'font-size': 15, 'width': '500px'},
			value= ['Shop', 'Invoice', 'Transaction_Date', 'Amount_Due']
			),
		],
		width = {'size': 7}
		),

	dbc.Col([
		html.H6('Show Outstanding:'),
		dbc.RadioItems(
            options=[
                {"label": "Yes", "value": 'yes'},
                {"label": "No", "value": 'no'},
                {"label": "Both", "value": 'both'}
            ],
            value=2,
            id="show_outstanding",
            inline=True,
        ),
		],
		width = {'size': 4}
		),
	], 
	justify = 'start',
	align = 'start',
	style ={'margin-left': 15}
	)

table = dbc.Row(
	dbc.Col([
		dash_table.DataTable(
			id = 'datatable',
			columns = [{"name": " ".join(i.split('_')), "id": i} for i in df.columns.values],
			data = df.to_dict('rows'),
			style_header = {'font-family': 'Lato', 'fontWeight': 'bold', 'textAlign': 'center'},
			style_cell = {'font-family': 'Lato', 'textAlign': 'center'},
			style_as_list_view=True,
			),
		],
		width = {'size': 10, 'offset': 1},
		)
	)

body = html.Div([
	html.Br(),
	html.H3('Monthly Statement'),
	html.Br(),
	bill_from, 
	html.Br(style ={'t': 15, 'b': 15}),
	bill_to,
	html.Br(),
	html.Hr(),
	selector, 
	html.Br(),
	table
	])

tab_2_layout = html.Div(
	dbc.Container([
		body
		],className='mt-2'
		)
	)
