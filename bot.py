import io
import re
import yaml
import chess
import chess.pgn
import chess.engine
from chatterbot import ChatBot
from chatterbot.conversation import Statement
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.comparisons import LevenshteinDistance
import collections.abc
collections.Hashable = collections.abc.Hashable

def extract_moves(question):
    move_pattern = re.compile(r'\b(?:[KQRBN]?[a-h]?[1-8]?x?[a-h][1-8]|O-O(?:-O)?)\b')
    moves = re.findall(move_pattern, question)
    result_string = ' '.join(moves)
    return result_string

def categorize_question(question):
    keywords = ["best move", "best next move", "to do next", "optimal move", "recommended move", "strategy", "tactics"]

    for keyword in keywords:
        if keyword in question.lower():
            return True
    
    return 

def parse_moves(moves_str):
    moves = chess.pgn.read_game(io.StringIO(moves_str)).mainline_moves()
    return [move.uci()[:-1] if move.uci().endswith('+') else move.uci() for move in moves]

def get_best_move(moves_string):
    engine = chess.engine.SimpleEngine.popen_uci("stockfish\stockfish-windows-x86-64-modern.exe")
    
    board = chess.Board()
    moves = parse_moves(moves_string)
    
    for move in moves:
        board.push(chess.Move.from_uci(move))
    
    print("♟️ Current chess table: ")
    print(board)

    result = engine.play(board, chess.engine.Limit(time=2.0))
    best_move = result.move

    engine.quit()

    print("\n ♟️ Chess table after taking the best move: ")
    board.push(best_move)
    print(board)

    return best_move

def compare_statements(statement):
    levenshtein = LevenshteinDistance()
    statement1 = Statement(statement)
    with open('data.yml', 'r') as f:
        data = yaml.safe_load(f)
    statements = [Statement(conversation[0]) for conversation in data['conversations']]
    max_similarity = 0
    most_similar_statement = None
    for statement in statements:
        similarity = levenshtein.compare(statement1, statement)
        if similarity > max_similarity:
            max_similarity = similarity
            most_similar_statement = statement

    return most_similar_statement.text, max_similarity


chatbot = ChatBot("ChessBot")
trainer = ChatterBotCorpusTrainer(chatbot)

trainer.train("chatterbot.corpus.english.ai")
trainer.train("chatterbot.corpus.english.botprofile")
trainer.train("chatterbot.corpus.english.conversations")
trainer.train("chatterbot.corpus.english.greetings")
trainer.train("chatterbot.corpus.english.humor")
trainer.train("chatterbot.corpus.english.trivia")
trainer.train("data")

player_color = "w" # player_color = "b"

exit_conditions = (":q", "quit", "exit")
while True:
    request = input("> ")
    if request in exit_conditions:
        break
    
    moves = extract_moves(request)
    
    if moves:
        player_color = "w" if len(moves.split()) % 2 == 0 else "b"
        if categorize_question(request):
            best_move = get_best_move(moves)
            print(f"♟️ Best move in your case: {best_move}")
        else:
            print ("♟️ I don't understand the question.")  
    else:
        most_similar_statement, max_similarity = compare_statements(request)
        # print(f"Cel mai similar statement pentru '{request}' este: '{most_similar_statement}' cu o similaritate de {max_similarity}")
        if max_similarity > 0.55:
            response = chatbot.get_response(most_similar_statement)
        else:
            response = chatbot.get_response(request)
        print(f"♟️ {response}")


# Comenzi:
# python -m venv venv
# venv\Scripts\activate