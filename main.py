import pandas as pd
import requests
import os
import json

extraction_bronze = "data/extraction_bronze"

# os.makedirs(extraction_bronze, exist_ok= True)

# df_city = pd.read_csv("data/ma.csv")

# url = "https://api.open-meteo.com/v1/forecast"

# daily_params = ["temperature_2m_max",
#                 "temperature_2m_min",
#                 "precipitation_sum",
#                 "precipitation_probability_max",
#                 "wind_speed_10m_max",
#                 "wind_gusts_10m_max",
#                 "weather_code"
#                 ]


# for index, row in df_city.iterrows():
#     city_name = row["city"]
#     lat = row["lat"]
#     lng = row["lng"]

#     print(f"Récupération des données pour : {city_name}...")

#     params = {
#         'latitude' : lat,
#         'longitude' : lng,
#         'daily' : daily_params,
#         'timezone': 'auto'
#     }

#     try:
#         reponse = requests.get(url, params=params, timeout= 10)

#         reponse.raise_for_status()

#         data = reponse.json()

#         file = f"{extraction_bronze}/{city_name.lower().replace(' ', '_')}_raw.json"

#         with open(file, "w", encoding='utf-8') as f:
#            json.dump(data, f) 

#         print(f"data est sauvegarder dans {city_name}")

#     except requests.exceptions.RequestException as e:
#         print(f"error lors de l'appel de API pour {city_name} : {e}")


# path = "C:/Users/safiy/Desktop/2eme annee Youcode/Brief/Construction d'un pipeline de données de bout en bout pour l'aide à la décision/projet/data/extraction_bronze"

nettoyage_silver = "data/nettoyage_silver"

all_cities_date = []

os.makedirs(nettoyage_silver, exist_ok= True)


for file in os.listdir(extraction_bronze):
    if file.endswith('.json'):
        file_path = os.path.join(extraction_bronze, file)
        city_name = file.replace("_raw.json", "").replace("_", " ").title()

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if "daily" in data:
            df = pd.DataFrame(data["daily"])
            df["city"] = city_name
            df["latitude"] = data.get("latitude")
            df["longitude"] = data.get("longitude")

            all_cities_date.append(df)
    

df_sealver = pd.concat(all_cities_date, ignore_index= True)

df_sealver['time'] = pd.to_datetime(df_sealver['time'])

df_sealver = df_sealver.rename(columns={'time' : 'date'})

df_sealver = df_sealver.drop_duplicates(subset=['city', 'date'])

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

# p = os.listdir(path)

# for x in p :
#     with open(path + '/' + x, "r", encoding="utf-8") as file:
#         data = json.load(file)

#     df = pd.DataFrame(data)

# print(df)