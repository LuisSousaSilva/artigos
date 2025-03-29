#%%
import plotly.graph_objects as go
import ds4finance as dsf
import yfinance as yf
import pandas as pd

# %%
# Download SPY data
spy_data = yf.download("SPY", start="2000-01-01", end="2024-11-27", progress=False)

# %%
# Extract adjusted close column
spy = spy_data[['Adj Close']].rename(columns={"Adj Close": "SPY"})

spy = dsf.compute_growth_index(spy)

#%%
# Calculate the midpoint date
start_date = spy.index.min()
end_date = spy.index.max()

# Find the midpoint date
midpoint_date = start_date + (end_date - start_date) / 2
midpoint_date

#%%
spy_ret = spy.pct_change().dropna()

spy_ret

#%%
# Define the crisis dates and corresponding y-axis values
crisis_date_2000 = '2001-07-07'
crisis_value_2000 = 6  # Arrow pointing to 10% for the 2008 crisis

# Define the crisis dates and corresponding y-axis values
crisis_date_2008 = '2008-07-07'
crisis_value_2008 = 11  # Arrow pointing to 10% for the 2008 crisis

covid_date = '2019-12-15'  # Approximate start of the COVID crisis
covid_value = 8  # Arrow pointing to 15% for the COVID crisis

# Create the chart
fig = dsf.ichart(spy_ret * 100, image='fp', yticksuffix='%',
                  yTitle='Em percentagem',
                  title= "Retornos diários do SPY")

# Add annotation for .com burst
fig.add_annotation(
    x=crisis_date_2000,
    y=crisis_value_2000,  # Point to 8%
    text="Rebentar da bolha .com",
    showarrow=True,
    arrowhead=2,
    ax=30,
    ay=-50,
    arrowwidth=3,
    font=dict(size=12, color="black"),
    arrowcolor="black"
)

# Add annotation for 2008 crisis
fig.add_annotation(
    x=crisis_date_2008,
    y=crisis_value_2008,  # Point to 10%
    text="Crash de 2008",
    showarrow=True,
    arrowhead=2,
    ax=-40,
    ay=-50,
    arrowwidth=3,
    font=dict(size=12, color="black"),
    arrowcolor="black"
)

# Add annotation for COVID-19 crisis
fig.add_annotation(
    x=covid_date,
    y=covid_value,  # Point to 8%
    text="Crash do COVID-19",
    showarrow=True,
    arrowhead=2,
    ax=-30,
    ay=-50,
    arrowwidth=3,
    font=dict(size=12, color="black"),
    arrowcolor="black"
)

# Show the chart
fig.show()



# %%
# Reverse the order of the returns while maintaining the same dates
spy_ret_reversed = spy_ret.copy()

spy_ret_reversed['SPY'] = spy_ret['SPY'].iloc[::-1].values

spy_ret_reversed

#%%
# Define the crisis dates and corresponding y-axis values
crisis_date_2000 = '2022-07-07'
crisis_value_2000 = 6  # Arrow pointing to 10% for the 2008 crisis

# Define the crisis dates and corresponding y-axis values
crisis_date_2008 = '2015-07-07'
crisis_value_2008 = 11  # Arrow pointing to 10% for the 2008 crisis

covid_date = '2004-04-15'  # Approximate start of the COVID crisis
covid_value = 8  # Arrow pointing to 15% for the COVID crisis

# Create the chart
fig = dsf.ichart(spy_ret_reversed * 100, image='fp', yticksuffix='%',
                  yTitle='Em percentagem',
                  title= "Retornos diários do Reversed SPY")

# Add annotation for .com burst
fig.add_annotation(
    x=crisis_date_2000,
    y=crisis_value_2000,  # Point to 8%
    text="Rebentar da bolha .com",
    showarrow=True,
    arrowhead=2,
    ax=-30,
    ay=-50,
    arrowwidth=3,
    font=dict(size=12, color="black"),
    arrowcolor="black"
)

