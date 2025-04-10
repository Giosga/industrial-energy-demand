import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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

# Plotting
x = df_selected.index
width = 0.8

fig, ax = plt.subplots(figsize=(15, 10))
bottom = np.zeros(len(df_selected))

colors = {
    'Natural gas': 'red',
    'Manufactured gases': 'orange',
    'Electricity': 'blue',
    'Oil': 'gray',
    'Coal': 'black',
    'Heat': 'purple',
    'Renewables and biofuels': 'green',
    'Other': 'brown'
}

for fuel in df_selected.columns:
    ax.bar(x, df_selected[fuel], width, bottom=bottom, label=fuel, color=colors.get(fuel, None))
    bottom += df_selected[fuel].values

fig.set_facecolor('white')
plt.setp(ax.get_xticklabels(), rotation=60, horizontalalignment='right')
ax.set_ylabel(f'{unit}')
ax.set_title(f'{sector} energy consumption by type of energy over time in {country}')
ax.legend(loc='upper left')
plt.tight_layout()

# Display plot in Streamlit
st.pyplot(fig)