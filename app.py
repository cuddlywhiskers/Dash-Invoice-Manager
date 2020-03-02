# dash and python modules  
import os
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
from datetime import datetime as dt
import pandas as pd
import numpy as np
import sqlite3
import sqlalchemy 
import tab_1
import tab_2
import tab_3

stylesheets=[dbc.themes.FLATLY]
app = dash.Dash(__name__, external_stylesheets= stylesheets)
server = app.server
app.config['suppress_callback_exceptions'] = True

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

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Dashboard", href="/dashboard",  id="page-1-link")),
        dbc.NavItem(dbc.NavLink("Monthly Statement", href="/view-invoice",  id="page-2-link")),
        dbc.NavItem(dbc.NavLink("Manage Invoice", href="/manage-invoice",  id="page-3-link")),

    ],
    brand="Overall Financial Performance & Accounting Tool",
    brand_href="/",
    sticky="top",
    dark = True,
    color = 'primary'
)

app.layout = html.Div([
	navbar,
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

# TAB1 FUNCTIONS
def calculate_card(df):
    total_revenue = round((df['Amount_Due'].sum()), 2)
    total_average = round((df['Amount_Due'].mean()), 2)
    total_invoice = df['Invoice'].count()
    total_clients = df['Shop'].nunique()
    
    return total_revenue, total_average, total_invoice, total_clients

# create functions for graphing manipulation
def piechart(df):

    groupbyShop = df.groupby('Shop').agg({'Amount_Due': 'sum', 'Invoice':'count'}).reset_index()
    invoice = groupbyShop['Invoice'].values
    amount = groupbyShop['Amount_Due'].values
    shop = groupbyShop['Shop'].values

    colors = ['gold', 'mediumturquoise', 'darkorange', 'lightgreen']

    fig = make_subplots(rows=2, cols=1, specs=[[{"type": "pie"}], [{"type" : "pie"}]])

    fig.add_trace(
        go.Pie(
            labels = shop,
            values = amount,
            hole = 0.5,
            textinfo= 'percent+label',
            marker = {'colors': colors , 'line':{'width': 2}},
            name ='revenue'
            ), 
        1, 1
        )

    fig.add_trace(
        go.Pie(
            labels = shop,
            values = invoice,
            hole = 0.5,
            textinfo= 'percent+label',
            marker = {'line':{'width': 2}},
            name = 'invoice'
            ), 
        2, 1
        )

    fig.update_layout(
    title_text="Revenue & Invoice Breakdown",
    width = 380,
    annotations=[dict(text='<b>Revenue<b>', x=-0.25, y=1.1, font_size=12, showarrow=False),
                 dict(text='<b>Invoice<b>', x=-0.25, y=0.45, font_size=12, showarrow=False)])
    return fig

def aggregate_revenue(df, view):
    d = {
        'daily': 'D',
        'weekly' : 'W-MON',
        'monthly' : 'M',
        'yearly' : 'Y'
        }

    df2 = df.set_index("Transaction_Date")
    df2 = df2.groupby(pd.Grouper(freq= d[view])).agg({'Amount_Due' : 'sum', 'Invoice': 'count'})
    df2 = df2.reset_index().sort_values('Transaction_Date')

    if view == 'monthly':
        df2['xaxis'] = df2['Transaction_Date'].dt.month_name()
    elif view == 'yearly':
        df2['xaxis'] = df2['Transaction_Date'].dt.year
    else:
        df2['xaxis'] = df2['Transaction_Date']

    return df2

def avg_revenue_plot(df, view):
    bargap_d = {
        'daily': 0.15,
        'weekly' : 0.3,
        'monthly' : 0.92,
        'yearly' : 0.92
        }

    df2 = aggregate_revenue(df, view)
    df2['Average'] = df2['Amount_Due'] / df2['Invoice']
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Bar(
            x = df2['xaxis'],
            y = df2['Average'], 
            name = 'Revenue',
            marker_color =  'LightSalmon',
            ),
        secondary_y=False,)

    fig.add_trace(
        go.Scatter(
            x = df2['xaxis'], 
            y = df2['Invoice'], 
            name = 'Invoice',
            line = {'color': 'Steelblue'}
            ), 
        secondary_y=True,
        )

    fig.update_layout(
        title_text='Average Revenue & Total Invoice', 
        plot_bgcolor = 'rgba(0,0,0,0)', 
        bargap = bargap_d[view],
        legend=dict(x=0.8, y=1.2)
        )
    fig.update_xaxes(
        title_text="Date", 
        showline= True, 
        linecolor = 'black'
        )
    fig.update_yaxes(
        title_text="Avg <b>Revenue</b> ($)", 
        secondary_y=False, 
        )
    fig.update_yaxes(
        title_text="Total <b>Invoice</b>", 
        secondary_y=True
        )
    return fig

def revenue_by_shop_plot(df, shop, view):
    fig = go.Figure()
    traces = []

    # overall revenue
    dff = aggregate_revenue(df, view)
    
    fig.add_trace(
        go.Scatter(
            x=dff['xaxis'],
            y=dff['Amount_Due'],
            mode='lines+markers',
            name='Total',
            opacity=0.8,
            line = {'color': 'black', 'width': 1.5},
            marker={'size': 5}
            )
        )

    # revenue per shop
    for i in shop:
        filter_by_shop = df[df['Shop'] == i]
        agg_per_shop = aggregate_revenue(filter_by_shop, view)

        fig.add_trace(
            go.Scatter(
                x=agg_per_shop['xaxis'],
                y=agg_per_shop['Amount_Due'],
                mode='lines',
                opacity=0.7,
                line = {'width': 1.5},
                name=i
                )
            )

    fig.update_layout(title_text='Total Revenue', plot_bgcolor = 'rgba(0,0,0,0)', margin={'r': 20},legend=dict(x=0.9, y=1.2))
    fig.update_xaxes(title_text="Date", showline= True, linecolor = 'black')
    fig.update_yaxes(title_text="Total <b>Revenue</b> ($)")
    return fig

def scatter_plot(df, shop):
    fig = go.Figure()
    traces = []
    df = df.set_index('Transaction_Date')
    for i in shop:
        filter_by_shop = df[df['Shop'] == i]
        grouped_df = filter_by_shop.groupby([pd.Grouper(freq= 'W-MON')]).agg({'Amount_Due': 'sum', 'Invoice': 'count'}).reset_index()
        grouped_df['Transaction_Date'] = pd.to_datetime(grouped_df['Transaction_Date'])
        grouped_df['Average'] =  'Avg $' + ((grouped_df['Amount_Due'] / grouped_df['Invoice']).round(2)).astype(str) 

        fig.add_trace(
            go.Scatter(
                x=grouped_df['Invoice'],
                y=grouped_df['Amount_Due'],
                text= grouped_df['Average'],
                mode='markers',
                opacity=0.8,
                marker={
                    'size': 7,
                    'line': {'width': 0.5, 'color': 'white'}
                },
                name=i
            ))

    fig.update_layout(title_text='Revenue vs Invoice Per Week', plot_bgcolor = 'rgba(0,0,0,0)',)
    fig.update_xaxes(title_text="Weekly <b>Revenue<b>", showline= True, linecolor = 'black')
    fig.update_yaxes(title_text="Weekly <b>Invoice<b>")
    return fig

# Update the index
@app.callback(Output('page-content', 'children'), 
    [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/dashboard':
        return tab_1.tab_1_layout
    elif pathname == "/view-invoice":
        return tab_2.tab_2_layout
    elif pathname == '/manage-invoice':
        return tab_3.tab_3_layout
    else:
        return tab_1.tab_1_layout

# tab 1 graphs
@app.callback([Output('card1', 'children'),
    Output('card2', 'children'),
    Output('card3', 'children'),
    Output('card4', 'children'),
    Output('daily-revenue', 'figure'),
    Output('piechart', 'figure'),
    Output('revenue-by-shop', 'figure'),
    Output('scatterplot', 'figure')],
    [Input('tab_1_view', 'value'),
    Input('tab_1_shop', 'value'),
    Input('tab_1_time', 'start_date'),
    Input('tab_1_time', 'end_date')])
def dashboard_callback (view, shop, start_date, end_date):
    df = read_table()
    df['Transaction_Date'] = pd.to_datetime(df['Transaction_Date'], dayfirst=True)
    
    if shop is not None:
        dff = df[df['Shop'].isin(shop)]
    if start_date and end_date is not None:
        dff = dff.loc[dff['Transaction_Date'] >= start_date][dff['Transaction_Date'] <= end_date]

    card1, card2, card3, card4 = calculate_card(dff)
    piechart_fig = piechart(dff)
    shop_revenue_fig =  revenue_by_shop_plot(dff, shop, view)
    scatter_fig = scatter_plot(dff, shop)
    combined_fig = avg_revenue_plot(dff, view)

    return [ "$"+str(card1),  "$"+str(card2), str(card3), card4, shop_revenue_fig, piechart_fig, combined_fig, scatter_fig]

# TAB 2 - manage invoice
@app.callback(
    [Output('datatable', 'columns'),
    Output('datatable', 'data'),
    Output('total_payable', 'value')],
    [Input('show_columns', 'value'),
    Input('tab_2_bill_to', 'value'),
    Input('statement_period', 'start_date'),
    Input('statement_period', 'end_date'),
    Input('show_outstanding', 'value')])
def update_table(choosen_cols, vendor, start_period, end_period, outstanding):
    # choose columns
    df = read_table

    columns = []
    df = read_table()   
    df['Amount_Paid'] = df['Amount_Paid'].fillna(0)
    df['Remaining'] = df['Amount_Due'] - df['Amount_Paid']
    # choose outstanding
    if outstanding == 'yes':
        dff = df.loc[df['Remaining'] > 0]
    elif outstanding == 'no':
        dff = df.loc[df['Remaining'] == 0]
    else:
        dff = df.loc[df['Remaining'] >= 0]

    # choose column
    all_cols = [{"name": " ".join(i.split('_')), "id": i} for i in df.columns.values]
    for cols in choosen_cols:
        for col_info in all_cols:
            if cols == col_info['id']:
                columns.append(col_info)
    dff = dff[choosen_cols]

    # choose shop
    if vendor is not None:
        dff = dff.loc[dff['Shop'] == vendor]
    # choose date period
    if start_period is not None and end_period is not None:
        start_period = dt.strptime(start_period, "%Y-%m-%d").date()
        end_period = dt.strptime(end_period, "%Y-%m-%d").date()
        dff = dff.loc[dff['Transaction_Date'] >= start_period][dff['Transaction_Date'] <= end_period]
    
    data = dff.to_dict('rows')

    if 'Amount_Due' not in choosen_cols:
        total_payable = 0
    else:
        total_payable = dff['Amount_Due'].sum()
    
    return [columns, data, total_payable]

# tab 3 callbacks
@app.callback(
    Output('output_bill_from', 'children'),
    [Input('select_bill_from', 'value')])
def output_text(value):
    if value == 'My Shop':
        return 'HSK Seafood PTE LTD'
    else:
        return value

# update sql database with new invoices 
@app.callback(
    Output('output-to-sql', 'children'),
    [Input('button', 'n_clicks')],
    state=[
        State('select_shop', 'value'),
        State('select_new_shop', 'value'),
        State('select_invoice','value'),
        State('select_amount','value'),
        State('select_payment_date', 'date')])
def update_database(n_clicks, select_shop, select_new_shop, select_invoice, select_amount, start_date,):  
    # call sql connections
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    df = read_table()

    # ensure that callback not called upon refresh
    if n_clicks is None:
        raise PreventUpdate
    elif select_invoice is None:
        return ('Invoice cannot be Empty!')
    else:
    # clean data inputs before sending them back to the sql
        if select_new_shop is None:
            shopname = select_shop
        else: 
            shopname = select_new_shop

        if start_date is not None:
            start_date = '/'.join((start_date.split('-'))[::-1])

        end_date = None 
        amount_paid = 0

        # create new invoice entry , convert to df and send to sql
        new_entry_df = pd.DataFrame(
            data = [[shopname, start_date, select_invoice, select_amount, end_date, amount_paid]], 
            columns = df.columns.values, 
            index=[0])

        new_entry_df.to_sql(
            'invoice', 
            con=conn, 
            index=False,
            if_exists='append'
            )

        return "Invoice Number {} has been submitted!".format(select_invoice)

if __name__ == '__main__':
    app.run_server(debug = True)