# Add annotation for 2008 crisis
fig.add_annotation(
    x=crisis_date_2008,
    y=crisis_value_2008,  # Point to 10%
    text="Crash de 2008",
    showarrow=True,
    arrowhead=2,
    ax=-40,
    ay=-50,
    arrowwidth=3,
    font=dict(size=12, color="black"),
    arrowcolor="black"
)

# Add annotation for COVID-19 crisis
fig.add_annotation(
    x=covid_date,
    y=covid_value,  # Point to 8%
    text="Crash do COVID-19",
    showarrow=True,
    arrowhead=2,
    ax=-30,
    ay=-50,
    arrowwidth=3,
    font=dict(size=12, color="black"),
    arrowcolor="black"
)

# Show the chart
fig.show()
# %%
spy_reversed = dsf.compute_time_series(spy_ret_reversed)

#%%
# Define start, midpoint, and end dates
start_date = spy.index.min()
end_date = spy.index.max()
midpoint_date = start_date + (end_date - start_date) / 2

# Create the chart using dsf.ichart
fig = dsf.ichart(spy, image='fp', yticksuffix='$',
                  yTitle='Valorização de 100 doláres investidos',
                  title= "Crescimento de SPY (com base 100)",
                  source_text=f'Valor final de {round(spy.iloc[-1].iloc[0], 2)} usd')

# Add shading for the bear market (start to midpoint)
fig.add_shape(
    type="rect",
    x0=str(start_date), x1=str(midpoint_date),
    y0=spy['SPY'].min(), y1=spy['SPY'].max(),
    fillcolor="lightcoral",  # Light red
    opacity=0.2,
    layer="below",
    line_width=0,
)

# Add shading for the bull market (midpoint to end)
fig.add_shape(
    type="rect",
    x0=str(midpoint_date), x1=str(end_date),
    y0=spy['SPY'].min(), y1=spy['SPY'].max(),
    fillcolor="lightgreen",  # Light green
    opacity=0.2,
    layer="below",
    line_width=0,
)

# Lower the text slightly by subtracting a small value from the maximum
text_position_y = spy['SPY'].max() - (spy['SPY'].max() * 0.05)  # Adjust 5% below max

# Add annotation for Bear Market
fig.add_annotation(
    x=str((midpoint_date - (end_date - midpoint_date) / 2)),  # Center of the red section
    y=text_position_y,  # Slightly below the top
    text="Secular Bear Market",
    showarrow=False,
    font=dict(size=14, color="darkred"),
    xanchor="center",
    yanchor="top",
)

# Add annotation for Bull Market
fig.add_annotation(
    x=str((midpoint_date + (end_date - midpoint_date) / 2)),  # Center of the green section
    y=text_position_y,  # Slightly below the top
    text="Secular Bull Market",
    showarrow=False,
    font=dict(size=14, color="darkgreen"),
    xanchor="center",
    yanchor="top",
)

# Show the chart
fig.show()

# %%
fig = dsf.ichart(spy_reversed, image='fp', yticksuffix='$',
                  yTitle='Valorização de 100 doláres investidos',
                  title= "Crescimento de SPY (com base 100)",
                  source_text=f'Valor final de {round(spy_reversed.iloc[-1].iloc[0], 2)} usd')

# Add shading for the bear market (start to midpoint)
fig.add_shape(
    type="rect",
    x0=str(start_date), x1=str(midpoint_date),
    y0=spy_reversed['SPY'].min(), y1=1200,
    fillcolor="lightgreen",  # Light red
    opacity=0.2,
    layer="below",
    line_width=0,
)

# Add shading for the bull market (midpoint to end)
fig.add_shape(
    type="rect",
    x0=str(midpoint_date), x1=str(end_date),
    y0=spy_reversed['SPY'].min(), y1=1200,
    fillcolor="lightcoral",  # Light green
    opacity=0.2,
    layer="below",
    line_width=0,
)

# Lower the text slightly by subtracting a small value from the maximum
text_position_y = spy_reversed['SPY'].max() - (spy_reversed['SPY'].max() * 0.05)

