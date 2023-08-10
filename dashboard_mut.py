import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import pandas as pd
from dash import dash_table
import plotly.express as px



app = dash.Dash(__name__)
app.suppress_callback_exceptions = True


# Updated List of Fund Houses
fund_houses = [
    "ABN__AMRO_Mutual_Fund",
    "Aditya_Birla_Sun_Life_Mutual_Fund",
    "Axis_Mutual_Fund",
    "Bajaj_Finserv_Mutual_Fund",
    "Bandhan_Mutual_Fund",
    "Bank_of_India_Mutual_Fund",
    "Baroda_BNP_Paribas_Mutual_Fund",
    "Baroda_Mutual_Fund",
    "Baroda_Pioneer_Mutual_Fund",
    "Benchmark_Mutual_Fund",
    "BNP_Paribas_Mutual_Fund",
    "BOI_AXA_Mutual_Fund",
    "Canara_Robeco_Mutual_Fund",
    "Daiwa_Mutual_Fund",
    "DBS_Chola_Mutual_Fund",
    "Deutsche_Mutual_Fund",
    "DHFL_Pramerica_Mutual_Fund",
    "DSP_Mutual_Fund",
    "Edelweiss_Mutual_Fund",
    "Essel_Mutual_Fund",
    "Fidelity_Mutual_Fund",
    "Fortis_Mutual_Fund","Franklin_Templeton_Mutual_Fund", "Goldman_Sachs_Mutual_Fund", "Groww_Mutual_Fund", "HDFC_Mutual_Fund", "HSBC_Mutual_Fund", "ICICI_Prudential_Mutual_Fund", "IDBI_Mutual_Fund", "IDFC_Mutual_Fund", "IIFL_Mutual_Fund", "Indiabulls_Mutual_Fund", "ING_Mutual_Fund", "Invesco_Mutual_Fund", "ITI_Mutual_Fund", "JM_Financial_Mutual_Fund", "JPMorgan_Mutual_Fund", "Kotak_Mahindra_Mutual_Fund", "L&T_Mutual_Fund", "LIC_Mutual_Fund", "Mahindra_Manulife_Mutual_Fund", "Mirae_Asset_Mutual_Fund", "Morgan_Stanley_Mutual_Fund", "Motilal_Oswal_Mutual_Fund", "Navi_Mutual_Fund", "Nippon_India_Mutual_Fund", "NJ_Mutual_Fund", "PGIM_India_Mutual_Fund", "PineBridge_Mutual_Fund", "PPFAS_Mutual_Fund", "PRINCIPAL_Mutual_Fund", "Quantum_Mutual_Fund", "Quant_Mutual_Fund", "Reliance_Mutual_Fund", "Sahara_Mutual_Fund", "Samco_Mutual_Fund", "SBI_Mutual_Fund", "Shinsei_Mutual_Fund", "Shriram_Mutual_Fund", "Standard_Chartered_Mutual_Fund", "Sundaram_Mutual_Fund", "Tata_Mutual_Fund", "Taurus_Mutual_Fund", "Trust_Mutual_Fund", "Union_Mutual_Fund", "UTI_Mutual_Fund", "WhiteOak_Capital_Mutual_Fund", "YES_Mutual_Fund"
    ]

initial_layout = html.Div([
    dcc.Dropdown(id='fund-house-dropdown', options=[{'label': fh, 'value': fh} for fh in fund_houses]),
    # html.Button('Submit', id='submit-button'),
    html.Div(id='additional-filters')
])

app.layout = initial_layout

@app.callback(
    Output('additional-filters', 'children'),
    [Input('fund-house-dropdown', 'value')]
)
def update_filters(fund_house):
    if fund_house:
        df = pd.read_csv(f"Fundwise_MutualFund/{fund_house}.csv")
        scheme_type_options = [{'label': 'All', 'value': 'All'}] +[{'label': st, 'value': st} for st in df['Scheme_Type'].unique()]
        scheme_category_options = [{'label': 'All', 'value': 'All'}] + [{'label': sc, 'value': sc} for sc in df['Scheme_Category'].unique()] 
        scheme_code_options = [{'label': 'All', 'value': 'All'}] + [{'label': sc, 'value': sc} for sc in df['Scheme_Code'].unique()] 
        scheme_name_options = [{'label': 'All', 'value': 'All'}] + [{'label': sn, 'value': sn} for sn in df['Scheme_Name'].unique()] 

        # The second layout with additional filters
        return html.Div([
            dcc.Dropdown(id='scheme-type-dropdown', options=scheme_type_options, multi=False),
            dcc.Dropdown(id='scheme-category-dropdown',options=scheme_category_options, multi=False),
            dcc.Dropdown(id='scheme-code-dropdown',options=scheme_code_options, multi=False),
            dcc.Dropdown(id='scheme-name-dropdown',options=scheme_name_options, multi=False),
            html.Button('Submit', id='submit-button'),
            html.Div(id='data-display')
        ])

    return None

@app.callback(
    Output('data-display', 'children'),
    [Input('submit-button', 'n_clicks')],
    [State('fund-house-dropdown', 'value'),
     State('scheme-type-dropdown', 'value'),
     State('scheme-category-dropdown', 'value'),
     State('scheme-code-dropdown', 'value'),
     State('scheme-name-dropdown', 'value')]
)
def update_data(n_clicks, fund_house, scheme_type, scheme_category, scheme_code, scheme_name):
    if n_clicks is None:  # No button clicks yet
        return None

    df = pd.read_csv(f"Fundwise_MutualFund/{fund_house}.csv") if fund_house else pd.DataFrame()
    
    # Apply Scheme_Type filter if not 'All'
    if scheme_type != 'All':
        df = df[df['Scheme_Type'] == scheme_type]

    # Apply Scheme_Category filter if not 'All'
    if scheme_category != 'All':
        df = df[df['Scheme_Category'] == scheme_category]

    # Apply Scheme_Code filter if not 'All'
    if scheme_code != 'All':
        df = df[df['Scheme_Code'] == scheme_code]

    # Apply Scheme_Name filter if not 'All'
    if scheme_name != 'All':
        df = df[df['Scheme_Name'] == scheme_name]

    df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)


    fig = px.line(df, x="Date", y="NAV", title='NAV over Time')

    return dcc.Graph(
        id='line-chart',
        figure=fig
    )



    
if __name__ == '__main__':
    app.run_server(debug=True)
