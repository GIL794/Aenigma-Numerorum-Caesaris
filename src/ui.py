import pygame
import math
from typing import Tuple
from .romannum import int_to_roman

# Roman imperial colors
IMPERIAL_PURPLE = (48, 16, 64)
GOLD = (212, 175, 55)
MARBLE = (245, 245, 245)
BLACK = (20, 20, 20)
GRID = (80, 60, 40)
BLUE = (66, 135, 245)
RED = (200, 70, 70)
GREEN = (70, 160, 90)
GRAY = (180, 180, 180)
YELLOW = (245, 210, 85)
SCROLL = (245, 222, 179)
PILLAR = (210, 200, 180)
CAPITAL = (180, 160, 120)
SHADOW = (80, 60, 40)
WHITE = (255, 255, 255)

CELL_SIZE = 32
GRID_SIZE = CELL_SIZE * 9
MARGIN = 24  # Padding around grid and UI elements
WINDOW_SIZE = GRID_SIZE + 2 * MARGIN  # MARGIN can be 20-30 for padding

WINDOW_WIDTH = WINDOW_SIZE
TOP_BAR = 60  # Top bar for title and decorative elements
RULES_HEIGHT = 90  # Height for rules section
BOTTOM_MARGIN = 20  # Bottom padding
WINDOW_HEIGHT = TOP_BAR + RULES_HEIGHT + GRID_SIZE + BOTTOM_MARGIN  # Total height to fit all elements

def draw_text(surface, text, font, color, pos, shadow=False):
    if shadow:
        shadow_render = font.render(text, True, SHADOW)
        surface.blit(shadow_render, (pos[0]+2, pos[1]+2))
    render = font.render(text, True, color)
    surface.blit(render, pos)

