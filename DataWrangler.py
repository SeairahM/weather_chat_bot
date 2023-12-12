import json
from flask_sqlalchemy import SQLAlchemy
import sqlite3
from flask import *

app = Flask(__name__)
import ssl

db_name = "weather.db"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


class Weather(db.Model):
    __tablename__ = 'weather_data'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.VARCHAR)
    date = db.Column(db.VARCHAR)
    feels_like = db.Column(db.Float)
    wind_speed = db.Column(db.VARCHAR)
    humidity = db.Column(db.REAL)
    temp = db.Column(db.Float)
    maximum_temp = db.Column(db.Float)
    minimum_temp = db.Column(db.Float)
    weather_desc = db.Column(db.VARCHAR)
    weather_main = db.Column(db.VARCHAR)


class DataWrangler:
    def bot_training_data(self):
        sqliteConnection = sqlite3.connect('weather.db')
        cursor = sqliteConnection.cursor()
        weather_query = "SELECT * FROM weather_data;"

        cursor.execute(weather_query)
        record = cursor.fetchall()

        _create_unverified_https_context = ssl._create_unverified_context
        data_list = []

        for row in record:
            data_list.append({
                "What's the weather for the next week in " + row[1] + " at " + row[2] + "?": {
                    'id': row[0],
                    'name': row[1],
                    'date': row[2],
                    'feels_like': row[3],
                    'wind_speed': row[4],
                    'Humidity': row[5],
                    'Temperature': row[6],
                    'Maximum Temperature': row[7],
                    'Minimum Temperature': row[8],
                    'Weather Description': row[9],
                    'Main Weather': row[10]
                }})
        text_file_path = "weatherData/general_weather_question.json"
        with open(text_file_path, 'w') as file:
            json.dump(data_list, file, indent=2)
