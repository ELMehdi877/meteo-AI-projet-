############################# Étape 2 — Nettoyage / Silver

import pandas as pd
import os
import json

# Définition de la racine du projet (un niveau au-dessus du dossier 'scripts')
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

extraction_bronze = os.path.join(BASE_DIR, "data", "extraction_bronze")
nettoyage_silver = os.path.join(BASE_DIR, "data", "nettoyage_silver")

# extraction_bronze = "data/extraction_bronze"
# nettoyage_silver = "data/nettoyage_silver"

all_cities_date = []

os.makedirs(nettoyage_silver, exist_ok= True)


for file in os.listdir(extraction_bronze):
    if file.endswith('.json'):
        file_path = os.path.join(extraction_bronze, file)
        city_name = file.replace("_raw.json", "").replace("_", " ").title()

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if "daily" in data:
            df_city = pd.DataFrame(data["daily"])
            df_city["city_name"] = city_name
            df_city["latitude"] = data.get("latitude")
            df_city["longitude"] = data.get("longitude")

            all_cities_date.append(df_city)
    

df_sealver = pd.concat(all_cities_date, ignore_index= True)

df_sealver['time'] = pd.to_datetime(df_sealver['time'])

df_sealver = df_sealver.rename(columns={'time' : 'date'})

df_sealver = df_sealver.drop_duplicates(subset=['city_name', 'date'])

cols = [
    'temperature_2m_max',
    'temperature_2m_min',
    'precipitation_sum',
    'precipitation_probability_max',
    'wind_speed_10m_max',
    'wind_gusts_10m_max',
    'weather_code',
    'latitude',
    'longitude'
    ]

for col in cols:
    df_sealver[col] = df_sealver[col].fillna(0.0)


df_sealver = df_sealver[df_sealver['temperature_2m_max'] >= df_sealver['temperature_2m_min']]

path_sealver = os.path.join(nettoyage_silver, "data_clear.csv")

df_sealver.to_csv(path_sealver, index= False)

print(f" Nettoyage terminé ! Données enregistrées dans {path_sealver}")
print(df_sealver.head())




print(df_sealver)