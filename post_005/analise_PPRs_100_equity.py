# %%
import pandas as pd
import ds4finance as dsf

# Define the URL for the Excel file
url = "https://goldensgf.pt/wp-content/uploads/2024/08/HISTORICO-DE-COTACOES.xlsx"

data_fim = '2024-10-30'

# Read the Excel file into a pandas DataFrame
sgf_data = pd.read_excel(url)

# %%
# keep only useful columns
sgf_data = sgf_data[['Nome do Fundo', 'Cotação', 'Data']]

# %%
# Filter the DataFrame where "Nome do Fundo" is 'Golden SGF TOP GESTORES'
SGF_TOP = sgf_data[sgf_data['Nome do Fundo'] == 'Golden SGF TOP GESTORES']

# Rename the columns
SGF_TOP = SGF_TOP.rename(columns={'Data': 'Date', 'Cotação': 'SGF_TOP'})

# Convert the "Date" column to a datetime type
SGF_TOP['Date'] = pd.to_datetime(SGF_TOP['Date'], errors='coerce')

# Set the "Date" column as the index
SGF_TOP = SGF_TOP.set_index('Date').sort_index()

# Drop "Nome do fundo" column
SGF_TOP = SGF_TOP.drop('Nome do Fundo', axis=1)

# Display the updated DataFrame
SGF_TOP

# %%
def process_investing_fund_data(file_code, fund_name):
    # Construct the file name from the input file code
    file_name = f'{file_code} Historical Data.csv'
    
    # Load the CSV file
    df = pd.read_csv(file_name)
    
    # Rename the columns
    df = df.rename(columns={'Date': 'Date', 'Price': fund_name})
    
    # Convert the "Date" column to datetime format
    df['Date'] = pd.to_datetime(df['Date'], format='%b %d, %Y', errors='coerce')
    
    # Set "Date" as the index
    df = df.set_index('Date')
    
    # Keep only the renamed price column
    df = df[[fund_name]]
    
    # Return the cleaned DataFrame
    return df

# %%
optimize = process_investing_fund_data('0P0001FEUD', 'Opt. Agr.')
optimize

# %%
SG = process_investing_fund_data('0P0001LAO7', 'Casa S&G')
SG

# %%
ITG = process_investing_fund_data('0P0001PBB6', 'Inv. TG')
ITG

# %%
BPI = process_investing_fund_data('0P0001ITBQ', 'BPI')
BPI

# %%
import yfinance as yf

# Download historical data for IWDA.AS
IWDA = yf.download('IWDA.AS', end=data_fim)[['Adj Close']]

IWDA = IWDA.rename(columns={'Adj Close': 'IWDA'})

# Display the data
IWDA

# %%
data = dsf.merge_time_series(IWDA, optimize).ffill().dropna()

data = dsf.compute_growth_index(data)

data

# %%
start = data.index[0].strftime('%Y-%m-%d')
end = data.index[-1].strftime('%Y-%m-%d')

dsf.ichart(data, title=f"Comparação entre PPRs e IWDA entre {start} e {end}",
 yTitle='Valorização por cada 100 €uros investidos', yticksuffix='€')

# %%
dsf.compute_performance_table(data)

# %%
data = dsf.merge_time_series(data, SG).ffill().dropna()
data = dsf.merge_time_series(data, SGF_TOP).ffill().dropna()

data = data["2020-12-30":]

data = dsf.compute_growth_index(data)

data

# %%
start = data.index[0].strftime('%Y-%m-%d')
end = data.index[-1].strftime('%Y-%m-%d')

dsf.ichart(data, title=f"Comparação entre PPRs e IWDA entre {start} e {end}",
 yTitle='Valorização por cada 100 €uros investidos', yticksuffix='€')

# %%
dsf.compute_performance_table(data)

# %%
data = dsf.merge_time_series(data, ITG).ffill().dropna()
# data = dsf.merge_time_series(data, BPI).ffill().dropna()

data = dsf.compute_growth_index(data)

data

# %%
start = data.index[0].strftime('%Y-%m-%d')
end = data.index[-1].strftime('%Y-%m-%d')

dsf.ichart(data, title=f"Comparação entre PPRs e IWDA entre {start} e {end}",
 yTitle='Valorização por cada 100 €uros investidos', yticksuffix='€')

# %%
dsf.compute_performance_table(data)
# %%
