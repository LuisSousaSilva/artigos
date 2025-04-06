# %%
import yfinance as yf
import pandas as pd
import numpy as np

# Download VFINX data
VFINX_data = yf.download('VFINX', start='1950-01-29')

# Use close (yahoo finance adjusted close)
VFINX_data = VFINX_data['Close']

# Calculate 2-day returns
VFINX_data['2_day_return'] = VFINX_data['VFINX'].pct_change(periods=2)

# Count occurrences where 2-day return is less than -0.10 (10% drop)
drops_over_10_percent = (VFINX_data['2_day_return'] < -0.10).sum()

# Calculate probability (excluding NaN)
total_valid_periods = VFINX_data['2_day_return'].count()
probability = drops_over_10_percent / total_valid_periods

probability * 100

# %%
import plotly.express as px

fig = px.histogram(
    VFINX_data,
    x='2_day_return',
    nbins=50,
    title='Histogram of 2-Day Returns',
    color_discrete_sequence=['royalblue']
)

fig.update_layout(
    height=500,
    width=990,
    title_x=0.5,
    paper_bgcolor='#F5F6F9',
    plot_bgcolor='#F5F6F9',
    hovermode='x',
    xaxis=dict(
        title='2-Day Return',
        tickfont=dict(color='#4D5663'),
        gridcolor='#E1E5ED',
        titlefont=dict(color='#4D5663'),
        zerolinecolor='#E1E5ED',
        showgrid=True
    ),
    yaxis=dict(
        title='Frequency',
        tickfont=dict(color='#4D5663'),
        gridcolor='#E1E5ED',
        titlefont=dict(color='#4D5663'),
        zerolinecolor='#E1E5ED',
        showgrid=True
    ),
    images=[dict(
        name="watermark_1",
        source="https://raw.githubusercontent.com/LuisSousaSilva/Articles_and_studies/master/FP-cor-positivo.png",
        xref="paper",
        yref="paper",
        x=-0.055,
        y=1.25,
        sizex=0.2,
        sizey=0.2,
        opacity=1,
        layer="below"
    )],
    annotations=[dict(
        xref="paper",
        yref="paper",
        x=0.5,
        y=-0.125,
        xanchor="center",
        yanchor="top",
        text='',
        showarrow=False,
        font=dict(family="Arial", size=12, color="rgb(150,150,150)")
    )]
)

fig.show()

# %%
# Filter rows with 2-day drop > 10%
drop_days = VFINX_data[VFINX_data['2_day_return'] < -0.10]
drop_days

# %%
# Calculate 1-day returns
VFINX_data['1_day_return'] = VFINX_data['VFINX'].pct_change()

# Count days with drop > 5%
drops_over_5_percent = (VFINX_data['1_day_return'] < -0.05).sum()

drop_5_days = VFINX_data[VFINX_data['1_day_return'] < -0.05]

drops_over_5_percent

# %%
drop_5_days[['VFINX', '1_day_return']]

# %%



