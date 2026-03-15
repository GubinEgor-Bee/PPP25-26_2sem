class Move:
    def __init__(self, start_row, start_col, end_row, end_col):
        self.start_row = start_row
        self.start_col = start_col
        self.end_row = end_row
        self.end_col = end_col


class Piece:
    def __init__(self, color):
        self._color = color

    def get_color(self):
        return self._color

    def symbol(self):
        return "?"

    def valid_moves(self, board, row, col):
        return []


class Pawn(Piece):
    def symbol(self):
        return "P" if self._color == "white" else "p"

    def valid_moves(self, board, row, col):
        moves = []
        direction = -1 if self._color == "white" else 1

        # ход вперед на 1
        if board.is_empty(row + direction, col):
            moves.append((row + direction, col))

            # первый ход на 2
            start_row = 6 if self._color == "white" else 1
            if row == start_row and board.is_empty(row + 2 * direction, col):
                moves.append((row + 2 * direction, col))

        # взятие по диагонали
        for dc in [-1, 1]:
            r = row + direction
            c = col + dc

            if board.in_bounds(r, c):
                piece = board.get_piece(r, c)

                if piece and piece.get_color() != self._color:
                    moves.append((r, c))

        return moves


class Rook(Piece):
    def symbol(self):
        return "R" if self._color == "white" else "r"

    def valid_moves(self, board, row, col):
        moves = []
        directions = [(1,0),(-1,0),(0,1),(0,-1)]

        for dr, dc in directions:
            r, c = row + dr, col + dc
            while board.in_bounds(r, c):
                if board.is_empty(r, c):
                    moves.append((r, c))
                else:
                    if board.get_piece(r, c).get_color() != self._color:
                        moves.append((r, c))
                    break
                r += dr
                c += dc
        return moves


class Knight(Piece):
    def symbol(self):
        return "N" if self._color == "white" else "n"

    def valid_moves(self, board, row, col):
        moves = []
        steps = [
            (2,1),(2,-1),(-2,1),(-2,-1),
            (1,2),(1,-2),(-1,2),(-1,-2)
        ]

        for dr, dc in steps:
            r, c = row + dr, col + dc
            if board.in_bounds(r, c):
                if board.is_empty(r, c) or board.get_piece(r,c).get_color()!=self._color:
                    moves.append((r,c))
        return moves


class Bishop(Piece):
    def symbol(self):
        return "B" if self._color == "white" else "b"

    def valid_moves(self, board, row, col):
        moves = []
        directions = [(1,1),(1,-1),(-1,1),(-1,-1)]

        for dr, dc in directions:
            r, c = row + dr, col + dc
            while board.in_bounds(r,c):
                if board.is_empty(r,c):
                    moves.append((r,c))
                else:
                    if board.get_piece(r,c).get_color()!=self._color:
                        moves.append((r,c))
                    break
                r += dr
                c += dc
        return moves


class Queen(Piece):
    def symbol(self):
        return "Q" if self._color == "white" else "q"

    def valid_moves(self, board, row, col):
        moves = []
        directions = [
            (1,0),(-1,0),(0,1),(0,-1),
            (1,1),(1,-1),(-1,1),(-1,-1)
        ]

        for dr, dc in directions:
            r, c = row + dr, col + dc
            while board.in_bounds(r,c):
                if board.is_empty(r,c):
                    moves.append((r,c))
                else:
                    if board.get_piece(r,c).get_color()!=self._color:
                        moves.append((r,c))
                    break
                r += dr
                c += dc
        return moves


class King(Piece):
    def symbol(self):
        return "K" if self._color == "white" else "k"

    def valid_moves(self, board, row, col):
        moves = []
        directions = [
            (1,0),(-1,0),(0,1),(0,-1),
            (1,1),(1,-1),(-1,1),(-1,-1)
        ]

        for dr, dc in directions:
            r, c = row + dr, col + dc
            if board.in_bounds(r,c):
                if board.is_empty(r,c) or board.get_piece(r,c).get_color()!=self._color:
                    moves.append((r,c))
        return moves


