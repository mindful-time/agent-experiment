import streamlit as st
import pandas as pd
import folium
import plotly.express as px
from streamlit_folium import st_folium


# Load data from the extracted PDF
# UNICEF Response and Funding Status
unicef_response = pd.DataFrame({
    'Category': ['Health', 'Nutrition', 'Child Protection', 'Education', 'WASH', 'Cash Transfer', 'SBC'], 
    'Access': ['41%', '145%', '131%', '58%', '34%', '59%', '76%'],
    'Funding Status': ['12%', '51%', '31%', '70%', '22%', '0%', '5%']
})

# Funding Status
funding_status = pd.DataFrame({
    'Funds Received': ['$9.9M'],
    'Carry Forward': ['$22.3M'],
    'Funding Gap': ['$82M']
})

# Summary of Programme Results: Northern Mozambique 2024
northern_moz_results = pd.DataFrame({
    'Sector/Indicator': ['Health', '# children and women accessing primary healthcare in UNICEF-supported facilities',
                         '# of individuals receiving treatment for cholera/acute watery diarrhoea in UNICEF-supported facilities',
                         'HIV', 'Number of children 6-59 months with severe wasting admitted for treatment',
                         'Number of children 6-59 months screened for wasting',
                         'Number of primary caregivers of children 0-23 months receiving IYCF counselling',
                         'Number of children 6-59 months receive routine vitamin A supplementation',      
                         'Child Protection', '# women, girls and boys accessing GBV risk mitigation, prevention and/or response interventions',
                         '# people with safe and accessible channels to report SEA by personnel who provide assistance to affected populations',
                         '# children who have received individual case management', 'Education',
                         '# teachers (m/f) and other Education Personnel trained in EiE related topics',  
                         'WATER, SANITATION & HYGIENE', 'Number of people use safe and appropriate sanitation facilities',
                         'Number of people reached with hand-washing behaviour-change programmes',        
                         'Number of people reached with critical WASH supplies', 'Social Protection',     
                         'Number households benefiting from new or additional social assistance (cash/in-kind) measures from governments with UNICEF-technical assistance support'],
    'Total Needs': [559365, 338045, 56964, 3570, 74025, 900307, 368547, 863447, 612957, 706000, 612957, 98073, 421652, 5492, 1343233, 1344808, 1412706, 1413706, 86000, 120824],
    '2024 Target': [419524, 253540, 56964, 2859, 21647, 210258, 92973, 210258, 186362, 141900, 134904, 29818, 186000, 1716, 333508, 134403, 133403, 833769, 23000, 86000],
    'Total Results': [2, 137072, 13521, 838, 8567, 235921, 47872, 228511, 304521, 55468, 435179, 15401, 191278, 1326, 149217, 13655, 122401, 102770, 13482, 67879],
    '+/- since last report (Jan-March)': [0, 91658, 3580, 740, 4829, 179340, 20025, 179340, 103935, 13393, 195107, 6513, 36665, 43, 120130, 11870, 43200, 22040, 9015, 36904],
    'Cluster/Sector 2024 Target': [338045, 56964, 3570, 740, 74025, 371716, 368547, 371716, 232952, 236473, 98073, 98073, 300657, 4233, 987886, 987886, 987886, 987886, 120824, 280000],
    'Cluster/Sector Total Results': [253540, 56964, 2859, 838, 8567, 306977, 80773, 283130, 312005, 68158, 29818, 16384, 402220, 5362, 380125, 67355, 809525, 206380, 86000, 2225869],
    'Cluster/Sector +/- since last report (Jan-March)': [137072, 0, 838, 740, 21647, 306888, 184133, 306888, 111858, 15168, 15401, 6513, 126753, 782, 204083, 47575, 276410, 52715, 67879, 2548673]
})

# Create a Streamlit dashboard
st.title('Mozambique Humanitarian SitRep Mid-Year 2024 Dashboard')

# Display UNICEF Response and Funding Status
st.header('UNICEF Response and Funding Status')
st.dataframe(unicef_response)

# Display Funding Status
st.header('Funding Status')
st.dataframe(funding_status)

# Display Summary of Programme Results: Northern Mozambique 2024
st.header('Summary of Programme Results: Northern Mozambique 2024')
st.dataframe(northern_moz_results)

# Create a map using Folium
st.header('Map of Affected Areas')
map_center = [-15.0, 40.0]  # Center of Mozambique
map_zoom = 8
m = folium.Map(location=map_center, zoom_start=map_zoom)

# Add markers for key data points (example)
folium.Marker(location=[-15.5, 39.5], popup='Cabo Delgado - Conflict Affected').add_to(m)
folium.Marker(location=[-15.0, 39.0], popup='Nampula - Displacement').add_to(m)

# Display the map using streamlit-folium
st_folium(m, width=700, height=500)

# Create charts using Plotly
st.header('Funding Gap by Sector')
funding_gap_data = pd.DataFrame({
    'Sector': ['Health & HIV/AIDs', 'Nutrition', 'Child Protection', 'Education', 'WASH', 'Social Protection', 'Cross-Sectoral', 'Total'],
    'Funding Gap (%)': [88, 52, 70, 30, 79, 100, 95, 72]
})
fig = px.bar(funding_gap_data, x='Sector', y='Funding Gap (%)', title='Funding Gap by Sector')
st.plotly_chart(fig)

# Download button for PDF
st.header('Download Report')
if st.button('Download as PDF'):
    # Code to generate PDF report
    pass
