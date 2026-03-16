# Download data from International Agancy for Research on Cancer
# URL = https://gco.iarc.fr/today/en/dataviz/tables?mode=population

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import pandas as pd
from os.path import join

dir_repo = r'C:\Users\renald_e\Documents\02_Thesis\Cancer data'
dir_pics = join(dir_repo, 'pics')
dir_data = join(dir_repo, 'raw_data')

#%% Horizontal bar chart of incidence and mortality per cancer type
# Load data
fp_mort = join(dir_data, 'dataset-asr-mort-both-sexes-in-2022-world.json') # Age-standardized rate (ASR) per 100 000
fp_inc = join(dir_data, 'dataset-asr-inc-both-sexes-in-2022-world.json')

df = pd.read_json(fp_mort)
df.rename(columns={'asr': 'asr_mort'}, inplace=True)
df['asr_inc'] = pd.read_json(fp_inc)['asr']

# Drop values with ASR incidence < 0.5
df.drop(df.index[df['asr_inc']<2], inplace=True)

# Sort df based on ASR in decreasing order
df.sort_values('asr_inc', inplace=True, ignore_index=True)

#%% Plot bar chart

fig, ax = plt.subplots(figsize=(5,8))

# Draw balck thick, vertical line to split the plot
ax.vlines(0,-1,len(df['asr_inc']), colors='black', lw=1.25)

# Plot incidence
for x, y in zip(df['asr_inc'], df.index):
    ax.hlines(y, 0, -x, colors='#003049', lw=15)

# Plot mortality
for x, y in zip(df['asr_mort'], df.index):
    ax.hlines(y, 0, x, colors='#d62828', lw=15)

ax.set_ylim(-1,len(df['asr_inc']))

max_x = (int(df['asr_inc'].max() / 10) + 1) * 10
ax.set_xlim(-max_x, max_x)
# ax.set_xticks(np.arange(-max_x,max_x+10,10), labels=(str(abs(i)) for i in np.arange(-max_x,max_x+10,10)))
ax.xaxis.set_major_locator(mticker.MultipleLocator(10))
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: str(abs(int(x)))))

ax.set_xlabel('Age-Standardized Rate per 100 000 in 2022')

ax.set_yticks(df.index, labels=(str(l) for l in df['cancer_label']))

title_inc = ax.text(
    -max_x/2,
    df.index[-1]+1.5,
    s='Incidence',
    ha='center',
    weight='bold',
    fontsize='large')

title_mort = ax.text(
    max_x/2,
    df.index[-1]+1.5,
    s='Mortality',
    ha='center',
    weight='bold',
    fontsize='large')

ax.grid(visible=True,axis='x', alpha=0.7)

fig.savefig(
    join(dir_pics, 'ASR_cancer.png'),
    dpi=1000,
    bbox_inches='tight')

#%% Cancer over the years
# URL: https://gco.iarc.fr/overtime/en

fp_inc = join(dir_data, 'dataset-asr-inc-both-sexes-1943-2022-all-sites-excl-non-melanoma-skin-cancer.csv')
fp_mort = join(dir_data, 'dataset-asr-mort-both-sexes-1943-2022-all-sites-excl-non-melanoma-skin-cancer.csv')

df_inc = pd.read_csv(fp_inc)
df_mort = pd.read_csv(fp_mort)

countries = list(set([c if 'France' not in c else 'France' for c in df_inc['Country label']]))
data_inc = {}
data_mort = {}
for c in countries:
    data_inc[c] = {
        'years': df_inc['Year'][df_inc['Country label'] == c].to_numpy(),
        'asr': df_inc['ASR (World)'][df_inc['Country label'] == c].to_numpy(),
        }
    
    data_mort[c] = {
        'years': df_mort['Year'][df_mort['Country label'] == c].to_numpy(),
        'asr': df_mort['ASR (World)'][df_mort['Country label'] == c].to_numpy(),
        }


colors = plt.get_cmap('viridis', len(countries)).colors
fig, ax = plt.subplots(figsize=(10,5))

for c, col in zip(countries, colors):
    ax.plot(
        data_inc[c]['years'],
        data_inc[c]['asr'],
        color=col,
        lw=1.25,
        label=c)

for c, col in zip(countries, colors):
    ax.plot(
        data_mort[c]['years'],
        data_mort[c]['asr'],
        color=col,
        lw=1.25,
        ls='--')

ax.set_xlabel('Years')

ax.set_ylim(50, 350)
ax.set_ylabel('ASR')

ax.grid(True, alpha=0.5)

ax.legend(
    loc='upper left',
    bbox_to_anchor=(1.01,1.04),
    frameon=False,
    ncols=1)

title_inc = ax.text(
    1990,
    300,
    s='Incidence',
    ha='center',
    weight='bold',
    fontsize='large')

title_mort = ax.text(
    1993,
    80,
    s='Mortality',
    ha='center',
    weight='bold',
    fontsize='large')

ax.set_title(
    'Age-Standardized Rate (ASR) per 100 000',
    weight='bold',
    fontsize='x-large')

fig.savefig(
    join(dir_pics, 'ASR_years.png'),
    dpi=1000,
    bbox_inches='tight')