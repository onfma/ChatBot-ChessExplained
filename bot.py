from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer, ChatterBotCorpusTrainer
import collections.abc
collections.Hashable = collections.abc.Hashable
import io
import chess
import chess.pgn
import chess.engine


def verify_chess_input(input, color):
    if (len(input) % 2 == 0 and color == "w") or (len(input) % 2 == 1 and color == "b"): return True
    else: return False

def parse_moves(moves_str):
    moves = chess.pgn.read_game(io.StringIO(moves_str)).mainline_moves()
    return [move.uci()[:-1] if move.uci().endswith('+') else move.uci() for move in moves]

def get_best_move_from_moves_string(moves_string):
    engine = chess.engine.SimpleEngine.popen_uci("stockfish\stockfish-windows-x86-64-modern.exe")
    
    board = chess.Board()
    moves = parse_moves(moves_string)
    
    for move in moves:
        board.push(chess.Move.from_uci(move))
    
    print("Tabla ta este: ")
    print(board)

    result = engine.play(board, chess.engine.Limit(time=2.0))
    best_move = result.move

    engine.quit()

    print("\nTabla ar deveni: ")
    board.push(best_move)
    print(board)

    return best_move


# player_color = "w" # player_color = "b"
# moves_string = "d4 d5 c4 e5 dxe5 d4 Nf3 Nc6 a3 Bg4 Nbd2 Nge7"
# if verify_chess_input(moves_string.split(), player_color):
#     best_move = get_best_move_from_moves_string(moves_string)
#     print(f"Cea mai bună mutare: {best_move}")
# else:
#     print ("da-mi mutarea oponentului, dupa te ajut")


if __name__ == "main":

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