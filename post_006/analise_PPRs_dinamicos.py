# %%
import pandas as pd
import ds4finance as dsf

# Define the URL for the Excel file
url = "https://goldensgf.pt/wp-content/uploads/2024/08/HISTORICO-DE-COTACOES.xlsx"

data_fim = '2024-10-29'

# Read the Excel file into a pandas DataFrame
sgf_data = pd.read_excel(url)

# %%
# keep only useful columns
sgf_data = sgf_data[['Nome do Fundo', 'Cotação', 'Data']]

###################################################
###################### Stoik ######################
###################################################
# %%
# Filter the DataFrame where "Nome do Fundo" is 'XXXXXXXXX'
SGF_STOIK = sgf_data[sgf_data['Nome do Fundo'] == 'SGF Reforma Stoik']

# Rename the columns
SGF_STOIK = SGF_STOIK.rename(columns={'Data': 'Date', 'Cotação': 'SGF_STOIK'})

# Convert the "Date" column to a datetime type
SGF_STOIK['Date'] = pd.to_datetime(SGF_STOIK['Date'], errors='coerce')

# Set the "Date" column as the index
SGF_STOIK = SGF_STOIK.set_index('Date').sort_index()

# Drop "Nome do fundo" column
SGF_STOIK = SGF_STOIK.drop('Nome do Fundo', axis=1)

# Display the updated DataFrame
SGF_STOIK

##############################################################
###################### SGF Dr Finanças  ######################
##############################################################
# %%
# Filter the DataFrame where "Nome do Fundo" is 'XXXXXXXXX'
SGF_FIN = sgf_data[sgf_data['Nome do Fundo'] == 'SGF DR FINANÇAS']

# Rename the columns
SGF_FIN = SGF_FIN.rename(columns={'Data': 'Date', 'Cotação': 'SGF_FIN'})

# Convert the "Date" column to a datetime type
SGF_FIN['Date'] = pd.to_datetime(SGF_FIN['Date'], errors='coerce')

# Set the "Date" column as the index
SGF_FIN = SGF_FIN.set_index('Date').sort_index()

# Drop "Nome do fundo" column
SGF_FIN = SGF_FIN.drop('Nome do Fundo', axis=1)

# Display the updated DataFrame
SGF_FIN

#####################################################
###################### SGF ETF ######################
#####################################################
# %%
# Filter the DataFrame where "Nome do Fundo" is 'XXXXXXXXX'
SGF_ETF = sgf_data[sgf_data['Nome do Fundo'] == 'Golden SGF ETF A']

# Rename the columns
SGF_ETF = SGF_ETF.rename(columns={'Data': 'Date', 'Cotação': 'SGF_ETF'})

# Convert the "Date" column to a datetime type
SGF_ETF['Date'] = pd.to_datetime(SGF_ETF['Date'], errors='coerce')

# Set the "Date" column as the index
SGF_ETF = SGF_ETF.set_index('Date').sort_index()

# Drop "Nome do fundo" column
SGF_ETF = SGF_ETF.drop('Nome do Fundo', axis=1)

# Display the updated DataFrame
SGF_ETF

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
optimize = process_investing_fund_data('0P0000UP12', 'Opt. Activo')
optimize

# %%
smart_din = process_investing_fund_data('0P0001LHA7', 'Smart Din.')
smart_din

# %%
import yfinance as yf

# Download historical data for V80A.AS
V80A = yf.download('V80A.AS', end=data_fim)[['Adj Close']]

V80A = V80A.rename(columns={'Adj Close': 'V80A'})

# Display the data
V80A

# %%

# Download historical data for V80A.AS
V60A = yf.download('V60A.AS', end=data_fim)[['Adj Close']]

V60A = V60A.rename(columns={'Adj Close': 'V60A'})

# Display the data
V60A

# %%
data = dsf.merge_time_series(SGF_STOIK, optimize).ffill().dropna()
data = dsf.merge_time_series(data, V80A).ffill().dropna()
data = dsf.merge_time_series(data, V60A).ffill().dropna()
data = dsf.merge_time_series(data, smart_din).ffill().dropna()

data = data[:data_fim]

data = dsf.compute_growth_index(data)

data

# %%
data = data[data.iloc[-1].sort_values(ascending=False).index]

data

# %%
start = data.index[0].strftime('%Y-%m-%d')
end = data.index[-1].strftime('%Y-%m-%d')

dsf.ichart(data, title=f"Comparação entre PPRs e Vanguards lifestrategy <br> entre {start} e {end}",
 yTitle='Valorização por cada 100 €uros investidos', yticksuffix='€', image='fp')

# %%
dsf.compute_performance_table(data)

# %%
data = dsf.merge_time_series(data, SGF_FIN).dropna()

data = data['2023-10-31':]
data = dsf.compute_growth_index(data)

data = data[data.iloc[-1].sort_values(ascending=False).index]

data

# %%
start = data.index[0].strftime('%Y-%m-%d')
end = data.index[-1].strftime('%Y-%m-%d')

dsf.ichart(data, title=f"Comparação entre PPRs e Vanguards lifestrategy <br> entre {start} e {end}",
 yTitle='Valorização por cada 100 €uros investidos', yticksuffix='€', image='fp')

# %%
dsf.compute_performance_table(data)

# %%
data = dsf.merge_time_series(data, SGF_ETF).dropna()

data = data['2024-03-31':]
data = dsf.compute_growth_index(data)

data = data[data.iloc[-1].sort_values(ascending=False).index]

data

# %%
start = data.index[0].strftime('%Y-%m-%d')
end = data.index[-1].strftime('%Y-%m-%d')

dsf.ichart(data, title=f"Comparação entre PPRs e Vanguards lifestrategy <br> entre {start} e {end}",
 yTitle='Valorização por cada 100 €uros investidos', yticksuffix='€', image='fp')

# %%
dsf.compute_performance_table(data)

# %%
### Anexos

data = dsf.merge_time_series(SGF_STOIK, optimize)
data = dsf.merge_time_series(data, V80A)
data = dsf.merge_time_series(data, V60A)
data = dsf.merge_time_series(data, smart_din)
data = dsf.merge_time_series(data, SGF_FIN)

data = data.dropna()

data = dsf.compute_growth_index(data)
data = data[data.iloc[-1].sort_values(ascending=False).index]

data

# %%
dsf.ichart(data, title=f"O mau arranque do SGF Dr. Finanças",
 yTitle='Valorização por cada 100 €uros investidos', yticksuffix='€', image='fp')
# %%

data = dsf.merge_time_series(SGF_STOIK, optimize)
data = dsf.merge_time_series(data, V80A)
data = dsf.merge_time_series(data, V60A)
data = dsf.merge_time_series(data, smart_din)
data = dsf.merge_time_series(data, SGF_FIN)
data = dsf.merge_time_series(data, SGF_ETF)

data = data.dropna()

data = data[data.iloc[-1].sort_values(ascending=False).index]

data = dsf.compute_growth_index(data)

data
# %%
dsf.ichart(data, title=f"O mau arranque do SGF ETF PPR",
 yTitle='Valorização por cada 100 €uros investidos', yticksuffix='€', image='fp')
# %%
