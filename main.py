from flask import *
from flask_sqlalchemy import SQLAlchemy
import json
from WeatherAPIProcessor import WeatherAPIProcessor
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer, ChatterBotCorpusTrainer
import ssl
from DataWrangler import DataWrangler

app = Flask(__name__)
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

# Database set up
db_name = "weather.db"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
bot = ChatBot(
    'Steve',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    logic_adapters=[
        'chatterbot.logic.BestMatch',
    ],
    database_uri='sqlite:///' + db_name
)
bot.storage.drop()
trainer = ListTrainer(bot)

beans = DataWrangler()
beans.bot_training_data()

training_data = "weatherData/general_weather_question.json"

with open(training_data, 'r') as file:
    json_data = json.load(file)

for entry in json_data:
    weather_section = next(iter(entry))
    weather_details = entry[weather_section]
    trainer.train([str(weather_section), str(weather_details)])


@app.route("/", methods=["POST", "GET"])
def index():
    return render_template('index.html', result="WOW")


@app.route("/get", methods=["GET","POST"])
def chatbot_response():
    msg = request.form["msg"]
    response = bot.get_response(msg)
    return str(response)



if __name__ == '__main__':
    try:
        weather_api_db_creation = WeatherAPIProcessor()
        weather_api_db_creation.weather_db_creation()
    finally:
        app.run(debug=True)
