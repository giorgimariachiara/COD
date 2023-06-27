from geopy.geocoders import Nominatim
import folium
import pandas as pd
from geopy.exc import GeocoderTimedOut
from functools import lru_cache

# Carica i dati dal file CSV
data = pd.read_csv('MAmapcount.csv')

# Crea una mappa di base centrata sull'Italia utilizzando Folium
italy_map = folium.Map(location=[41.8719, 12.5674], zoom_start=6)

# Funzione per ottenere le coordinate della regione utilizzando Geocoder
@lru_cache(maxsize=100)
def get_coordinates(region):
    geolocator = Nominatim(user_agent='mariachiara.giorgi1@gmail.com')
    try:
        location = geolocator.geocode(region + ', Italy')
        if location is not None:
            return location.latitude, location.longitude
    except GeocoderTimedOut:
        return get_coordinates(region)

    return None

# Itera sui dati del DataFrame e crea layer per le regioni sulla mappa
for index, row in data.iterrows():
    region = row['regione']
    count = row['count']
    coordinates = get_coordinates(region)

    if coordinates:
        folium.CircleMarker(
            location=coordinates,
            radius=count/1000,
            color='blue',
            fill=True,
            fill_color='blue',
            fill_opacity=0.6,
            popup=f"{region}: {count}",
        ).add_to(italy_map)

# Aggiungi il layer Choropleth alla mappa utilizzando il file GeoJSON delle regioni italiane
folium.Choropleth(
    geo_data='italy_regions.geojson',  # Inserisci il percorso al file GeoJSON delle regioni italiane
    name='choropleth',
    data=data,
    columns=['regione', 'count'],
    key_on='feature.properties.name',
    fill_color='YlOrRd',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Count'
).add_to(italy_map)

# Visualizza la mappa
italy_map.save('mappa.html')