def draw_title(surface, font_title, font_desc, title: str, desc: str, eagle_img=None):
    # Imperial purple background
    pygame.draw.rect(surface, IMPERIAL_PURPLE, (0, 0, WINDOW_WIDTH, TOP_BAR))
    # Laurel wreath drawn separately by draw_animated_laurel for animation
    # SPQR banner
    banner_rect = pygame.Rect(WINDOW_WIDTH//2 - 60, 32, 120, 24)
    pygame.draw.rect(surface, GOLD, banner_rect, border_radius=8)
    spqr_font = font_desc
    spqr_text = "SPQR"
    spqr_x = banner_rect.x + banner_rect.width//2 - spqr_font.size(spqr_text)[0]//2
    draw_text(surface, spqr_text, spqr_font, IMPERIAL_PURPLE, (spqr_x, banner_rect.y+2))
    # Eagle icon (optional) - top right corner
    if eagle_img:
        surface.blit(eagle_img, (WINDOW_WIDTH - MARGIN - 48, 6))

def draw_rules(surface, font_small, elapsed_seconds: int, paused: bool, y_offset: int = 120):
    x_rules = MARGIN
    rule_text = "Rules: Fill 1–9 uniquely in each row, column, and 3×3 box. Use Roman numerals I–IX."
    hint_text = "Controls: Click cell; 1–9 or Roman I/V/X; H=Hint, R=New Game, P=Pause, Q=Quit, Del=Clear"
    mins, secs = divmod(elapsed_seconds, 60)
    status_text = f"Time: {mins:02d}:{secs:02d}  {'[PAUSED]' if paused else ''}"
    lines = [rule_text, hint_text, status_text]
    scroll_height = len(lines) * (font_small.get_height() + 8) + 16
    pygame.draw.rect(surface, SCROLL, (x_rules-12, y_offset-10, WINDOW_WIDTH-2*MARGIN+24, scroll_height), border_radius=18)
    pygame.draw.rect(surface, GOLD, (x_rules-12, y_offset-10, WINDOW_WIDTH-2*MARGIN+24, scroll_height), 3, border_radius=18)
    y = y_offset + 4
    for line in lines:
        draw_text(surface, line, font_small, BLACK, (WINDOW_WIDTH // 2 - font_small.size(line)[0] // 2, y))
        y += font_small.get_height() + 8

def draw_grid(surface, font_cell, board, selected: Tuple[int, int] | None):
    offset_x = MARGIN
    offset_y = TOP_BAR + RULES_HEIGHT
    grid_w = CELL_SIZE * 9
    grid_h = CELL_SIZE * 9

    # Shadow for grid
    pygame.draw.rect(surface, GRAY, (offset_x+8, offset_y+8, grid_w+12, grid_h+12), border_radius=10)

    # Roman pillars with capitals
    pygame.draw.rect(surface, PILLAR, (offset_x-40, offset_y-8, 28, grid_h+16), border_radius=8)
    pygame.draw.rect(surface, PILLAR, (offset_x+grid_w+12, offset_y-8, 28, grid_h+16), border_radius=8)
    pygame.draw.rect(surface, CAPITAL, (offset_x-44, offset_y-18, 36, 18), border_radius=6)
    pygame.draw.rect(surface, CAPITAL, (offset_x+grid_w+8, offset_y-18, 36, 18), border_radius=6)
    pygame.draw.rect(surface, CAPITAL, (offset_x-44, offset_y+grid_h+8, 36, 18), border_radius=6)
    pygame.draw.rect(surface, CAPITAL, (offset_x+grid_w+8, offset_y+grid_h+8, 36, 18), border_radius=6)

    # Gold border for grid
    pygame.draw.rect(surface, GOLD, (offset_x-6, offset_y-6, grid_w+12, grid_h+12), 6, border_radius=10)

    # Grid lines
    for r in range(10):
        thick = 4 if r % 3 == 0 else 2
        pygame.draw.line(surface, GRID, (offset_x, offset_y + r * CELL_SIZE),
                         (offset_x + 9 * CELL_SIZE, offset_y + r * CELL_SIZE), thick)
    for c in range(10):
        thick = 4 if c % 3 == 0 else 2
        pygame.draw.line(surface, GRID, (offset_x + c * CELL_SIZE, offset_y),
                         (offset_x + c * CELL_SIZE, offset_y + 9 * CELL_SIZE), thick)

    # Cells and numbers
    for r in range(9):
        for c in range(9):
            x = offset_x + c * CELL_SIZE
            y = offset_y + r * CELL_SIZE
            rect = pygame.Rect(x + 1, y + 1, CELL_SIZE - 2, CELL_SIZE - 2)

            # Gradient marble cell
            for i in range(CELL_SIZE):
                shade = MARBLE[0] + int(10 * math.sin((i + r + c) / 8))
                pygame.draw.line(surface, (shade, shade, shade), (x+1, y+1+i), (x+CELL_SIZE-2, y+1+i))

            # Highlight selection
            if selected and selected == (r, c):
                pygame.draw.rect(surface, YELLOW, rect, 6, border_radius=8)

            val = board.user[r][c]
            if val != 0:
                roman = int_to_roman(val)
                color = GOLD if board.fixed[r][c] else BLUE
                draw_centered_text(surface, roman, font_cell, color, rect.center, shadow=True, outline=board.fixed[r][c])
            else:
                pygame.draw.rect(surface, MARBLE, rect, border_radius=8)

            # Conflicts
            if val != 0 and not board.fixed[r][c]:
                if board.get_conflicts(r, c):
                    pygame.draw.rect(surface, RED, rect, 6, border_radius=8)

            # Grid overlay for better visibility
            pygame.draw.rect(surface, GRID, rect, 2, border_radius=8)

def draw_centered_text(surface, text, font, color, center, shadow=False, outline=False):
    if shadow:
        shadow_render = font.render(text, True, BLACK)
        rect = shadow_render.get_rect(center=(center[0]+2, center[1]+2))
        surface.blit(shadow_render, rect.topleft)
    render = font.render(text, True, color)
    rect = render.get_rect(center=center)
    surface.blit(render, rect.topleft)
    if outline:
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            outline_render = font.render(text, True, BLACK)
            outline_rect = outline_render.get_rect(center=(center[0]+dx, center[1]+dy))
            surface.blit(outline_render, outline_rect.topleft)

def draw_menu(surface, font_title, font_button, title, desc, show_resume, eagle_img=None, frame=0):
    draw_gradient_background(surface)
    draw_animated_laurel(surface, frame)
    # Eagle icon
    if eagle_img:
        surface.blit(eagle_img, (WINDOW_WIDTH//2 - 24, 30))
    # Title
    draw_text(surface, title, font_title, GOLD, (WINDOW_WIDTH//2 - font_title.size(title)[0]//2, 80), shadow=True)
    # Description (wrapped)
    desc_lines = wrap_text(desc, font_button, WINDOW_WIDTH - 2*MARGIN)
    y = 140
    for line in desc_lines:
        draw_text(surface, line, font_button, MARBLE, (WINDOW_WIDTH//2 - font_button.size(line)[0]//2, y))
        y += font_button.get_height() + 4
    # Buttons
    btn_w, btn_h = 320, 70
    btn_x = WINDOW_WIDTH//2 - btn_w//2
    btn_y = y + 30
    new_rect = pygame.Rect(btn_x, btn_y, btn_w, btn_h)
    draw_gold_button(surface, new_rect, "Start New Game", font_button)
    resume_rect = None
    if show_resume:
        resume_rect = pygame.Rect(btn_x, btn_y+btn_h+40, btn_w, btn_h)
        draw_gold_button(surface, resume_rect, "Resume Previous", font_button)
    return new_rect, resume_rect

def draw_gradient_background(surface):
    for y in range(WINDOW_HEIGHT):
        color = (
            IMPERIAL_PURPLE[0] + int((GOLD[0] - IMPERIAL_PURPLE[0]) * y / WINDOW_HEIGHT),
            IMPERIAL_PURPLE[1] + int((GOLD[1] - IMPERIAL_PURPLE[1]) * y / WINDOW_HEIGHT),
            IMPERIAL_PURPLE[2] + int((GOLD[2] - IMPERIAL_PURPLE[2]) * y / WINDOW_HEIGHT),
        )
        pygame.draw.line(surface, color, (0, y), (WINDOW_WIDTH, y))

def draw_gold_button(surface, rect, text, font, hover=False):
    color = (255, 215, 0) if hover else GOLD
    pygame.draw.rect(surface, color, rect, border_radius=18)
    pygame.draw.rect(surface, (180, 140, 40), rect, 4, border_radius=18)
    draw_text(surface, text, font, IMPERIAL_PURPLE, (rect.x + rect.width // 2 - font.size(text)[0] // 2, rect.y + rect.height // 2 - font.get_height() // 2))

def draw_animated_laurel(surface, frame):
    for i in range(10):
        angle = frame % 360
        x = MARGIN + i*32
        y = 22 + int(4 * math.sin(math.radians(angle + i*36)))
        pygame.draw.ellipse(surface, GOLD, (x, y, 26, 16))
        pygame.draw.ellipse(surface, GOLD, (WINDOW_WIDTH - MARGIN - (i+1)*32, y, 26, 16))

def calculate_window_size(font_title, font_desc, font_button, title, desc):
    title_w, _ = font_title.size(title)
    desc_w, desc_h = font_desc.size(desc)
    btn_w, btn_h = 320, 70
    min_width = max(title_w, desc_w, btn_w) + MARGIN * 2
    min_height = 80 + desc_h + btn_h * 2 + 180  # Title + desc + buttons + margins
    # For grid view, ensure grid fits too
    grid_width = MARGIN * 2 + CELL_SIZE * 9 + 100
    grid_height = TOP_BAR + MARGIN + CELL_SIZE * 9 + MARGIN + 100
    return max(min_width, grid_width), max(min_height, grid_height)

def wrap_text(text, font, max_width):
    words = text.split()
    lines = []
    current = ""
    for word in words:
        test = current + (" " if current else "") + word
        if font.size(test)[0] > max_width:
            if current:
                lines.append(current)
            current = word
        else:
            current = test
    if current:
        lines.append(current)
    return lines

# Adding instruction button and dropdown window
def draw_instructions_button(surface, font, rect, hover=False):
    color = (255, 215, 0) if hover else GOLD
    pygame.draw.rect(surface, color, rect, border_radius=12)
    pygame.draw.rect(surface, (180, 140, 40), rect, 3, border_radius=12)
    draw_text(surface, "INSTRUCTIONES", font, IMPERIAL_PURPLE, (rect.x + rect.width // 2 - font.size("INSTRUCTIONES")[0] // 2, rect.y + rect.height // 2 - font.get_height() // 2))

def get_rules_text():
    rule_text = "Regulae: Omnem numerum Romanum I–IX in singulis ordinibus, columnis, quadratis pone."
    hint_text = "Claves: Cellulam selige; 1–9 aut Romanum I/V/X; H=Auxilium, R=Novum Ludum, P=Intermissio, Q=Exire, Del=Dele."
    return [rule_text, hint_text]

def get_rules_text_english():
    rule_text_en = "Rules: Fill each row, column, and 3x3 box with Roman numerals I–IX."
    hint_text_en = "Controls: Select a cell; enter 1–9 or Roman I/V/X; H=Hint, R=New Game, P=Pause, Q=Quit, Del=Clear."
    return [rule_text_en, hint_text_en]

def draw_instructions_dropdown(surface, font, rect):
    rules = get_rules_text()
    rules_en = get_rules_text_english()
    pygame.draw.rect(surface, SCROLL, rect, border_radius=18)
    pygame.draw.rect(surface, GOLD, rect, 3, border_radius=18)
    y = rect.y + 12
    for line in rules:
        draw_text(surface, line, font, BLACK, (rect.x + 20, y))
        y += font.get_height() + 6
    y += 8
    for line in rules_en:
        draw_text(surface, line, font, GRAY, (rect.x + 20, y))
        y += font.get_height() - 4
