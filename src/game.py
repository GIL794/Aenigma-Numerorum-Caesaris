import os
import time
import pygame
from .board import SudokuBoard, sample_puzzle
from .romannum import int_to_roman, roman_to_int, normalize_roman_input
from .ui import (WINDOW_WIDTH, WINDOW_HEIGHT, TOP_BAR, MARGIN, draw_text,
                 draw_grid, draw_rules, CELL_SIZE, YELLOW, BLACK, WHITE)

ASSETS_FONT_PATH = os.path.join(os.path.dirname(__file__), "assets", "fonts", "NotoSans-Regular.ttf")

def load_font(size):
    try:
        return pygame.font.Font(ASSETS_FONT_PATH, size)
    except Exception:
        return pygame.font.SysFont("arial", size)

def main():
    pygame.init()
    pygame.display.set_caption("Roman Sudoku")
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    font_small = load_font(18)
    font_cell = load_font(30)
    clock = pygame.time.Clock()

    loaded = SudokuBoard.load_if_exists()
    if loaded is None:
        puzzle, solution = sample_puzzle()
        board = SudokuBoard(puzzle, solution)
    else:
        board = loaded

    selected = None
    running = True
    paused = False
    start_time = time.time()
    paused_accum = 0.0
    pause_started = None
    roman_buffer = ""  # collects typed I/V/X before committing

    while running:
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
                    board.randomize_symbol_perm()
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
                grid_y0 = TOP_BAR
                if grid_x0 <= x <= grid_x0 + 9 * CELL_SIZE and grid_y0 <= y <= grid_y0 + 9 * CELL_SIZE:
                    c = (x - grid_x0) // CELL_SIZE
                    r = (y - grid_y0) // CELL_SIZE
                    selected = (int(r), int(c))
                    roman_buffer = ""

        # Drawing
        screen.fill(WHITE)
        # Elapsed time
        if paused:
            elapsed = int((pause_started - start_time - paused_accum)) if pause_started else int((time.time() - start_time - paused_accum))
        else:
            elapsed = int(time.time() - start_time - paused_accum)

        # Rules and status
        draw_rules(screen, font_small, elapsed, paused)
        # Grid and cells
        draw_grid(screen, font_cell, board, selected)

        # Win state
        if board.is_complete():
            msg = "Completed! Press R to reshuffle symbols or Q to quit."
            draw_text(screen, msg, font_small, BLACK, (MARGIN, 75))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
