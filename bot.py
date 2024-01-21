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

def count_consecutive_moves_in_file(move1, move2):
    total_count = 0
    win_count = 0

    with open('games.txt', 'r') as file:
        games = file.read().split('#')

    for game_str in games:
        if game_str.strip():
            moves = parse_moves(game_str + "#")
            
            for i in range(len(moves) - 1):
                if moves[i] == move1 and moves[i + 1] == move2:
                    total_count += 1
                    remaining_moves = len(moves) - (i + 2)
                    if remaining_moves % 2 == 0:
                        win_count += 1 
                    break 

    return total_count, win_count

def get_best_move(moves_string):
    engine = chess.engine.SimpleEngine.popen_uci("stockfish\stockfish-windows-x86-64-modern.exe")
    
    board = chess.Board()
    moves = parse_moves(moves_string)
    was_check = False

    for move in moves:
        board.push(chess.Move.from_uci(move))
    
    print("♟️ Current chess table: ")
    print(board)

    result = engine.play(board, chess.engine.Limit(time=2.0))
    best_move = result.move

    if best_move is None:
        print("♟️ No best move available.")
        return None
        
    engine.quit()

    is_in_check = board.is_check()
    if is_in_check:
        was_check = True

    print("\n ♟️ Chess table after taking the best move: ")
    board.push(best_move)
    print(board)

    best_move_uci = best_move.uci()
    last_move = moves[-1]
    x, y = count_consecutive_moves_in_file(last_move, best_move_uci)
    s = 0
    if y == 0 or x == 0:
        s = 0
    else:
        s = y/x*100

    if board.is_checkmate():
        print("\n♟️ This is a checkmate move.")
        s = 100

    if was_check:
        print("\n♟️ The king was in check.")
    
    print("\n♟️ The winning percentage for the next move:", s, "%")
    
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

#e4 c5 Nf3 Nf6 Bc4 e6 d3
#e4 Nc6 Nf3 a6 Bc4 Na5 Qe2 b5 Bd3 
#d4 g6 e4 Bg7 Nf3 d5 e5 e6 Nc3 Ne7 Be2 a6 O-O O-O a3 Bd7 b4 c5 bxc5 b6 cxb6
#next move is checkmate: f2f3 e7e5 g2g4 
#the king was in check: e2e4 e7e5 d1h5 g8f6 h5e5 
