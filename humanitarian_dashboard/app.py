import streamlit as st
import json

# Load extracted data
with open('data/extracted_data.json') as f:
    data = json.load(f)

# Dashboard title
st.title('Mozambique Humanitarian Dashboard')

# Display tables and important data points
for table in data['tables']:
    st.subheader(table['name'])
    st.write(table['data'])

st.subheader('Important Data Points')
for point in data['important_data_points']:
    st.write('- ' + point)
