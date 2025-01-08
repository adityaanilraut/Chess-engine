from typing import List, Tuple, Optional
import copy

class Piece:
    def __init__(self, color: str, piece_type: str):
        self.color = color  # 'white' or 'black'
        self.type = piece_type  # 'pawn', 'knight', 'bishop', 'rook', 'queen', 'king'
        self.has_moved = False

    def __str__(self):
        symbol = self.type[0].upper() if self.color == 'white' else self.type[0].lower()
        return 'K' if symbol.upper() == 'K' else symbol

class Board:
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.initialize_board()
    
    def initialize_board(self):
        # Initialize pawns
        for col in range(8):
            self.board[1][col] = Piece('white', 'pawn')
            self.board[6][col] = Piece('black', 'pawn')
        
        # Initialize other pieces
        piece_order = ['rook', 'night', 'bishop', 'queen', 'king', 'bishop', 'night', 'rook']
        for col in range(8):
            self.board[0][col] = Piece('white', piece_order[col])
            self.board[7][col] = Piece('black', piece_order[col])

    def get_piece(self, row: int, col: int) -> Optional[Piece]:
        return self.board[row][col]

    def make_move(self, start: Tuple[int, int], end: Tuple[int, int]) -> bool:
        start_row, start_col = start
        end_row, end_col = end
        piece = self.board[start_row][start_col]
        
        if piece is None:
            return False
        
        # Make the move
        self.board[end_row][end_col] = piece
        self.board[start_row][start_col] = None
        piece.has_moved = True
        return True

    def get_valid_moves(self, row: int, col: int) -> List[Tuple[int, int]]:
        piece = self.get_piece(row, col)
        if piece is None:
            return []
        
        moves = []
        if piece.type == 'pawn':
            moves.extend(self._get_pawn_moves(row, col, piece))
        elif piece.type == 'night':
            moves.extend(self._get_knight_moves(row, col, piece))
        elif piece.type == 'bishop':
            moves.extend(self._get_bishop_moves(row, col, piece))
        elif piece.type == 'rook':
            moves.extend(self._get_rook_moves(row, col, piece))
        elif piece.type == 'queen':
            moves.extend(self._get_queen_moves(row, col, piece))
        elif piece.type == 'king':
            moves.extend(self._get_king_moves(row, col, piece))
        
        return moves

    def _get_pawn_moves(self, row: int, col: int, piece: Piece) -> List[Tuple[int, int]]:
        moves = []
        direction = 1 if piece.color == 'white' else -1
        
        # Forward move
        if 0 <= row + direction < 8 and self.board[row + direction][col] is None:
            moves.append((row + direction, col))
            # Initial two-square move
            if ((piece.color == 'white' and row == 1) or 
                (piece.color == 'black' and row == 6)) and \
               self.board[row + 2 * direction][col] is None:
                moves.append((row + 2 * direction, col))
        
        # Captures
        for col_offset in [-1, 1]:
            new_col = col + col_offset
            if 0 <= new_col < 8:
                new_row = row + direction
                if 0 <= new_row < 8:
                    target = self.board[new_row][new_col]
                    if target and target.color != piece.color:
                        moves.append((new_row, new_col))
        
        return moves

    def _get_knight_moves(self, row: int, col: int, piece: Piece) -> List[Tuple[int, int]]:
        moves = []
        offsets = [
            (-2, -1), (-2, 1), (-1, -2), (-1, 2),
            (1, -2), (1, 2), (2, -1), (2, 1)
        ]
        
        for row_offset, col_offset in offsets:
            new_row, new_col = row + row_offset, col + col_offset
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                target = self.board[new_row][new_col]
                if target is None or target.color != piece.color:
                    moves.append((new_row, new_col))
        
        return moves

    def _get_bishop_moves(self, row: int, col: int, piece: Piece) -> List[Tuple[int, int]]:
        moves = []
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        
        for row_dir, col_dir in directions:
            new_row, new_col = row + row_dir, col + col_dir
            while 0 <= new_row < 8 and 0 <= new_col < 8:
                target = self.board[new_row][new_col]
                if target is None:
                    moves.append((new_row, new_col))
                elif target.color != piece.color:
                    moves.append((new_row, new_col))
                    break
                else:
                    break
                new_row += row_dir
                new_col += col_dir
        
        return moves

    def _get_rook_moves(self, row: int, col: int, piece: Piece) -> List[Tuple[int, int]]:
        moves = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        for row_dir, col_dir in directions:
            new_row, new_col = row + row_dir, col + col_dir
            while 0 <= new_row < 8 and 0 <= new_col < 8:
                target = self.board[new_row][new_col]
                if target is None:
                    moves.append((new_row, new_col))
                elif target.color != piece.color:
                    moves.append((new_row, new_col))
                    break
                else:
                    break
                new_row += row_dir
                new_col += col_dir
        
        return moves

    def _get_queen_moves(self, row: int, col: int, piece: Piece) -> List[Tuple[int, int]]:
        return self._get_bishop_moves(row, col, piece) + self._get_rook_moves(row, col, piece)

    def _get_king_moves(self, row: int, col: int, piece: Piece) -> List[Tuple[int, int]]:
        moves = []
        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),           (0, 1),
            (1, -1),  (1, 0),  (1, 1)
        ]
        
        for row_dir, col_dir in directions:
            new_row, new_col = row + row_dir, col + col_dir
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                target = self.board[new_row][new_col]
                if target is None or target.color != piece.color:
                    moves.append((new_row, new_col))
        
        return moves

