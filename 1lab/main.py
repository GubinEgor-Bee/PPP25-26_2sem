class Move:
    def __init__(self, sr, sc, er, ec):
        self.start_row = sr
        self.start_col = sc
        self.end_row = er
        self.end_col = ec


class Piece:
    def __init__(self, color):
        self._color = color

    def get_color(self):
        return self._color

    def symbol(self):
        return "?"

    def valid_moves(self, board, row, col):
        return []

    def slide_moves(self, board, row, col, directions):

        moves = []

        for dr, dc in directions:
            r = row + dr
            c = col + dc

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

    def jump_moves(self, board, row, col, steps):

        moves = []

        for dr, dc in steps:
            r = row + dr
            c = col + dc

            if board.in_bounds(r, c):
                if (
                    board.is_empty(r, c)
                    or board.get_piece(r, c).get_color() != self._color
                ):
                    moves.append((r, c))

        return moves


class Pawn(Piece):
    def symbol(self):
        return "P" if self._color == "white" else "p"

    def valid_moves(self, board, row, col):

        moves = []

        direction = -1 if self._color == "white" else 1

        if board.is_empty(row + direction, col):
            moves.append((row + direction, col))

            start = 6 if self._color == "white" else 1

            if row == start and board.is_empty(row + 2 * direction, col):
                moves.append((row + 2 * direction, col))

        for dc in [-1, 1]:
            r = row + direction
            c = col + dc

            if board.in_bounds(r, c):
                piece = board.get_piece(r, c)

                if piece and piece.get_color() != self._color:
                    moves.append((r, c))

                if (r, c) == board.en_passant_target:
                    moves.append((r, c))

        return moves


class Rook(Piece):
    def symbol(self):
        return "R" if self._color == "white" else "r"

    def valid_moves(self, board, row, col):

        dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        return self.slide_moves(board, row, col, dirs)


class Bishop(Piece):
    def symbol(self):
        return "B" if self._color == "white" else "b"

    def valid_moves(self, board, row, col):

        dirs = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

        return self.slide_moves(board, row, col, dirs)


class Queen(Piece):
    def symbol(self):
        return "Q" if self._color == "white" else "q"

    def valid_moves(self, board, row, col):

        dirs = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]

        return self.slide_moves(board, row, col, dirs)


class Knight(Piece):
    def symbol(self):
        return "N" if self._color == "white" else "n"

    def valid_moves(self, board, row, col):

        steps = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]

        return self.jump_moves(board, row, col, steps)


class King(Piece):
    def symbol(self):
        return "K" if self._color == "white" else "k"

    def valid_moves(self, board, row, col):

        steps = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]

        return self.jump_moves(board, row, col, steps)


class FirstNewFigure(Piece):
    def symbol(self):
        return "O" if self._color == "white" else "o"

    def valid_moves(self, board, row, col):

        dirs = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]

        moves = []

        for dr, dc in dirs:
            r = row + dr
            c = col + dc
            step = 1

            while board.in_bounds(r, c):
                if step % 2 == 1:
                    if board.is_empty(r, c):
                        moves.append((r, c))
                    else:
                        if board.get_piece(r, c).get_color() != self._color:
                            moves.append((r, c))
                        break
                else:
                    if not board.is_empty(r, c):
                        break

                r += dr
                c += dc
                step += 1

        return moves


class SecondNewFigure(Piece):
    def symbol(self):
        return "A" if self._color == "white" else "a"

    def valid_moves(self, board, row, col):

        return Bishop.valid_moves(self, board, row, col) + Knight.valid_moves(
            self, board, row, col
        )


class ThirdNewFigure(Piece):
    def symbol(self):
        return "E" if self._color == "white" else "e"

    def valid_moves(self, board, row, col):

        moves = []

        for dr in range(-2, 3):
            for dc in range(-2, 3):
                if dr == 0 and dc == 0:
                    continue

                r = row + dr
                c = col + dc

                if board.in_bounds(r, c):
                    if (
                        board.is_empty(r, c)
                        or board.get_piece(r, c).get_color() != self._color
                    ):
                        moves.append((r, c))

        return moves


class MoveRecord:
    def __init__(self, move, piece, captured, player, enpass):

        self.move = move
        self.moved_piece = piece
        self.captured_piece = captured
        self.player_color = player
        self.en_passant = enpass


