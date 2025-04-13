# %%
import pandas as pd

import ds4finance as dsf

# %%
data = pd.read_excel("/home/ubuntu/AWSParis/artigos/ipynb/longTermCorrelations/long_term_returns_data.xlsx", skiprows=10)

# Create a new dataframe with only 'US Equity'
data = data[['US Equity']]

data

# %%
data_growth = dsf.compute_time_series(data)

# %% [markdown]
# Esta semana quis testar o que acontecia a quem fez DCA começando no pico de Agosto 1929. Para os não iniciados tenho alguns termos que vou usar na análise:
# 
# Retorno Total: Performance que conta com dividendos reinvestidos, como um ETF ACC
# Time Weighted Return: O que "normalmente" vemos como a performance do investimento. Se o ETF foi de 100 euros para 200 euros o Time Weighted Return é de 100%
# Money Weighted Return: Performance que tem em consideração os investimentos. Como vamos ver abaixo mesmo quando o Time Weighted Return é 0% o Money Weighted Return pode ser positivo (ou negativo) se no fim do período analisado há uma forte subida (forte queda).

# %% [markdown]
# Em baixo podem ver a performance do mercado accionista large Cap dos EUA na grande depressão. É usado o Retorno Total (o que quer dizer que a performance tem em consideração os dividendos, reinvestindo-os, como se fosse um ETF ACC).
# 
# Tendo em consideração o retorno total demorou cerca de 15 anos a atingir novo máximo depois de Agosto de 2029, com uma queda maior que 80%.
# 
# O Time Weighted Return foi de cerca de 0% durante este período.

# %%
dsf.ichart(data_growth['1926-01-01':'1945-01-01'],
            title='Performance Large Cap Equity EUA <br> entre Jan 1926 e Jan 1945',
            yticksuffix="€",
            yTitle='Performance dos investimentos',
            image='fp'
            )

# %%
# Filter the data
investment_df = data_growth[(data_growth.index >= '1929-08-01') & (data_growth.index <= '1945-01-01')].copy()

# Investment amounts
initial_investment_amount = 100
monthly_investment_amount = 100

# Returns
investment_df['ret'] = investment_df['US Equity'].pct_change()
investment_df.fillna({'ret': 0.0}, inplace=True)

# Columns for tracking
investment_df['Monthly_Money_Invested'] = monthly_investment_amount
investment_df['Monthly_Gain'] = 0.0
investment_df['Investments'] = 0.0

# Total money invested
investment_df['Money_Invested_Total'] = investment_df['Monthly_Money_Invested'].cumsum()
investment_df['Money_Invested_Total'] += (initial_investment_amount - monthly_investment_amount)
first_date_index = investment_df.index[0]
investment_df.loc[first_date_index, 'Money_Invested_Total'] = initial_investment_amount
investment_df.loc[first_date_index, 'Monthly_Money_Invested'] = 0

# First row setup
investment_df.loc[first_date_index, 'Investments'] = initial_investment_amount
investment_df.loc[first_date_index, 'Monthly_Gain'] = 0.0

# Simulation
for i in range(1, len(investment_df)):
    current_index = investment_df.index[i]
    previous_index = investment_df.index[i-1]
    
    prev_value = investment_df.loc[previous_index, 'Investments']
    ret = investment_df.loc[current_index, 'ret']
    
    gain = prev_value * ret
    investment_df.loc[current_index, 'Monthly_Gain'] = gain

    investment_df.loc[current_index, 'Investments'] = prev_value * (1 + ret) + monthly_investment_amount

# %% [markdown]
# O que aconteceu se tivessemos começado a investir mesmo no pico MAS tivessemos continuado a investir? Fiz a simulação de um DCA de 100 dólares começando com os primeiros 100 dólares em Agosto de 1929, mesmo no pico.
# 
# O gráfico começa portanto em Agosto de 1929 e acaba na mesma em Jan de 1945. 
# 
# O montante investido durante o período foi de 18.6 mil dólares e o valor dos investimentos de 35.9 mil dólares para um Money Weighted Return de 4.6%.

