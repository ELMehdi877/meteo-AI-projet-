############################# Étape 1 — Extraction / Bronze

import pandas as pd
import requests
import os
import json

extraction_bronze = "data/extraction_bronze"

os.makedirs(extraction_bronze, exist_ok= True)

df_city = pd.read_csv("data/ma.csv")

url = "https://api.open-meteo.com/v1/forecast"

daily_params = ["temperature_2m_max",
                "temperature_2m_min",
                "precipitation_sum",
                "precipitation_probability_max",
                "wind_speed_10m_max",
                "wind_gusts_10m_max",
                "weather_code"
                ]


for index, row in df_city.iterrows():
    city_name = row["city"]
    lat = row["lat"]
    lng = row["lng"]

    print(f"Récupération des données pour : {city_name}...")

    params = {
        'latitude' : lat,
        'longitude' : lng,
        'daily' : daily_params,
        'timezone': 'auto',
        "forecast_days" : 3
    }

    try:
        reponse = requests.get(url, params=params, timeout= 10)

        reponse.raise_for_status()

        data = reponse.json()

        file = f"{extraction_bronze}/{city_name.lower().replace(' ', '_')}_raw.json"

        with open(file, "w", encoding='utf-8') as f:
           json.dump(data, f, indent=2) 

        print(f"data est sauvegarder dans {city_name}")

    except requests.exceptions.RequestException as e:
        print(f"error lors de l'appel de API pour {city_name} : {e}")



