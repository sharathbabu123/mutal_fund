
import streamlit as st
import pandas as pd
import plotly.express as px

# List of Fund Houses
fund_houses =  [
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


def cal_cagr3y():
    # Make sure 'Date' is a datetime type
    df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)

    # Define the years for which CAGR needs to be calculated
    years = [2018, 2019, 2020, 2021, 2022, 2023]

    # Function to calculate CAGR
    def calculate_cagr(start_value, end_value, years=3):
        return (end_value / start_value) ** (1 / years) - 1

    # Dictionary to store the results
    cagr_results = {}

    # Iterate through the years and calculate CAGR for each 3-year period
    for year in years:
        # Filtering the DataFrame for the given 3-year period
        filtered_df = df[(df['Date'].dt.year >= year - 2) & (df['Date'].dt.year <= year)]
        
        # Get the starting and ending values for the NAV
        start_value = filtered_df[filtered_df['Date'].dt.year == year - 2]['NAV'].iloc[-1]
        end_value = filtered_df[filtered_df['Date'].dt.year == year]['NAV'].iloc[-1]

        # Calculate the CAGR for the 3-year period
        cagr = calculate_cagr(start_value, end_value)

        # Add the CAGR to the results
        cagr_results[year] = cagr * 100  # in percentage

    # Creating a DataFrame to display the results
    cagr_df = pd.DataFrame(list(cagr_results.items()), columns=['Year', 'CAGR 3Y (%)'])
    cagr_df.set_index('Year', inplace=True)

    return cagr_df


st.title('Mutual Fund Analysis')

# Dropdown for selecting the Fund House
fund_house = st.selectbox('Select Fund House:', options=fund_houses)

if fund_house:
    df = pd.read_csv(f"Fundwise_MutualFund/{fund_house}.csv")

    # Dropdowns for other filters
    scheme_type = st.selectbox('Select Scheme Type:', options=['All'] + df['Scheme_Type'].unique().tolist())
    scheme_category = st.selectbox('Select Scheme Category:', options=['All'] + df['Scheme_Category'].unique().tolist())
    scheme_code = st.selectbox('Select Scheme Code:', options=['All'] + df['Scheme_Code'].unique().tolist())
    scheme_name = st.selectbox('Select Scheme Name:', options= df['Scheme_Name'].unique().tolist())

    # Submit button
    if st.button('Submit'):
        if scheme_type != 'All':
            df = df[df['Scheme_Type'] == scheme_type]

        if scheme_category != 'All':
            df = df[df['Scheme_Category'] == scheme_category]

        if scheme_code != 'All':
            df = df[df['Scheme_Code'] == scheme_code]

        
        df = df[df['Scheme_Name'] == scheme_name]

        df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)
        fig = px.line(df, x="Date", y="NAV", title='NAV over Time')
        st.plotly_chart(fig)

        st.header("3-Year CAGR Table throught the years")
        st.table(cal_cagr3y())
