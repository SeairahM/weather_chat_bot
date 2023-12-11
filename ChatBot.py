# Import libraries.
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer, ChatterBotCorpusTrainer
import nltk
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download()

my_bot = ChatBot(
    name="PyBot",
    read_only=True,
    logic_adapters=["chatterbot.logic.MathematicalEvaluation",
                    "chatterbot.logic.BestMatch"]
)

small_talk = [
    "Hello",
    "Hi there!",
    "How are you doing?",
    "I'm doing great.",
    "That is good to hear",
    "Thank you.",
    "You're welcome."
]


list_trainer = ListTrainer(my_bot)

for item in (small_talk, math_talk_1, math_talk_2):
    list_trainer.train(item)

corpus_trainer = ChatterBotCorpusTrainer(my_bot)
corpus_trainer.train('chatterbot.corpus.english')

print(my_bot.get_response("Hi"))
print(my_bot.get_response("How are you?"))
print(my_bot.get_response("What is your name?"))


while True:
    try:
        bot_input = input("You: ")
        bot_response = my_bot.get_response(bot_input)
        print(f"{my_bot.name}: {bot_response}")
    except(KeyboardInterrupt, EOFError, SystemExit):
        break