class Board:
    def __init__(self):
        self._board = [[None for _ in range(8)] for _ in range(8)]
        self._history = []  # список MoveRecord
        self.setup()

    def setup(self):
        for i in range(8):
            self._board[6][i] = Pawn("white")
            self._board[1][i] = Pawn("black")

        self._board[7][0] = Rook("white")
        self._board[7][7] = Rook("white")
        self._board[0][0] = Rook("black")
        self._board[0][7] = Rook("black")

        self._board[7][1] = Knight("white")
        self._board[7][6] = Knight("white")
        self._board[0][1] = Knight("black")
        self._board[0][6] = Knight("black")

        self._board[7][2] = Bishop("white")
        self._board[7][5] = Bishop("white")
        self._board[0][2] = Bishop("black")
        self._board[0][5] = Bishop("black")

        self._board[7][3] = Queen("white")
        self._board[0][3] = Queen("black")

        self._board[7][4] = King("white")
        self._board[0][4] = King("black")

    def in_bounds(self, r, c):
        return 0 <= r < 8 and 0 <= c < 8

    def is_empty(self, r, c):
        if not self.in_bounds(r,c):
            return False
        return self._board[r][c] is None

    def get_piece(self, r, c):
        return self._board[r][c]

    def move(self, move, player_color):
        piece = self._board[move.start_row][move.start_col]

        if piece is None:
            print("Нет фигуры")
            return False

        valid = piece.valid_moves(self, move.start_row, move.start_col)
        if (move.end_row, move.end_col) not in valid:
            print("Недопустимый ход")
            return False

        captured_piece = self._board[move.end_row][move.end_col]

        # сохраняем ход в истории
        self._history.append(MoveRecord(move, piece, captured_piece, player_color))

        # применяем ход
        self._board[move.end_row][move.end_col] = piece
        self._board[move.start_row][move.start_col] = None

        return True
    
    def undo(self):
        if not self._history:
            print("Нет ходов для отката")
            return None

        last_record = self._history.pop()

        # возвращаем фигуру на исходную клетку
        self._board[last_record.move.start_row][last_record.move.start_col] = last_record.moved_piece

        # возвращаем взятую фигуру, если была
        self._board[last_record.move.end_row][last_record.move.end_col] = last_record.captured_piece

        print(f"Ход игрока {last_record.player_color} отменён")
        return last_record.player_color

    def print_board(self, highlights=None, captures=None, danger=None, check=False):

        highlights = highlights or []
        captures = captures or []
        danger = danger or []

        print("  A B C D E F G H")

        for r in range(8):
            row_str = str(8 - r) + " "

            for c in range(8):

                if (r, c) in captures:
                    row_str += "x "
                    continue

                if (r, c) in highlights:
                    row_str += "* "
                    continue

                piece = self._board[r][c]

                if (r, c) in danger and piece:
                    if isinstance(piece, King) and check:
                        row_str += "K! "
                    else:
                        row_str += piece.symbol() + "! "
                    continue

                row_str += (piece.symbol() if piece else ".") + " "

            print(row_str)

        print()

    def get_attacked_squares(self, enemy_color):
        attacked = []

        for r in range(8):
            for c in range(8):
                piece = self.get_piece(r, c)

                if piece and piece.get_color() == enemy_color:
                    moves = piece.valid_moves(self, r, c)
                    attacked.extend(moves)

        return attacked
    
    def get_pieces_under_attack(self, color):
        enemy = "black" if color == "white" else "white"

        attacked = self.get_attacked_squares(enemy)

        under_attack = []

        for r in range(8):
            for c in range(8):
                piece = self.get_piece(r, c)

                if piece and piece.get_color() == color:
                    if (r, c) in attacked:
                        under_attack.append((r, c))

        return under_attack
    
    def is_check(self, color):
        enemy = "black" if color == "white" else "white"

        attacked = self.get_attacked_squares(enemy)

        for r in range(8):
            for c in range(8):
                piece = self.get_piece(r, c)

                if piece and isinstance(piece, King) and piece.get_color() == color:
                    return (r, c) in attacked

        return False
    
    def parse_move(self, move_str):
        """
        Преобразует ход вида "E2 E4" в индексы
        """
        try:
            start, end = move_str.split()
            sc = ord(start[0].upper()) - ord('A')
            sr = 8 - int(start[1])
            ec = ord(end[0].upper()) - ord('A')
            er = 8 - int(end[1])
            return Move(sr, sc, er, ec)
        except:
            return None
        
    def get_possible_moves(self, row, col):
        piece = self.get_piece(row, col)

        if piece is None:
            return []

        return piece.valid_moves(self, row, col)
    
    def get_moves_and_captures(self, row, col):
        piece = self.get_piece(row, col)

        if piece is None:
            return [], []

        moves = piece.valid_moves(self, row, col)

        normal_moves = []
        captures = []

        for r, c in moves:
            target = self.get_piece(r, c)

            if target is None:
                normal_moves.append((r, c))
            else:
                captures.append((r, c))

        return normal_moves, captures

class MoveRecord:
    def __init__(self, move, moved_piece, captured_piece, player_color):
        self.move = move                  # объект Move
        self.moved_piece = moved_piece    # фигура, которая ходила
        self.captured_piece = captured_piece  # фигура, если была взята
        self.player_color = player_color 


def main():
    board = Board()
    current_turn = "white"

    while True:
        print("Ход:", "Белых" if current_turn == "white" else "Чёрных")

        danger = board.get_pieces_under_attack(current_turn)
        check = board.is_check(current_turn)

        board.print_board(danger=danger, check=check)

        command = input("Выберите фигуру (например E2) или 'q' для выхода, 'u' для отмены хода: ")

        if command.lower() == "q":
            break

        if command.lower() == "u":
            player = board.undo()
            if player:
                current_turn = player  # восстанавливаем правильного игрока
            continue

        if len(command) != 2:
            print("Неверный формат!")
            continue

        col = ord(command[0].upper()) - ord('A')
        row = 8 - int(command[1])

        piece = board.get_piece(row, col)

        if piece is None:
            print("Нет фигуры")
            continue

        if piece.get_color() != current_turn:
            print("Это не ваша фигура!")
            continue

        moves, captures = board.get_moves_and_captures(row, col)

        if not moves and not captures:
            print("Нет возможных ходов")
            continue

        board.print_board(
            highlights=moves,
            captures=captures,
            danger=danger,
            check=check
        )

        target = input("Куда ходить? (например E4): ")

        if len(target) != 2:
            continue

        ec = ord(target[0].upper()) - ord('A')
        er = 8 - int(target[1])

        move = Move(row, col, er, ec)

        if board.move(move, current_turn):
            current_turn = "black" if current_turn == "white" else "white"


if __name__ == "__main__":
    main()