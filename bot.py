from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer, ChatterBotCorpusTrainer
from cleaner import clean_corpus
import collections.abc
collections.Hashable = collections.abc.Hashable


CORPUS_FILE = "chat.txt"

chatbot = ChatBot("ChessBot")

# Crearea unui antrenor pentru chatbot
corpus_trainer = ChatterBotCorpusTrainer(chatbot)
list_trainer = ListTrainer(chatbot)

# Antrenarea chatbotului pe baza corpusului în limba engleză
corpus_trainer.train("chatterbot.corpus.english")

cleaned_corpus = clean_corpus(CORPUS_FILE)

# Antrenarea chatbotului pe fiecare conversație din cleaned_corpus
for conversation in cleaned_corpus:
    list_trainer.train(conversation)

exit_conditions = (":q", "quit", "exit")
while True:
    query = input("> ")
    if query in exit_conditions:
        break
    else:
        print(f"♟️ {chatbot.get_response(query)}")
