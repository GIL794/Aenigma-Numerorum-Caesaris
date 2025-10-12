import pygame
from typing import Tuple
from .romannum import int_to_roman

WHITE = (245, 245, 245)
BLACK = (20, 20, 20)
GRID = (50, 50, 50)
BLUE = (66, 135, 245)
RED = (200, 70, 70)
GREEN = (70, 160, 90)
GRAY = (180, 180, 180)
YELLOW = (245, 210, 85)

CELL_SIZE = 60
MARGIN = 20
TOP_BAR = 100
WINDOW_WIDTH = MARGIN * 2 + CELL_SIZE * 9
WINDOW_HEIGHT = TOP_BAR + MARGIN + CELL_SIZE * 9 + MARGIN

def draw_text(surface, text, font, color, pos):
    render = font.render(text, True, color)
    surface.blit(render, pos)

def draw_rules(surface, font_small, elapsed_seconds: int, paused: bool):
    rule_text = "Rules: Fill 1–9 uniquely in each row, column, and 3×3 box. Use Roman numerals I–IX."
    hint_text = "Controls: Click cell; 1–9 or Roman I/V/X; H=Hint, R=Reshuffle, P=Pause, Q=Quit, Del=Clear"
    status_text = f"Time: {elapsed_seconds:4d}s  {'[PAUSED]' if paused else ''}"
    draw_text(surface, rule_text, font_small, BLACK, (MARGIN, 10))
    draw_text(surface, hint_text, font_small, BLACK, (MARGIN, 30))
    draw_text(surface, status_text, font_small, BLACK, (MARGIN, 55))

def draw_grid(surface, font_cell, board, selected: Tuple[int, int] | None):
    # Background
    surface.fill(WHITE)
    # Rules
    # Drawn by caller
    # Grid lines
    offset_x = MARGIN
    offset_y = TOP_BAR
    for r in range(10):
        thick = 4 if r % 3 == 0 else 1
        pygame.draw.line(surface, GRID, (offset_x, offset_y + r * CELL_SIZE),
                         (offset_x + 9 * CELL_SIZE, offset_y + r * CELL_SIZE), thick)
    for c in range(10):
        thick = 4 if c % 3 == 0 else 1
        pygame.draw.line(surface, GRID, (offset_x + c * CELL_SIZE, offset_y),
                         (offset_x + c * CELL_SIZE, offset_y + 9 * CELL_SIZE), thick)

    # Cells and numbers
    for r in range(9):
        for c in range(9):
            x = offset_x + c * CELL_SIZE
            y = offset_y + r * CELL_SIZE
            rect = pygame.Rect(x + 1, y + 1, CELL_SIZE - 2, CELL_SIZE - 2)

            # Highlight selection
            if selected and selected == (r, c):
                pygame.draw.rect(surface, YELLOW, rect)

            val = board.user[r][c]
            shown_val = board.permute_symbol(val)
            if val != 0:
                roman = int_to_roman(shown_val)
                color = BLACK if board.fixed[r][c] else BLUE
                draw_centered_text(surface, roman, font_cell, color, rect.center)
            else:
                # subtle empty cell
                pygame.draw.rect(surface, (252, 252, 252), rect)

            # Conflicts
            if val != 0 and not board.fixed[r][c]:
                if board.get_conflicts(r, c):
                    pygame.draw.rect(surface, RED, rect, 3)

def draw_centered_text(surface, text, font, color, center):
    render = font.render(text, True, color)
    rect = render.get_rect(center=center)
    surface.blit(render, rect.topleft)
