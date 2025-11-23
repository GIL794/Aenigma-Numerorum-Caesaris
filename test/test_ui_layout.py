"""Test UI layout and window dimensions to ensure professional rendering."""
from src.ui import (WINDOW_WIDTH, WINDOW_HEIGHT, TOP_BAR, RULES_HEIGHT, 
                     BOTTOM_MARGIN, CELL_SIZE, MARGIN)


def test_window_dimensions():
    """Verify that window dimensions are properly calculated."""
    # Grid should be 9x9 cells
    grid_height = CELL_SIZE * 9
    
    # Total height should accommodate all elements
    expected_height = TOP_BAR + RULES_HEIGHT + grid_height + BOTTOM_MARGIN
    
    assert WINDOW_HEIGHT == expected_height, \
        f"Window height {WINDOW_HEIGHT} should equal {expected_height}"
    
    # Window should be wide enough for grid with margins
    min_width = CELL_SIZE * 9 + 2 * MARGIN
    assert WINDOW_WIDTH >= min_width, \
        f"Window width {WINDOW_WIDTH} should be at least {min_width}"


def test_grid_fits_in_window():
    """Ensure the grid fits within the window boundaries."""
    grid_start_y = TOP_BAR + RULES_HEIGHT
    grid_end_y = grid_start_y + CELL_SIZE * 9
    
    # Grid should not exceed window height
    assert grid_end_y <= WINDOW_HEIGHT, \
        f"Grid end {grid_end_y} exceeds window height {WINDOW_HEIGHT}"
    
    # Grid should start below top bar and rules
    assert grid_start_y >= TOP_BAR, \
        f"Grid start {grid_start_y} should be below top bar {TOP_BAR}"


def test_layout_constants():
    """Verify layout constants are reasonable."""
    assert TOP_BAR > 0, "TOP_BAR should be positive"
    assert RULES_HEIGHT > 0, "RULES_HEIGHT should be positive"
    assert BOTTOM_MARGIN >= 0, "BOTTOM_MARGIN should be non-negative"
    assert CELL_SIZE > 20, "CELL_SIZE should be large enough to be readable"
    assert MARGIN > 0, "MARGIN should be positive"
