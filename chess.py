import os, sys
import pygame

class Chessboard:
    def __init__(self, fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"):
        self.board = [[None for j in range(8)] for i in range(8)]
        self.side_to_move = "w"
        self.castling_ability = "KQkq"
        self.en_passant_square = "-"
        self.halfmove_clock = 0
        self.fullmove_counter = 1
        self.fen_parser(fen)

    def fen_parser(self, fen):
        fields = fen.split(" ")

        # piece placement
        if len(fields) >= 1:
            placement = fields[0]
            ranks = placement.split("/")
            if len(ranks) != 8: # raise an exception if too many ranks are specified
                raise ValueError("Invalid piece placement, there are too many ranks")

            for rank_number, rank in enumerate(ranks, 0):
                reading_pos = 0
                insert_pos = 0
                while reading_pos < len(rank) and insert_pos < 8:
                    char = rank[reading_pos]
                    if char.isnumeric():
                        insert_pos += int(char)
                    else:
                        if char.islower():
                            color = "b"
                            if char == "p":
                                self.add_to_board(Pawn(color), insert_pos, rank_number)
                            if char == "r":
                                self.add_to_board(Rook(color), insert_pos, rank_number)
                            elif char == "n":
                                self.add_to_board(Knight(color), insert_pos, rank_number)
                            elif char == "b":
                                self.add_to_board(Bishop(color), insert_pos, rank_number)
                            elif char == "q":
                                self.add_to_board(Queen(color), insert_pos, rank_number)
                            elif char == "k":
                                self.add_to_board(King(color), insert_pos, rank_number)
                        elif char.isupper():
                            color = "w"
                            if char == "P":
                                self.add_to_board(Pawn(color), insert_pos, rank_number)
                            if char == "R":
                                self.add_to_board(Rook(color), insert_pos, rank_number)
                            elif char == "N":
                                self.add_to_board(Knight(color), insert_pos, rank_number)
                            elif char == "B":
                                self.add_to_board(Bishop(color), insert_pos, rank_number)
                            elif char == "Q":
                                self.add_to_board(Queen(color), insert_pos, rank_number)
                            elif char == "K":
                                self.add_to_board(King(color), insert_pos, rank_number)
                        
                        insert_pos += 1

                    reading_pos += 1
                    
        # side to move
        if len(fields) >= 2:
            if fields[1] in "wb":
                self.side_to_move = fields[1]
            else:
                raise ValueError("Invalid side to move, must be 'w' or 'b'")
        else:
            raise ValueError("Missing field, no side to move value")

        # castling ability
        if len(fields) >= 3:
            self.castling_ability = fields[2]
        else:
            raise ValueError("Missing field, no castling ability described")

        # en passant target square
        if len(fields) >= 4:
            self.en_passant_square = fields[3]
        else:
            raise ValueError("Missing field, no en passant square value")

        # halfmove clock
        if len(fields) >= 5:
            self.halfmove_clock = int(fields[4])
        else:
            raise ValueError("Missing field, no halfmove clock value")

        # halfmove clock
        if len(fields) >= 6:
            self.fullmove_counter = int(fields[5])
        else:
            raise ValueError("Missing field, no fullmove counter value")


    def add_to_board(self, piece, x, y):
        self.board[y][x] = piece
        
    def remove_from_board(self, x, y):
        self.board[y][x] = None
        
    def move_piece(self, piece_x, piece_y, x, y):
        if not (piece_x == x and piece_y == y):
            self.board[y][x] = self.board[piece_y][piece_x]
            self.remove_from_board(piece_x, piece_y)
        else:
            print("Cannot move piece to its position")

        

    def __repr__(self):
        string = "  ╔═══╤═══╤═══╤═══╤═══╤═══╤═══╤═══╗\n"
        for rank_number, element  in enumerate(self.board):
            string = "".join([string, 
            f"{8-rank_number} ║ ", 
            " │ ".join([str(piece) if piece is not None else " " for piece in element]),
            " ║",
            "\n  ╟───┼───┼───┼───┼───┼───┼───┼───╢\n"
            ])


        return string[:-37] + "\n  ╚═══╧═══╧═══╧═══╧═══╧═══╧═══╧═══╝\n    a   b   c   d   e   f   g   h"

    def __getitem__(self, index):
        rank_index = 7-index//8
        file_index = index % 8
        return self.board[rank_index][file_index]

class Pieces:
    @staticmethod
    def load_images(square_size):
        print("Loading images")
        Pieces.loaded_images = {}
        module = sys.modules['__main__']
        path, name = os.path.split(module.__file__)
        for color in ("w", "b"):
            for piece in ("rook", "bishop", "knight", "king", "queen", "pawn"):
                piece_name = f"{color}_{piece}"
                full_path = os.path.join(path, f"images/pieces/{piece_name}.png")
                Pieces.loaded_images[piece_name] = pygame.transform.scale(pygame.image.load(full_path), (square_size, square_size))
        
    def __init__(self):
        self.relative_value: float
        self.repr: str
        self.color: str
        self.piece_name: str
        self.hidden = False
    
    def __lt__(self, piece):
        return self.relative_value < piece.relative_value

    def __gt__(self, piece):
        return self.relative_value > piece.relative_value

    def __eq__(self, piece):
        return self.relative_value == piece.relative_value 

    def __ne__(self, piece):
        return self.relative_value != piece.relative_value 

    def __le__(self, piece):
        return self.relative_value <= piece.relative_value 

    def __ge__(self, piece):
        return self.relative_value >= piece.relative_value 

    def __repr__(self):
        return self.repr
    
    def get_image(self):
        return Pieces.loaded_images[f"{self.color}_{self.piece_name}"]
    
    def is_hidden(self):
        return self.hidden == True
    
    def hide(self):
        self.hidden = True
    
    def show(self):
        self.hidden = False
        


class Knight(Pieces):
    relative_value = 4.16
    piece_name = "knight"
    sliding_piece = False
    move_direction = (15, 17, 6, 10, -10, -6, -17, -15)

    def __init__(self, color="w"):
        Pieces.__init__(self)
        self.color = color
        self.repr = "♞" if self.color == "b" else "♘"

class Bishop(Pieces):
    relative_value = 4.41
    piece_name = "bishop"
    sliding_piece = True
    move_direction = (7, 9, -9, -7)

    def __init__(self, color="w"):
        Pieces.__init__(self)
        self.color = color
        self.repr = "♝" if self.color == "b" else "♗"


class Rook(Pieces):
    relative_value = 6.625
    piece_name = "rook"
    sliding_piece = True
    move_direction = (8, -1, 1, -8)

    def __init__(self, color="w"):
        Pieces.__init__(self)
        self.color = color
        self.repr = "♜" if self.color == "b" else "♖"


class Queen(Pieces):
    relative_value = 12.92
    piece_name = "queen"
    sliding_piece = True
    move_direction = (7, 8, 9, -1, 1, -9, -8, -7)

    def __init__(self, color="w"):
        Pieces.__init__(self)
        self.color = color
        self.repr = "♛" if self.color == "b" else "♕"


class Pawn(Pieces):
    relative_value = 1.0
    piece_name = "pawn"
    sliding_piece = False
    move_direction = (8)

    def __init__(self, color="w"):
        Pieces.__init__(self)
        self.color = color
        self.repr = "♟" if self.color == "b" else "♙"

class King(Pieces):
    relative_value = float('inf')
    piece_name = "king"
    sliding_piece = False
    move_direction = (7, 8, 9, -1, 1, -9, -8, -7)

    def __init__(self, color="w"):
        Pieces.__init__(self)
        self.color = color
        self.repr = "♚" if self.color == "b" else "♔"

if __name__ == "__main__":
    chess = Chessboard("8/5kpp/2p2p2/2Pp4/3Pq3/7P/5PP1/Q5K1 b - - 3 31")
    print(chess)


