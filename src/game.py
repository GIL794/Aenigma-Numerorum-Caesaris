import os
import sys
import time
import math
import pygame
from .board import SudokuBoard, sample_puzzle
from .romannum import int_to_roman, roman_to_int, normalize_roman_input
from .ui import (WINDOW_WIDTH, WINDOW_HEIGHT, TOP_BAR, RULES_HEIGHT, MARGIN, draw_animated_laurel, draw_menu, draw_text,
                 draw_grid, draw_rules, CELL_SIZE, YELLOW, BLACK, WHITE, draw_title)

ASSETS_FONT_PATH = os.path.join(os.path.dirname(__file__), "assets", "fonts", "NotoSans-Regular.ttf")
ASSETS_TITLE_FONT_PATH = os.path.join(os.path.dirname(__file__), "assets", "fonts", "NotoSans-Regular.ttf")
ASSETS_EAGLE_PATH = os.path.join(os.path.dirname(__file__), "assets", "images", "eagle.png")

def load_font(size, path=ASSETS_FONT_PATH):
    try:
        return pygame.font.Font(path, size)
    except (FileNotFoundError, pygame.error):
        return pygame.font.SysFont("serif", size)

def load_title_font(size):
    try:
        return pygame.font.Font(ASSETS_TITLE_FONT_PATH, size)
    except (FileNotFoundError, pygame.error):
        return pygame.font.SysFont("serif", size, bold=True)

def load_eagle():
    try:
        img = pygame.image.load(ASSETS_EAGLE_PATH)
        return pygame.transform.scale(img, (48, 48))
    except (FileNotFoundError, pygame.error):
        return None

def start_menu(screen, font_title, font_button, title, desc, show_resume, eagle_img=None):
    """Display the start menu and handle user input.
    
    Args:
        screen: Pygame display surface
        font_title: Font for title text
        font_button: Font for button text
        title: Game title string
        desc: Game description string
        show_resume: Whether to show the resume button
        eagle_img: Optional eagle icon image
        
    Returns:
        str: "new" for new game or "resume" to resume saved game
    """
    clock = pygame.time.Clock()
    frame = 0
    while True:
        frame += 1
        new_rect, resume_rect = draw_menu(screen, font_title, font_button, title, desc, show_resume, eagle_img, frame)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if new_rect.collidepoint(event.pos):
                    return "new"
                if resume_rect and resume_rect.collidepoint(event.pos):
                    return "resume"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n:
                    return "new"
                if show_resume and event.key == pygame.K_r:
                    return "resume"
        clock.tick(30)

