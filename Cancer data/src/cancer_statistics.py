# Download data from International Agancy for Research on Cancer
# URL = https://gco.iarc.fr/today/en/dataviz/tables?mode=population

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
import folium

def get_data(display, measures):
    
    if display == 'populations' and measures == 'mortality':
        filename = 'dataset-mort-both-sexes-in-2022-all-cancers.json'
        
    elif display == 'cancers' and measures == 'mortality':
        filename = 'dataset-mort-both-sexes-in-2022-continents.json'
        
    elif display == 'populations' and measures == 'incidence':
        filename = 'dataset-inc-both-sexes-in-2022-all-cancers.json'
        
    elif display == 'cancers'and measures == 'incidence':
        filename = 'dataset-inc-both-sexes-in-2022-continents.json'
    
    
    return pd.read_json(filename)

measure = 'mortality'

df = get_data('populations', 'mortality').iloc[:-1] # remove the totals
df['total'] = df['total'].str.replace('\xa0', '', regex=False).astype(int)

#%% Visualize the world map

# Get countries boundaries 
political_countries_url = (
    "http://geojson.xyz/naturalearth-3.3.0/ne_50m_admin_0_countries.geojson"
)

m = folium.Map(
    location=(30, 10),
    zoom_start=2,
    tiles="Cartodb Positron")

# folium.GeoJson(political_countries_url).add_to(m)

folium.Choropleth(
    geo_data=political_countries_url,
    data=df,
    columns=("country_iso3", "crude_rate"),
    key_on="feature.properties.iso_a3",
    bins=np.linspace(0, (int(df['crude_rate'].max()/10)+1)*10, 10),
    fill_color="RdYlGn_r",
    fill_opacity=0.8,
    line_opacity=0.3,
    nan_fill_color="white",
    legend_name="Cancer " + f"{measure} rate"
    ).add_to(m)

m.save("cancer.html")

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

options = Options()
options.add_argument("--headless")
options.add_argument("--window-size=4000,3000")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

driver.get("file:///absolute/path/to/cancer.html")
time.sleep(2)

driver.save_screenshot("cancer_map_screenshot.png")
driver.quit()
