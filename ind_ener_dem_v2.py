import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# Load data
df_ind = pd.read_csv('Eurostat energy balances_industries.csv') 

# Sidebar selectors
st.sidebar.title("Filter Options")
sector = st.sidebar.selectbox("Select sector", sorted(df_ind['nrg_bal'].unique()))
unit = st.sidebar.selectbox("Select unit", sorted(df_ind['unit'].unique()))
country = st.sidebar.selectbox("Select country", sorted(df_ind['geo'].unique()))

# Define year range
years = [ '2005', '2006', '2007', '2008', '2009',
          '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018',
          '2019', '2020', '2021', '2022', '2023']

# Filter and reshape data
selected = df_ind[
    (df_ind['nrg_bal'] == sector) &
    (df_ind['unit'] == unit) &
    (df_ind['geo'] == country)
]

selected = selected[['siec'] + years]
selected.set_index('siec', inplace=True)

# Transpose for plotting: years as index, fuels as columns
df_selected = selected.T
df_selected.drop(columns=['Total'], errors='ignore', inplace=True)
df_selected.dropna(axis=0, how='all', inplace=True)
df_selected.fillna(0, inplace=True)
# Filter out fuels where all values are 0 or NaN
nonzero_fuels = df_selected.loc[:, (df_selected != 0).any(axis=0)]


# Create a list to hold traces
traces = []

x = nonzero_fuels.index  # years

# Create a bottom array to stack bars
bottom = np.zeros(len(df_selected))

colors = {
    'Solid fossil fuels': 'brown',
    'Peat and peat products': 'navy',
    'Natural gas': 'red',
    'Manufactured gases': 'orange',
    'Electricity': '#13EAC9',
    'Oil': 'gray',
    'Oil and petroleum products (excluding biofuel portion)': '#580F41',
    'Nuclear heat': 'blue',
    'Heat': 'lime',
    'Renewables and biofuels': 'green',
    'Oil shale and oil sands': '#A52A2A'
}

for fuel in nonzero_fuels.columns:
    traces.append(
        go.Bar(
            x=x,
            y=nonzero_fuels[fuel],
            name=fuel,
            marker=dict(color=colors.get(fuel, None)),
        )
    )

# Create the figure
fig = go.Figure(data=traces)

fig.update_layout(
    barmode='stack',
    title=dict(
        text=f'{sector} energy consumption by type of energy over time in {country}',
        x=0.5,
        xanchor='center',
        yanchor='top',
        y=0.95
    ),
    xaxis=dict(
    tickangle=-60,
    tickmode='linear',  # ensures all ticks are shown (assuming they are numeric)
    tickfont=dict(
        size=12,
        color='black'
    )),
    xaxis_title='Year',
    yaxis_title=unit,
    legend=dict(
        x=0.01,
        y=0.99,
        xanchor='left',
        yanchor='top',
        bgcolor='rgba(255,255,255,0.7)',  # transparent background
        bordercolor='rgba(0,0,0,0)',    # no border
        font=dict(color='black', size=14)
    ),
    plot_bgcolor='white',
    height=700,
    margin=dict(t=100, b=80, r=60),
)


# Display in Streamlit
st.plotly_chart(fig, use_container_width=True)