class Board:
    def __init__(self):

        self._board = [[None] * 8 for _ in range(8)]
        self._history = []
        self.en_passant_target = None

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

        if not self.in_bounds(r, c):
            return False

        return self._board[r][c] is None

    def get_piece(self, r, c):
        return self._board[r][c]

    def find_king(self, color):

        for r in range(8):
            for c in range(8):
                p = self.get_piece(r, c)

                if p and isinstance(p, King) and p.get_color() == color:
                    return (r, c)

        return None

    def get_attacked_squares(self, enemy):

        attacked = []

        for r in range(8):
            for c in range(8):
                p = self.get_piece(r, c)

                if p and p.get_color() == enemy:
                    if isinstance(p, Pawn):
                        direction = -1 if enemy == "white" else 1

                        for dc in [-1, 1]:
                            rr = r + direction
                            cc = c + dc

                            if self.in_bounds(rr, cc):
                                attacked.append((rr, cc))

                    else:
                        attacked.extend(p.valid_moves(self, r, c))

        return attacked

    def is_check(self, color):

        enemy = "black" if color == "white" else "white"

        king = self.find_king(color)

        if king is None:
            return False

        return king in self.get_attacked_squares(enemy)

    def get_pieces_under_attack(self, color):

        enemy = "black" if color == "white" else "white"

        attacked = self.get_attacked_squares(enemy)

        danger = []

        for r in range(8):
            for c in range(8):
                p = self.get_piece(r, c)

                if p and p.get_color() == color:
                    if (r, c) in attacked:
                        danger.append((r, c))

        return danger

    def move(self, move, player):

        piece = self._board[move.start_row][move.start_col]

        if piece is None:
            return False

        valid = piece.valid_moves(self, move.start_row, move.start_col)

        if (move.end_row, move.end_col) not in valid:
            return False

        captured = self._board[move.end_row][move.end_col]

        if (
            isinstance(piece, Pawn)
            and (move.end_row, move.end_col) == self.en_passant_target
        ):
            direction = 1 if piece.get_color() == "white" else -1

            captured = self._board[move.end_row + direction][move.end_col]

            self._board[move.end_row + direction][move.end_col] = None

        self._history.append(
            MoveRecord(move, piece, captured, player, self.en_passant_target)
        )

        self._board[move.end_row][move.end_col] = piece
        self._board[move.start_row][move.start_col] = None

        self.en_passant_target = None

        if isinstance(piece, Pawn):
            if abs(move.start_row - move.end_row) == 2:
                mid = (move.start_row + move.end_row) // 2
                self.en_passant_target = (mid, move.start_col)

        if isinstance(piece, Pawn):
            if move.end_row in (0, 7):
                self._board[move.end_row][move.end_col] = Queen(piece.get_color())

        if isinstance(captured, King):
            return "game_over"

        return True

    def undo(self):

        if not self._history:
            return None

        rec = self._history.pop()

        self._board[rec.move.start_row][rec.move.start_col] = rec.moved_piece
        self._board[rec.move.end_row][rec.move.end_col] = rec.captured_piece

        self.en_passant_target = rec.en_passant

        return rec.player_color

    def print_board(self, highlights=None, captures=None, danger=None, check=False):

        highlights = highlights or []
        captures = captures or []
        danger = danger or []

        print("  A B C D E F G H")

        for r in range(8):
            row = str(8 - r) + " "

            for c in range(8):
                if (r, c) in captures:
                    row += "x "
                    continue

                if (r, c) in highlights:
                    row += "* "
                    continue

                piece = self._board[r][c]

                if (r, c) in danger and piece:
                    if isinstance(piece, King) and check:
                        row += piece.symbol() + "! "
                    else:
                        row += piece.symbol() + "! "

                    continue

                row += (piece.symbol() if piece else ".") + " "

            print(row)

        print()


def main():

    board = Board()
    current_turn = "white"

    while True:
        print("Ход:", "Белых" if current_turn == "white" else "Чёрных")

        danger = board.get_pieces_under_attack(current_turn)
        check = board.is_check(current_turn)

        if check:
            king = board.find_king(current_turn)
            if king and king not in danger:
                danger.append(king)

        board.print_board(danger=danger, check=check)

        if check:
            print("ШАХ!")

        command = input(
            "Выберите фигуру (например A1), 'end' - выход, 'back' - откат назад на 1 ход "
        )

        if command.lower() == "end":
            break

        if command.lower() == "back":
            player = board.undo()

            if player:
                current_turn = player

            continue

        if len(command) != 2:
            print("Неверный формат!")
            continue

        col = ord(command[0].upper()) - ord("A")
        row = 8 - int(command[1])

        piece = board.get_piece(row, col)

        if piece is None:
            print("Нет фигуры")
            continue

        if piece.get_color() != current_turn:
            print("Это не ваша фигура!")
            continue

        moves = piece.valid_moves(board, row, col)

        highlights = []
        captures = []

        for r, c in moves:
            target = board.get_piece(r, c)

            if target is None:
                highlights.append((r, c))
            else:
                captures.append((r, c))

        board.print_board(
            highlights=highlights, captures=captures, danger=danger, check=check
        )

        target = input("Куда ходить? (например E4): ")

        if len(target) != 2:
            continue

        ec = ord(target[0].upper()) - ord("A")
        er = 8 - int(target[1])

        move = Move(row, col, er, ec)

        result = board.move(move, current_turn)

        if result == "game_over":
            board.print_board()
            print("Игра окончена!")

            break

        if result:
            current_turn = "black" if current_turn == "white" else "white"


if __name__ == "__main__":
    main()
