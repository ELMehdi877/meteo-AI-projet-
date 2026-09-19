############################# Étape 3 — Feature Engineering / Gold

import pandas as pd
import os
from sqlalchemy import create_engine, text

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

feature_engineering_gold = os.path.join(BASE_DIR, "data", "feature_engineering_gold")
nettoyage_selver = os.path.join(BASE_DIR, "data", "nettoyage_silver", "data_clear.csv")

# feature_engineering_gold = BASE_DIR + "data/feature_engineering_gold"
os.makedirs(feature_engineering_gold, exist_ok= True)

def category_vent(valeur):
    if valeur >= 60:
        return "Vent violent"

    elif valeur >= 30:
        return "Vent fort"
    
    elif valeur >= 15:
        return "moyen"

    else:
        return "faible"

def category_pluie(valeur):
    if valeur >= 20:
        return "forte"

    elif valeur >= 5:
        return "moderer"

    else:
        return "faible"

def category_temperature(temp_max,temp_min):
    if temp_max >= 40:
        return "Chaleur Extrême"

    elif temp_max >= 30:
        return "chaud"

    elif temp_min <=15:
        return "froid"

    elif temp_min <= 5:
        return "tree froid"

    else:
        return "agreable"

df = pd.read_csv(nettoyage_selver)

df["category_vent"] = df["wind_gusts_10m_max"].apply(category_vent)
df["category_pluie"] = df["precipitation_sum"].apply(category_pluie)
df["category_temperature"] = df.apply(lambda x: category_temperature(x["temperature_2m_max"], x["temperature_2m_min"]), axis=1)

####################### Weather Risk Score

def weather_risk_score(pluie, pluie_probable, vent, temp_max, temp_min):
    if pluie >= 25:
        pluie_point = 40

    elif pluie >= 15:
        pluie_point = 25

    elif pluie >= 5:
        pluie_point = 10

    else:
        pluie_point = 0

    risk_pluie = pluie_point * (pluie_probable/100)


    if vent >= 60:
        risk_vent = 35

    elif vent >= 35:
        risk_vent = 25

    elif vent >= 20:
        risk_vent = 15

    else :
        risk_vent = 0


    if temp_max >= 40 or temp_min <= 0:
        risk_temp = 25

    elif temp_max >= 30 or temp_min <= 5:
        risk_temp = 15

    elif temp_max >= 25:
        risk_temp = 5
        
    else: 
        risk_temp = 0

    risk_score = round(risk_pluie + risk_vent + risk_temp)
    return risk_score


df["risk_score"] = df.apply(
    lambda x: weather_risk_score(x["precipitation_sum"], x["precipitation_probability_max"], x["wind_gusts_10m_max"], x["temperature_2m_max"], x["temperature_2m_min"]), axis=1
) 

intervale = [-1, 25, 50, 100]

niveau = ["faible", "moyen", "elever"]

df["niveau_risk"] = pd.cut(df["risk_score"], bins= intervale, labels= niveau)
  
path_gold = os.path.join(feature_engineering_gold, "data_gold.csv")

df.to_csv(path_gold, index=False)

############################# Charger les données finales dans PostgreSQL

from db import get_engine

def recupere_gold_data():
    df = pd.read_csv(path_gold)

    df_cities = df[['city_name', 'latitude', 'longitude']].drop_duplicates()

    df_weather = df.copy()

    return df_cities, df_weather


df_cities, df_weather = recupere_gold_data()

def load_data(df_cities, df_weather):
    engine = get_engine()

    df_cities.to_sql(name='cities', con=engine, if_exists='append', index=False)

    db_cities = pd.read_sql("SELECT city_id, city_name FROM cities", con=engine)

    df_weather_ready = df_weather.merge(db_cities, on='city_name', how='inner')

    df_weather_ready = df_weather_ready.drop(columns=['city_name', 'weather_code', 'latitude', 'longitude'])

    df_weather_ready.to_sql(name='weather_previsions', con=engine, if_exists='append', index=False)

    print("Données insérées avec succès avec leurs clés étrangères !")


load_data(df_cities, df_weather)

