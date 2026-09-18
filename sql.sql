-- Active: 1768312369187@@127.0.0.1@5432@meteo
CREATE DATABASE meteo;

DROP DATABASE meteo;

CREATE Table if NOT EXISTS watheer_gold(
    city VARCHAR(50),
    date DATE,
    latitude FLOAT,
    longitude FLOAT,
    weather_code INT
    precipitation_sum FLOAT,
    precipitation_probability_max FLOAT,
    temperature_2m_max FLOAT,
    temperature_2m_min FLOAT,
    wind_speed_10_max FLOAT,
    wind_gusts_10m_max FLOAT,
    category_pluie VARCHAR(50),
    category_vent VARCHAR(50),
    category_temperature VARCHAR(50),
    risk_score INT,
    niveau_risk VARCHAR(50)
    PRIMARY KEY (city, date)
)