import chess
import chess.pgn
import io
from collections import defaultdict

def parse_moves(moves_str):
    moves = chess.pgn.read_game(io.StringIO(moves_str)).mainline_moves()
    return [move.uci()[:-1] if move.uci().endswith('+') else move.uci() for move in moves]

def find_winner_moves(game_str, winner_moves_dict):
    board = chess.Board()
    moves = parse_moves(game_str)
    
    for move in moves:
        board.push(chess.Move.from_uci(move))
    
    if board.is_checkmate():
        winner_color = "White" if board.turn == chess.WHITE else "Black"
        winner_moves = tuple(board.move_stack[-3:])
        winner_moves_dict[winner_moves] += 1

def main():
    with open('games.txt', 'r') as file:
        games = file.read().split('#')

    winner_moves_dict = defaultdict(int)

    for game in games:
        if game.strip():  # Ignore empty strings
            find_winner_moves(game + "#", winner_moves_dict)  # Add '#' to mark the end of the last game

    for winner_moves, occurrences in winner_moves_dict.items():
        if occurrences >= 2:
            print(f"Winner Moves: {', '.join(move.uci() for move in winner_moves)}")
            print(f"Occurrences: {occurrences}\n")

if __name__ == "__main__":
    main()
