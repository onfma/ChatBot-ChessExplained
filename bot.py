from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer, ChatterBotCorpusTrainer
import collections.abc
collections.Hashable = collections.abc.Hashable

chatbot = ChatBot("ChessBot")

# Crearea unui antrenor pentru chatbot
trainer = ChatterBotCorpusTrainer(chatbot)

# Antrenarea chatbotului pe baza corpusului în limba engleză
trainer.train("chatterbot.corpus.english")
trainer.train("data")

while True:
    request = input("> ")
    response = chatbot.get_response(request)
    print(f"♟️ {response}")


