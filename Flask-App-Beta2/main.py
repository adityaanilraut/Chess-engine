from flask import Flask, render_template, jsonify, request
from chess_engine import ChessEngine, Piece
import os

app = Flask(__name__, static_url_path='/static')

# Global chess engine instance
chess_engine = ChessEngine()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/get_board')
def get_board():
    board_state = []
    for row in range(8):
        board_row = []
        for col in range(8):
            piece = chess_engine.board.get_piece(row, col)
            if piece:
                board_row.append({
                    'type': piece.type,
                    'color': piece.color
                })
            else:
                board_row.append(None)
        board_state.append(board_row)
    return jsonify({'board': board_state})

@app.route('/api/make_move', methods=['POST'])
def make_move():
    data = request.json
    start = tuple(data['start'])
    end = tuple(data['end'])
    
    # Make player's move
    if chess_engine.board.make_move(start, end):
        # Get and make AI's move
        ai_move = chess_engine.get_best_move('black', depth=2)
        if ai_move:
            chess_engine.board.make_move(ai_move[0], ai_move[1])
            return jsonify({
                'success': True,
                'ai_move': {
                    'start': ai_move[0],
                    'end': ai_move[1]
                }
            })
    
    return jsonify({'success': False})

@app.route('/api/valid_moves/<int:row>/<int:col>')
def get_valid_moves(row, col):
    moves = chess_engine.board.get_valid_moves(row, col)
    return jsonify({'moves': moves})

@app.route('/api/new_game', methods=['POST'])
def new_game():
    global chess_engine
    chess_engine = ChessEngine()
    return jsonify({'success': True})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
 