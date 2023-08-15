import pandas as pd
from plotly import express as px

path = r'C:\OneDrive\GDrive\Python\Парсер\HH.ru\combined_data.xlsx'
df = pd.read_excel(path)
df_filtered = df.dropna(subset=['(address)_lat', '(address)_lng'])
fig = px.scatter_mapbox(df_filtered, lat = '(address)_lat', lon = '(address)_lng')
fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()


