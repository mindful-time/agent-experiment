import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load data from the extracted JSON
# For the sake of this example, we will create dataframes from the extracted data

# UNICEF’s Response and Funding Status
unicef_response_data = {
    'Category': ['Health', 'Nutrition', 'Child Protection', 'Education', 'WASH', 'Cash Transfer', 'SBC'],
    'Access (%)': [41, 145, 131, 58, 34, 59, 76],
    'Funding Status (%)': [12, 51, 31, 70, 22, 0, 5]
}

# Funding Status
funding_status_data = {
    'Funds Received': ['$9.9M'],
    'Carry Forward': ['$22.3M'],
    'Funding Gap': ['$82M']
}

# UNICEF and IPs Response
unicef_ips_response_data = {
    'Sector/Indicator': ['Health', 'Nutrition', 'Education'],
    'Total Needs': [559365, 74025, 421652],
    '2024 Target': [419524, 21647, 186000],
    'Total Results': [2, 21647, 186000]
}

# Create DataFrames
unicef_response_df = pd.DataFrame(unicef_response_data)
funding_status_df = pd.DataFrame(funding_status_data)
unicef_ips_response_df = pd.DataFrame(unicef_ips_response_data)

# Streamlit dashboard layout
st.title('UNICEF Mozambique Humanitarian SitRep Dashboard')

# Display UNICEF’s Response and Funding Status
st.header('UNICEF’s Response and Funding Status')
st.bar_chart(unicef_response_df.set_index('Category'))

# Display Funding Status
st.header('Funding Status')
st.write(f"Funds Received: {funding_status_df['Funds Received'][0]}")
st.write(f"Carry Forward: {funding_status_df['Carry Forward'][0]}")
st.write(f"Funding Gap: {funding_status_df['Funding Gap'][0]}")

# Display UNICEF and IPs Response
st.header('UNICEF and IPs Response')
st.write(unicef_ips_response_df)

# Run the Streamlit app
if __name__ == '__main__':
    st.run()