class ChessEngine:
    def __init__(self):
        self.board = Board()
        self.piece_values = {
            'pawn': 100,
            'night': 320,
            'bishop': 330,
            'rook': 500,
            'queen': 900,
            'king': 20000
        }

    def evaluate_position(self) -> int:
        score = 0
        matrix = [
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,1.1,1.1,1.1,1.1,0,0],
            [0,0,1.1,1.1,1.1,1.1,0,0],
            [0,0,1.1,1.1,1.1,1.1,0,0],
            [0,0,1.1,1.1,1.1,1.1,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
        ]
        for row in range(8):
            for col in range(8):
                piece = self.board.get_piece(row, col)
                if piece:
                    value = self.piece_values[piece.type]
                    if piece.color == 'white':
                        #score += value
                        score += value + matrix[row][col]
                    else:
                        score -= value - matrix[row][col]
        return score

    def minimax(self, depth: int, alpha: float, beta: float, maximizing_player: bool) -> Tuple[int, Optional[Tuple[Tuple[int, int], Tuple[int, int]]]]:
        if depth == 0:
            return self.evaluate_position(), None

        best_move = None
        if maximizing_player:
            max_eval = float('-inf')
            for start_pos, moves in self._get_all_moves('white'):
                for end_pos in moves:
                    # Make move
                    temp_board = copy.deepcopy(self.board)
                    self.board.make_move(start_pos, end_pos)
                    
                    eval, _ = self.minimax(depth - 1, alpha, beta, False)
                    
                    # Undo move
                    self.board = temp_board
                    
                    if eval > max_eval:
                        max_eval = eval
                        best_move = (start_pos, end_pos)
                    
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
            
            return max_eval, best_move
        else:
            min_eval = float('inf')
            for start_pos, moves in self._get_all_moves('black'):
                for end_pos in moves:
                    # Make move
                    temp_board = copy.deepcopy(self.board)
                    self.board.make_move(start_pos, end_pos)
                    
                    eval, _ = self.minimax(depth - 1, alpha, beta, True)
                    
                    # Undo move
                    self.board = temp_board
                    
                    if eval < min_eval:
                        min_eval = eval
                        best_move = (start_pos, end_pos)
                    
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
            
            return min_eval, best_move

    def _get_all_moves(self, color: str) -> List[Tuple[Tuple[int, int], List[Tuple[int, int]]]]:
        moves = []
        for row in range(8):
            for col in range(8):
                piece = self.board.get_piece(row, col)
                if piece and piece.color == color:
                    valid_moves = self.board.get_valid_moves(row, col)
                    if valid_moves:
                        moves.append(((row, col), valid_moves))
        return moves

    def get_best_move(self, color: str, depth: int = 100) -> Optional[Tuple[Tuple[int, int], Tuple[int, int]]]:
        _, best_move = self.minimax(depth, float('-inf'), float('inf'), color == 'white')
        return best_move

    def print_board(self):
        for row in range(7, -1, -1):
            print(f"{row + 1} ", end="")
            for col in range(8):
                piece = self.board.get_piece(row, col)
                if piece:
                    print(f" {piece} ", end="")
                else:
                    print(" . ", end="")
            print()
        print("   a  b  c  d  e  f  g  h") 