def main():
    """Main game loop for Aenigma Numerorum Caesaris (Roman Numeral Sudoku).
    
    Initializes pygame, displays the start menu, and runs the game loop with
    controls for pause, resume, new game, hints, and cell selection/input.
    """
    try:
        pygame.init()
        pygame.display.set_caption("Aenigma Numerorum Caesaris")
        screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    except pygame.error as e:
        print(f"Failed to initialize pygame: {e}")
        sys.exit(1)
    font_small = load_font(18)
    font_cell = load_font(30)
    font_title = load_title_font(48)  # Large, bold Roman font
    font_desc = load_font(20)
    font_button = load_title_font(32)
    eagle_img = load_eagle()
    clock = pygame.time.Clock()

    title = "Aenigma Numerorum Caesaris"
    desc = "A Roman Sudoku: Fill the grid with I–IX, following classic Sudoku rules. Glory to the Empire!"

    # Show start menu
    show_resume = SudokuBoard.load_if_exists() is not None
    choice = start_menu(screen, font_title, font_button, title, desc, show_resume, eagle_img)
    if choice == "resume":
        board = SudokuBoard.load_if_exists()
    else:
        puzzle, solution = sample_puzzle()
        board = SudokuBoard(puzzle, solution)

    selected = None
    running = True
    paused = False
    start_time = time.time()
    paused_accum = 0.0
    pause_started = None
    roman_buffer = ""  # collects typed I/V/X before committing

    frame = 0
    while running:
        frame += 1
        dt = clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                board.save()
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    board.save()
                    running = False
                elif event.key == pygame.K_p:
                    if not paused:
                        paused = True
                        pause_started = time.time()
                    else:
                        paused = False
                        if pause_started:
                            paused_accum += time.time() - pause_started
                            pause_started = None
                elif event.key == pygame.K_r:
                    # Start a new game with a new puzzle and solution
                    puzzle, solution = sample_puzzle()
                    board = SudokuBoard(puzzle, solution)
                    selected = None
                    start_time = time.time()
                    paused_accum = 0.0
                    pause_started = None
                    roman_buffer = ""
                elif event.key == pygame.K_h:
                    hint = board.get_hint_cell()
                    if hint and not paused:
                        r, c, v = hint
                        if not board.fixed[r][c]:
                            board.set_cell(r, c, v)
                elif event.key in (pygame.K_DELETE, pygame.K_BACKSPACE):
                    if selected and not paused:
                        r, c = selected
                        board.clear_cell(r, c)
                        roman_buffer = ""
                elif event.key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN):
                    if selected:
                        r, c = selected
                    else:
                        r, c = (0, 0)
                    if event.key == pygame.K_LEFT:
                        c = (c - 1) % 9
                    elif event.key == pygame.K_RIGHT:
                        c = (c + 1) % 9
                    elif event.key == pygame.K_UP:
                        r = (r - 1) % 9
                    elif event.key == pygame.K_DOWN:
                        r = (r + 1) % 9
                    selected = (r, c)
                else:
                    if paused:
                        continue
                    # Handle numeric keys 1..9 as convenience
                    if pygame.K_1 <= event.key <= pygame.K_9:
                        if selected:
                            r, c = selected
                            if not board.fixed[r][c]:
                                digit = event.key - pygame.K_0
                                board.set_cell(r, c, digit)
                                roman_buffer = ""
                    else:
                        # Handle I/V/X Roman entry: buffer and commit when valid
                        ch = event.unicode.upper()
                        if ch in ("I", "V", "X"):
                            roman_buffer += ch
                            roman_commit = normalize_roman_input(roman_buffer)
                            if roman_commit:
                                try:
                                    val = roman_to_int(roman_commit)
                                except Exception:
                                    val = None
                                if val and selected:
                                    r, c = selected
                                    if not board.fixed[r][c]:
                                        board.set_cell(r, c, val)
                                roman_buffer = ""  # reset after commit
                        else:
                            # Any other key resets buffer
                            roman_buffer = ""

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                grid_x0 = MARGIN
                grid_y0 = TOP_BAR + RULES_HEIGHT
                if grid_x0 <= x <= grid_x0 + 9 * CELL_SIZE and grid_y0 <= y <= grid_y0 + 9 * CELL_SIZE:
                    c = (x - grid_x0) // CELL_SIZE
                    r = (y - grid_y0) // CELL_SIZE
                    selected = (int(r), int(c))
                    roman_buffer = ""

        # Drawing
        screen.fill(WHITE)
        # Title and description with laurel, SPQR, eagle
        draw_animated_laurel(screen, frame)
        draw_title(screen, font_title, font_desc, title, desc, eagle_img)
        # Elapsed time
        if paused:
            elapsed = int((pause_started - start_time - paused_accum)) if pause_started else int((time.time() - start_time - paused_accum))
        else:
            elapsed = int(time.time() - start_time - paused_accum)
        # Rules and status
        rules_y = TOP_BAR
        draw_rules(screen, font_small, elapsed, paused, y_offset=rules_y)
        # Grid and cells
        draw_grid(screen, font_cell, board, selected)
        # Win state
        if board.is_complete():
            msg = "Completed! Press R for a new puzzle or Q to quit."
            win_y = TOP_BAR + RULES_HEIGHT + 9 * CELL_SIZE + 10
            draw_text(screen, msg, font_small, BLACK, (MARGIN, win_y))
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