# %%
investment_df.rename(columns={"Investments": "Investimentos", "Money_Invested_Total": "Depósitos"}, inplace=True)

dsf.ichart(investment_df[['Depósitos', 'Investimentos']],
            title='Performance investimentos <br> entre Aug 1929 e Jan 1945',
            yticksuffix="€",
            yTitle='Performance dos investimentos',
            image='fp')

fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5))

# %% [markdown]
# Como se pode ver em cerca de 4 anos recuperamos o dinheiro, embora só em 1942 o portfolio tiveese de facto começado a render acima do montante dos reforços (12/13 anos depois de começarmos a investir).

# %%
# Filter the data
investment_df = data_growth[(data_growth.index >= '1929-08-01') & (data_growth.index <= '1945-01-01')].copy()

# Investment amounts
initial_investment_amount = 10000
monthly_investment_amount = 100

# Returns
investment_df['ret'] = investment_df['US Equity'].pct_change()
investment_df.fillna({'ret': 0.0}, inplace=True)

# Columns for tracking
investment_df['Monthly_Money_Invested'] = monthly_investment_amount
investment_df['Monthly_Gain'] = 0.0
investment_df['Investments'] = 0.0

# Total money invested
investment_df['Money_Invested_Total'] = investment_df['Monthly_Money_Invested'].cumsum()
investment_df['Money_Invested_Total'] += (initial_investment_amount - monthly_investment_amount)
first_date_index = investment_df.index[0]
investment_df.loc[first_date_index, 'Money_Invested_Total'] = initial_investment_amount
investment_df.loc[first_date_index, 'Monthly_Money_Invested'] = 0

# First row setup
investment_df.loc[first_date_index, 'Investments'] = initial_investment_amount
investment_df.loc[first_date_index, 'Monthly_Gain'] = 0.0

# Simulation
for i in range(1, len(investment_df)):
    current_index = investment_df.index[i]
    previous_index = investment_df.index[i-1]
    
    prev_value = investment_df.loc[previous_index, 'Investments']
    ret = investment_df.loc[current_index, 'ret']
    
    gain = prev_value * ret
    investment_df.loc[current_index, 'Monthly_Gain'] = gain

    investment_df.loc[current_index, 'Investments'] = prev_value * (1 + ret) + monthly_investment_amount

# %% [markdown]
# Fiz o teste também para um investimento inicial de 10 mil dólares e reforços mensais de 100 dólares (porque muita gente começa com um pequeno lump sum antes de iniciar o DCA). Como esperado o facto de termos começado com um montante mais elevado fez com que em termos de rentabilidade não tenhamos conseguido tanto, uma vez que a primeira tranche de 10 mil dólares não teve rentabilidade (lembrem-se que o Time Weighted Retun foi de 0%).
# 
# No final tinhamos 45.800 mil dólares vs um investimento de 28.500 (reparem que até o que se ganhou foram os mesmos 17.300 USD, apenas do DCA de 100 dólares mensais). O Time weighted return foi de 3.1% neste caso, sendo mais baixo quanto maior tivesse sido o investimento inicial.
# 
# Atenção, o DCA "ganhou" numa situação de crise. A maioria das vezes não ganha e investirmos como se viesse aí outra Grande Depressão provavelmente não é o ideal, mas estas simulações mostram a forma do DCA.

# %%
investment_df.rename(columns={"Investments": "Investimentos", "Money_Invested_Total": "Depósitos"}, inplace=True)

fig = dsf.ichart(investment_df[['Depósitos', 'Investimentos']],
                 title='Performance investimentos <br> entre Aug 1929 e Jan 1945',
                 yticksuffix="€",
                 yTitle='Performance dos investimentos',
                 image='fp')

fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5))

# %%



