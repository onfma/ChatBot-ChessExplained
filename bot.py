from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer, ChatterBotCorpusTrainer
import collections.abc
collections.Hashable = collections.abc.Hashable
import chess
import chess.pgn
import io

def verify_chess_input(input, color):
    if (len(input) % 2 == 0 and color == "w") or (len(input) % 2 == 1 and color == "b"): return True
    else: return False

def find_similar_moves(input_chess_table, color):
    input_moves = input_chess_table.split()
    similar_moves = []

    with open('games.txt', 'r') as file:
        games = file.read().split('#')

    for game in games:
        moves = game.split()

        if moves[:len(input_moves)] == input_moves:
            if (len(moves) % 2 == 1 and color == "w") or (len(moves) % 2 == 0 and color == "b"):
                similar_moves.append(moves)
                print(moves)
                print("\n")

    return similar_moves

def recommand_move(input_chess_table, similar_moves):
    best = min(similar_moves, key=len)
    best = best[len(input_chess_table.split())]
    print(best)
    return best


if __name__ == "main":

    chatbot = ChatBot("ChessBot")

    # Crearea unui antrenor pentru chatbot
    trainer = ChatterBotCorpusTrainer(chatbot)

    # Antrenarea chatbotului pe baza corpusului în limba engleză
    trainer.train("chatterbot.corpus.english")
    trainer.train("data")

    # while True:
    #     request = input("> ")
    #     response = chatbot.get_response(request)
    #     print(f"♟️ {response}")


player_color = "w" # player_color = "b"
chess_board_input = "e4 e6 Bc4 d5 exd5 exd5"
if verify_chess_input(chess_board_input.split(), player_color):
    similar = find_similar_moves(chess_board_input, player_color)
    if similar is None:
        print("esti pe barba ta vere")
    else:
        recommand_move(chess_board_input, similar)
else:
    print ("da-mi mutarea oponentului, dupa te ajut")