# Add annotation for Bear Market
fig.add_annotation(
    x=str((midpoint_date - (end_date - midpoint_date) / 2)),  # Center of the red section
    y=text_position_y,  # Slightly below the top
    text="Secular Bull Market",
    showarrow=False,
    font=dict(size=14, color="darkgreen"),
    xanchor="center",
    yanchor="top",
)

# Add annotation for Bull Market
fig.add_annotation(
    x=str((midpoint_date + (end_date - midpoint_date) / 2)),  # Center of the green section
    y=text_position_y,  # Slightly below the top
    text="Secular Bear Market",
    showarrow=False,
    font=dict(size=14, color="darkred"),
    xanchor="center",
    yanchor="top",
)
# %%
# Resample SPY prices to monthly frequency to calculate monthly returns
spy_monthly = spy.resample('ME').last()
monthly_returns = spy_monthly.pct_change().dropna()

# Initialize variables for the simulation
initial_investment = 10000
monthly_contribution = 200
portfolio_value = [initial_investment]

# Simulate the portfolio growth
for i in range(len(monthly_returns)):
    # Add monthly contribution
    portfolio_value.append(portfolio_value[-1] * (1 + monthly_returns.iloc[i, 0]) +
                            monthly_contribution)

# Create a DataFrame for the simulated portfolio value
simulation_dates = monthly_returns.index
portfolio_simulation_spy = pd.DataFrame({'Portfolio Value': portfolio_value[1:]},
                                         index=simulation_dates)

dsf.ichart(portfolio_simulation_spy)
# %%
# Resample spy_reversed prices to monthly frequency to calculate monthly returns
spy_reversed_monthly = spy_reversed.resample('ME').last()
monthly_returns = spy_reversed_monthly.pct_change().dropna()

# Initialize variables for the simulation
initial_investment = 10000
monthly_contribution = 200
portfolio_value = [initial_investment]

# Simulate the portfolio growth
for i in range(len(monthly_returns)):
    # Add monthly contribution
    portfolio_value.append(portfolio_value[-1] * (1 + monthly_returns.iloc[i, 0]) +
                            monthly_contribution)

# Create a DataFrame for the simulated portfolio value
simulation_dates = monthly_returns.index
portfolio_simulation_reversed_spy = pd.DataFrame({'Portfolio Value': portfolio_value[1:]},
                                                  index=simulation_dates)

dsf.ichart(portfolio_simulation_reversed_spy)

#%%

simulation = dsf.merge_time_series(portfolio_simulation_spy, portfolio_simulation_reversed_spy)

simulation.columns = ['SPY com reforços', 'Reversed_SPY com reforços']

fig = dsf.ichart(simulation,
                 title = "SPY com reforços vs Reversed_SPY com reforços",
                 image='fp', yticksuffix='$',
                 yTitle = "Valorizaç=ão dos investimentos")

fig.update_layout(
    legend=dict(
        orientation="h",  # Horizontal orientation
        yanchor="bottom",  # Align to the bottom
        y=-0.2,  # Position below the chart
        xanchor="center",  # Center horizontally
        x=0.5  # Center of the x-axis
    )
)

fig.show()

# %%
ts = dsf.merge_time_series(spy, spy_reversed)

ts.columns = ['SPY', 'Reversed_SPY']

fig = dsf.ichart(ts, title= "SPY vs Reversed SPY",
            yTitle='Valorização por cada 100 dólares investidos',
            image='fp', yticksuffix='$',
            )

fig.update_layout(
    legend=dict(
        orientation="h",  # Horizontal orientation
        yanchor="bottom",  # Align to the bottom
        y=-0.2,  # Position below the chart
        xanchor="center",  # Center horizontally
        x=0.5  # Center of the x-axis
    )
)

fig.show()
# %%
ts_ret = dsf.merge_time_series(spy_ret, spy_ret_reversed)

ts_ret.columns = ['spy_ret', 'reversed_spy_ret']

ts_ret
# %%