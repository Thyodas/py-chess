from chess import *
import pygame

SQUARE_SIZE = 64
WINDOW_HEIGHT = 512
WINDOW_WIDTH = 512
SQUARE_LIST = [[None for j in range(8)] for i in range(8)]

class Possible_move_circle:
    def __init__(self, surface, x, y):
        self.surface = surface
        self.x = x
        self.y = y

    def draw_circle(self):
        pygame.draw.circle(self.surface, (100,100,100), (self.x*SQUARE_SIZE+SQUARE_SIZE//2, self.x*SQUARE_SIZE+SQUARE_SIZE//2), SQUARE_SIZE//6)

class Squares:
    selected_square = None
    moved_piece_squares = []
    
    @staticmethod
    def reset_selected():
        if Squares.selected_square is not None:
            Squares.selected_square.deselect()
            Squares.selected_square = None
            
    @staticmethod
    def reset_moved():
        for element in Squares.moved_piece_squares:
            element.remove_move_highlight()
        Squares.moved_piece_squares = []
            
    def __init__(self, surface, color, x, y, size):
        self.rect = pygame.Rect(x*size, y*size, size, size)
        self.surface = surface
        self.color = color
        self.x = x
        self.y = y
        self.draw_square()
        
    def draw_square(self):
        pygame.draw.rect(self.surface, self.color, self.rect)
        
    def select(self):
        if self not in Squares.moved_piece_squares:
            self.color = (100, 100, 150) if(self.x + self.y) % 2 == 0 else (100, 80, 150)
            Squares.selected_square = self
    
    def deselect(self):
        self.color = (238, 238, 210) if(self.x + self.y) % 2 == 0 else (118, 150, 85)
        Squares.selected_square = None
        
    def add_move_highlight(self):
        self.color = (246, 246, 105) if(self.x + self.y) % 2 == 0 else (186, 202, 43)
        Squares.moved_piece_squares.append(self)
        
    def remove_move_highlight(self):
        self.color = (238, 238, 210) if(self.x + self.y) % 2 == 0 else (118, 150, 85)

    def __repr__(self):
        return f"<Square {self.color}>"
        
    
        

def board_init(screen, square_size):
    colors = ((238, 238, 210), (118, 150, 85))
    for y in range(8):
        for x in range(8):
            color = colors[(x+y) % 2]
            SQUARE_LIST[y][x] = Squares(screen, color, x, y, square_size)

def draw_board(screen):
    for y in range(8):
        for x in range(8):
            SQUARE_LIST[y][x].draw_square()
            
def draw_pieces(screen, input_board, square_size):
    raw_board = input_board.board
    for y in range(8):
        for x in range(8):
            current_piece = raw_board[y][x]
            if current_piece is not None:
                if not current_piece.is_hidden(): # if piece is set to be visible
                    current_piece.rect = pygame.Rect(x*square_size, y*square_size, square_size, square_size)
                    screen.blit(current_piece.get_image(), current_piece.rect)
            
def main():
    # Pygame
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Chess")
    screen.fill((255, 255, 255))
    myfont = pygame.font.SysFont('Arial', 30)
      
    chessboard = Chessboard()
    raw_board = chessboard.board

    Pieces.load_images(SQUARE_SIZE)
    board_init(screen, SQUARE_SIZE)

    launched = True
    piece_draging = False
    piece_selected = False
    
    while launched:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                launched = False
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # BIND FOR LEFT CLICK
                    for y, rank_list in enumerate(raw_board, 0):
                        for x, piece in enumerate(rank_list, 0):
                            if piece is not None:
                                if piece.rect.collidepoint(event.pos):
                                    # Square selection highlight
                                    Squares.reset_selected()
                                    SQUARE_LIST[y][x].select()
                                    
                                    moving_piece = piece
                                    moving_piece_x = x
                                    moving_piece_y = y
                                    piece_draging = True
                                    piece_selected = True
                                    moving_piece.animation_rect = moving_piece.rect.copy()
                                    moving_piece.hide()


                elif event.button == 3: # BIND FOR RIGHT CLICK
                    # CURRENTLY FOR DEBUGING
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    target_square_x = mouse_x//SQUARE_SIZE
                    target_square_y = mouse_y//SQUARE_SIZE
                    print(f"Target square : {target_square_x}, {target_square_y}")
                    print(SQUARE_LIST[target_square_y][target_square_x])
                    circle = Possible_move_circle(screen, target_square_x, target_square_y)
                    circle.draw_circle()

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:       
                    if piece_draging:
                        piece_draging = False
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        target_square_x = mouse_x//SQUARE_SIZE
                        target_square_y = mouse_y//SQUARE_SIZE
                        if target_square_x != moving_piece_x or target_square_y != moving_piece_y:
                            # Square movement highlight
                            Squares.reset_moved()
                            Squares.reset_selected()
                            piece_square = SQUARE_LIST[moving_piece_y][moving_piece_x]
                            target_square = SQUARE_LIST[target_square_y][target_square_x]
                            piece_square.add_move_highlight()
                            target_square.add_move_highlight()
                            
                            chessboard.move_piece(moving_piece_x, moving_piece_y, mouse_x//SQUARE_SIZE, mouse_y//SQUARE_SIZE)
                            
                            
                        moving_piece.show()
                    elif piece_selected:
                        piece_selected = False
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        target_square_x = mouse_x//SQUARE_SIZE
                        target_square_y = mouse_y//SQUARE_SIZE
                        if target_square_x != moving_piece_x or target_square_y != moving_piece_y:
                            # Square movement highlight
                            
                            Squares.reset_moved()
                            Squares.reset_selected()
                            piece_square = SQUARE_LIST[moving_piece_y][moving_piece_x]
                            target_square = SQUARE_LIST[target_square_y][target_square_x]
                            piece_square.add_move_highlight()
                            target_square.add_move_highlight()
                            
                            chessboard.move_piece(moving_piece_x, moving_piece_y, mouse_x//SQUARE_SIZE, mouse_y//SQUARE_SIZE)
                        
                    
            elif event.type == pygame.MOUSEMOTION:
                if piece_draging:
                    # Moves the piece so that the cursor is in the center of it
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    piece_center_x = moving_piece.animation_rect.x + moving_piece.animation_rect.width//2
                    piece_center_y = moving_piece.animation_rect.y + moving_piece.animation_rect.height//2
                    moving_piece.animation_rect.move_ip(
                        mouse_x-piece_center_x, 
                        mouse_y-piece_center_y)
                    
                    
        draw_board(screen)
        draw_pieces(screen, chessboard, SQUARE_SIZE)
        # draw moving piece
        if piece_draging:
            screen.blit(moving_piece.get_image(), moving_piece.animation_rect)
        pygame.display.flip()

main()