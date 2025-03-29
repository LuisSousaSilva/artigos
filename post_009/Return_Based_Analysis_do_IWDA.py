# %%
import matplotlib.pyplot as plt
import statsmodels.api as sm
import ds4finance as dsf
import seaborn as sns
import yfinance as yf
import pandas as pd

plt.style.use('seaborn-v0_8')  # Apply the seaborn-v0_8 style

# %%
quotes = pd.DataFrame()

tickers = ['IWDA.AS', 'IS3R.DE', 'IS3Q.DE', 'IS3S.DE', 'IQQ0.DE', 'IS3T.DE']

for ticker in tickers:
    etf = yf.Ticker(ticker).history(start='2015-12-30', auto_adjust=False)[['Adj Close']]
    etf.columns = [ticker]  # Rename the column to the desired name
    quotes = dsf.merge_time_series(quotes, etf).ffill().dropna()

quotes.index = quotes.index.tz_localize(None)  # Remove timezone awareness

ETFs = quotes.copy()

# %%
ETFs.columns = ['IWDA', 'Momentum', 'Quality', 'Value', 'Volatility', 'Size']

ETFs = dsf.compute_growth_index(ETFs)

ETFs.index = ETFs.index.normalize()

ETFs

# %%
legend_index = ETFs.iloc[-1].sort_values(ascending=False).index
ETFs = ETFs[legend_index]

ETFs = ETFs.drop(pd.to_datetime("2017-06-04"))

# %%
start = ETFs.index[0].strftime('%Y-%m-%d')
end = ETFs.index[-1].strftime('%Y-%m-%d')

fig = dsf.ichart(round(ETFs, 2), title=f'Performance entre {start} e {end}',
          yticksuffix= '€', yTitle='Valorização por cada 100 €uros investidos',
          image='fp')

fig.show()

# %%
dsf.compute_performance_table(ETFs)

# %%
returns_M = ETFs.resample('M').last().pct_change().dropna() * 100

ax = sns.pairplot(
    returns_M, 
    corner=True, 
    kind="reg", 
    plot_kws={'line_kws': {'color': 'indigo'}}, 
    height=1.5  # Adjust the height to make the plot smaller
)
ax;

# %%
returns_M_corr = round(returns_M.corr(), 3)

# %%
plt.figure(figsize=(8, 6))  # Adjust the size as needed
sns.heatmap(
    returns_M_corr,
    annot=True,          # Display the correlation values
    cmap="coolwarm",     # Use a diverging color map
    fmt=".2f",           # Format the annotation to 3 decimal places
    linewidths=0.5,      # Add space between cells
    cbar_kws={'shrink': 0.8},  # Shrink the color bar slightly
    vmin=0,             # Minimum value for colormap
    vmax=1               # Maximum value for colormap
)

# Set transparent background
plt.gcf().patch.set_alpha(0)  # Transparent figure background
plt.gca().patch.set_alpha(0)  # Transparent axes background

plt.title("Correlation Heatmap")
plt.show()

# %%
# Find pairs with correlations less than 0.7
low_corr_pairs = returns_M_corr.where(returns_M_corr < 0.7).stack()

low_corr_pairs = low_corr_pairs.sort_values()

low_corr_pairs

# %%
# Helper functions
def regress(dependent_variable, explanatory_variables, alpha=True):
    """
    Runs a linear regression to decompose the dependent variable into the explanatory variables
    returns an object of type statsmodel's RegressionResults on which you can call
       .summary() to print a full summary
       .params for the coefficients
       .tvalues and .pvalues for the significance levels
       .rsquared_adj and .rsquared for quality of fit
    """
    if alpha:
        explanatory_variables = explanatory_variables.copy()
        explanatory_variables["Alpha"] = 1
    
    lm = sm.OLS(dependent_variable, explanatory_variables).fit()
    return lm.params

def compute_rsa(quotes, normalized_results=False):
    '''
    quotes is a dataframe of quotes where the first column is
    the dependent variable
    '''
    dependent_variable = quotes.iloc[:, 0].pct_change().dropna()
    independent_variables = quotes.iloc[:, 1:].pct_change().dropna()

    values = regress(dependent_variable=dependent_variable,
                    explanatory_variables=independent_variables,
                    alpha=False)
    
    if normalized_results==True:
        values = values / values.sum()
    
    return values

# %%
ETFs = ETFs[['IWDA', 'Momentum', 'Quality', 'Value', 'Size', 'Volatility']]
ETFs

# %%
df = pd.DataFrame(round(compute_rsa(ETFs, normalized_results=True), 3))

df.columns = ['% weight']

df * 100

# %%
ETFs = ETFs.drop(columns=['Volatility'])

df = pd.DataFrame(round(compute_rsa(ETFs, normalized_results=True), 3))

df.columns = ['% weight']

df * 100

# %%
weights = [0] + list(df['% weight'])

portfolio = dsf.compute_portfolio(quotes=ETFs, weights=weights)

IWDA = ETFs[['IWDA']]

IWDA_and_factors_p = dsf.compute_growth_index(dsf.merge_time_series(portfolio, IWDA, 'inner'))

IWDA_and_factors_p.columns=['Factors P', 'IWDA']

dsf.ichart(IWDA_and_factors_p, title='IWDA vs Portfolio de Factores', image='fp')

# %%
dsf.compute_performance_table(IWDA_and_factors_p)

# %%
# Define a function for one-year rolling weights
def compute_rolling_weights(data, window_size=252, normalized=True):
    """
    Compute rolling weights over a specified window size.
    :param data: DataFrame of ETFs quotes.
    :param window_size: Rolling window size (default: 252 trading days ~ 1 year).
    :param normalized: Whether to normalize the weights (default: True).
    :return: DataFrame of rolling weights for each factor.
    """
    rolling_weights = pd.DataFrame(index=data.index, columns=data.columns[1:])

    for end_date in range(window_size, len(data)):
        rolling_window = data.iloc[end_date - window_size:end_date]
        rolling_weights.iloc[end_date] = compute_rsa(rolling_window, normalized_results=normalized)

    return rolling_weights

# Apply the function to compute rolling weights
rolling_weights = compute_rolling_weights(ETFs, window_size=252)

# Drop NaN values caused by the initial rolling window
rolling_weights = rolling_weights.dropna()

# Inspect the resulting DataFrame
rolling_weights

# %%
rolling_weights_new = rolling_weights['2019':]

# rolling_weights_new = rolling_weights_new[['Quality', 'Momentum', 'Value', 'Size']]

# %%
rolling_weights_new

# %%
dsf.ichart(round(rolling_weights_new, 2))

# %%
import plotly.express as px

fig = px.area(
    rolling_weights_new,
    x=rolling_weights_new.index,   # Use the DataFrame index for the x-axis
    y=rolling_weights_new.columns, # Use all columns for the y-axis (they will be stacked)
    title="Factor Weights Over Time",
    labels={"value": "Weight Proportion", "variable": "Factor", "Date": "Date"}, # Customize axis/legend labels
)

fig.update_layout(
    yaxis_tickformat=".1%",
    width=900,
    height=500
)

# --- Show the Plot ---
fig.show()

# %%



