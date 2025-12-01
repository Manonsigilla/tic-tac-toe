import pygame

# Initialize pygame
pygame.init()

# Constants for the game
WINDOW_SIZE = 600
CELL_SIZE = WINDOW_SIZE // 3  # Each cell is 200x200
LINE_COLOR = (0, 0, 0)  # Black
BG_COLOR = (255, 255, 255)  # White
LINE_WIDTH = 5
FPS = 60

# Initialize window
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Tic Tac Toe")
clock = pygame.time.Clock()

# Game board: list of 9 elements (0-8)
# "" = empty, "X" = cross, "O" = circle
board = [""] * 9

def draw_grid():
    """
    Draw the 3x3 grid on the screen
    """
    screen.fill(BG_COLOR)
    
    # Draw vertical lines
    for i in range(1, 3):
        pygame.draw.line(screen, LINE_COLOR, 
                        (i * CELL_SIZE, 0), 
                        (i * CELL_SIZE, WINDOW_SIZE), 
                        LINE_WIDTH)
    
    # Draw horizontal lines
    for i in range(1, 3):
        pygame.draw.line(screen, LINE_COLOR, 
                        (0, i * CELL_SIZE), 
                        (WINDOW_SIZE, i * CELL_SIZE), 
                        LINE_WIDTH)

def get_cell_from_mouse(pos):
    """
    Convert mouse position to cell index (0-8)
    
    Parameters:
    - pos: tuple (x, y) mouse position
    
    Returns:
    - int: cell index from 0 to 8
    
    Grid layout:
    0 | 1 | 2
    ---------
    3 | 4 | 5
    ---------
    6 | 7 | 8
    """
    x, y = pos
    col = x // CELL_SIZE  # 0, 1, or 2
    row = y // CELL_SIZE  # 0, 1, or 2
    cell_index = row * 3 + col
    return cell_index

def draw_symbols():
    """
    Draw X and O symbols on the board based on current board state
    """
    for i in range(9):
        if board[i] != "":
            # Calculate position
            row = i // 3
            col = i % 3
            center_x = col * CELL_SIZE + CELL_SIZE // 2
            center_y = row * CELL_SIZE + CELL_SIZE // 2
            
            if board[i] == "O":
                # Draw circle (O)
                pygame.draw.circle(screen, (255, 0, 0), 
                    (center_x, center_y), 
                        CELL_SIZE // 3, 
                        LINE_WIDTH)
            
            elif board[i] == "X":
                # Draw cross (X) - two diagonal lines
                offset = CELL_SIZE // 3
                # Line from top-left to bottom-right
                pygame.draw.line(screen, (0, 0, 255),
                    (center_x - offset, center_y - offset),
                    (center_x + offset, center_y + offset),
                        LINE_WIDTH)
                # Line from top-right to bottom-left
                pygame.draw.line(screen, (0, 0, 255),
                    (center_x + offset, center_y - offset),
                    (center_x - offset, center_y + offset),
                    LINE_WIDTH)

# Main game loop
running = True
current_player = "X"  # X starts first

while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Get cell index from mouse click
            cell_index = get_cell_from_mouse(event. pos)
            
            # Check if cell is empty
            if board[cell_index] == "":
                board[cell_index] = current_player
                print(f"Player {current_player} played at position {cell_index}")
                print(f"Board: {board}")
                
                # Switch player
                current_player = "O" if current_player == "X" else "X"
    
    # Drawing
    draw_grid()
    draw_symbols()
    
    # Update display
    pygame.display.flip()
    clock.tick(FPS)

# Quit properly
pygame.quit()