from pprint import pprint
from ConvertTemperature import ConvertTemperature
import requests
from flask import *
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Define the database connection
DATABASE_URL = "sqlite:///weather.db"
engine = create_engine(DATABASE_URL, echo=True)

# Define the database model
Base = declarative_base()


class WeatherData(Base):
    __tablename__ = 'weather_data'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    dt_txt = Column(String)
    feels_like = Column(Float)
    wind_speed = Column(Float)
    humidity = Column(Integer)
    temp = Column(Float)
    temp_max = Column(Float)
    temp_min = Column(Float)
    weather_description = Column(String)
    weather_main = Column(String)



# Create tables
Base.metadata.create_all(bind=engine)
# Create a session
Session = sessionmaker(bind=engine)
session = Session()

class WeatherAPIProcessor:
    def weather_db_creation(self):
        locations = {
            "Lake District National Park": ("54.4609", "3.0886"),
            "Corfe Castle": ("50.6395", "2.0566"),
            "The Cotswolds": ("51.8330", "1.8433"),
            "Cambridge": ("52.2053", "0.1218"),
            "Bristol": ("51.4545", "2.5879"),
            "Oxford": ("51.7520", "1.2577"),
            "Norwich": ("52.6309", "1.2974"),
            "Stonehenge": ("51.1789", "1.8262"),
            "Watergate Bay": ("50.4429", "5.0553"),
            "Bay": ("50.6395", "2.0566"),
            "Birmingham": ("52.4862", "1.8904"),
        }

        api_read = open("apiKeys.txt", "r")
        open_weather_api_key = api_read.readline().strip('\n')
        tempcon = ConvertTemperature()

        for location, coordinates in locations.items():
            weather_url = ("https://api.openweathermap.org/data/2.5/forecast?lat=" +
                           coordinates[0] + "&lon=" + coordinates[1] + "&appid=" + open_weather_api_key)
            resp = requests.get(weather_url)
            for item in resp.json()['list']:
                check_name = resp.json()['city']['name']
                if check_name== "":
                    name = "Lake District National Park"
                elif check_name== "Lumbres":
                    name = "Corfes Castle"
                elif check_name== "Felixstowe":
                    name = "The Cotswolds"
                elif check_name== "Raversijde":
                    name = "Bristol"
                elif check_name== "Clacton-on-Sea":
                    name = "Oxford"
                elif check_name == "Calais":
                    name = "Stonehenge"
                elif check_name == "Les Tombes":
                    name = "Watergate Bay"
                elif check_name == "Lumbres":
                    name = "Bay"
                elif check_name == "Lowestoft":
                    name = "Birmingham"
                else:
                    name = resp.json()['city']['name']
                weather_data = WeatherData(
                    name=name,
                    dt_txt=item['dt_txt'],
                    feels_like=tempcon.convert_kelvin_to_celsius(item['main']['feels_like']),
                    temp= tempcon.convert_kelvin_to_celsius(item['main']['temp']),
                    temp_max = tempcon.convert_kelvin_to_celsius(item['main']['temp_max']),
                    temp_min = tempcon.convert_kelvin_to_celsius(item['main']['temp_min']),
                    humidity=item['main']['humidity'],
                    wind_speed=item['wind']['speed'],
                    weather_description=item['weather'][0]['description'],
                    weather_main = item['weather'][0]['main'],
                )
                session.add(weather_data)

        session.commit()
        session.close()
