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

def read_sql():
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    query = """ SELECT * FROM invoice """
    df = pd.read_sql(query, conn)
    return df
df = read_sql()

billing_info = dbc.Form([
	dbc.FormGroup([
		html.H5('Bill To*'),
		dbc.Select(
			id="select_shop",
			options=[{'label': i, 'value': i} for i in df['Shop'].unique()],
			),
		dbc.FormText("*Fill in the next row for new shops")
		]),

	html.Br(),

	dbc.FormGroup([
		html.H5('New Shop Name'),
		dbc.Input(
			id='select_new_shop', 
			type ='text'
			)
		]),

	html.Br(),

	dbc.FormGroup([
		html.H5('Bill From'),
		dbc.Input(
			id='select_bill_from', 
			type ='text', 
			placeholder = 'Edit Biling Details',
			value = 'My Shop'),
		html.Br(),
		html.P(id="output_bill_from", style = {'font-size': 18})
		])
	],
	)

invoice_info = dbc.Form([
	dbc.FormGroup([
		html.H5('Invoice Number*'),
		dbc.Input(
			id="select_invoice",
			type = 'number'
			),
		dbc.FormText("*Required Field", style ={'font-color': 'red'})
		]),

	html.Br(),

	dbc.FormGroup([
		html.H5('Amount Payable'),
		dbc.InputGroup([
			dbc.InputGroupAddon("$", addon_type = 'prepend'),
			dbc.Input(placeholder ='Amount', type ="number", id='select_amount',)
			]),
		]),

	html.Br(),

	dbc.FormGroup([
		html.H5('Transaction Date'),
		dcc.DatePickerSingle(
	        id="select_payment_date",
	        display_format='Do MMM, YYYY',
	        placeholder='Date',
	        clearable=True,
	        style = {'width': 20}
	        )],
		),
	])	

form = html.Div([
	dbc.Row([
			dbc.Col(billing_info, width = 5),
			dbc.Col(invoice_info, width =5)
		],justify = 'around'
		),
	
	html.Hr(),

	dbc.Row([

		dbc.Col(
			html.Div(
				id='output-to-sql'
				),
			width = {'offset': 6, 'size': 4}
			),

		dbc.Col([
			dbc.Button(
				'Submit', 
				id= 'button', 
				color = 'primary'
				)], 
			width = {'size': 2},
			),
		], 
		justify = 'around',
		align = 'center',
		), 
	])
	 
tab_3_layout = html.Div(
	dbc.Container([
		html.Br(),
		form,
		],
		className='mt-4'
		)
	)
