############################# connection avec la base de donner et la creation des tables

from sqlalchemy import create_engine, text

DATABASE_URL = "postgresql://postgres:password123@localhost:5433/meteo_db?client_encoding=utf8"

def get_engine() :
    return create_engine(DATABASE_URL)

# engine = create_engine(
#     "postgresql://postgres:password123@localhost:5433/meteo_db?client_encoding=utf8"
# )

create_tables_sql = """

DROP TABLE IF EXISTS watheer_previsions CASCADE; 
DROP TABLE IF EXISTS weather_previsions CASCADE;
DROP TABLE IF EXISTS cities CASCADE;

CREATE TABLE IF NOT EXISTS cities(
    city_id SERIAL PRIMARY KEY,
    city_name VARCHAR(100) UNIQUE NOT NULL,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL
);

CREATE Table if NOT EXISTS weather_previsions(
    prevision_id SERIAL PRIMARY KEY,
    city_id INT REFERENCES cities(city_id) ON DELETE CASCADE,
    date DATE,
    precipitation_sum FLOAT NOT NULL,
    precipitation_probability_max FLOAT NOT NULL,
    temperature_2m_max FLOAT NOT NULL,
    temperature_2m_min FLOAT NOT NULL,
    wind_speed_10m_max FLOAT NOT NULL,
    wind_gusts_10m_max FLOAT NOT NULL,
    category_pluie VARCHAR(50) NOT NULL,
    category_vent VARCHAR(50) NOT NULL,
    category_temperature VARCHAR(50) NOT NULL,
    risk_score INT NOT NULL,
    niveau_risk VARCHAR(50) NOT NULL,
    CONSTRAINT unique_city_date UNIQUE (city_id, date)
);
"""

engine = get_engine()

with engine.connect() as c :
    c.execute(text(create_tables_sql))
    c.commit()

print("Tables 'cities' et 'weather_previtions' créées avec succès")