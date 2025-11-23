"""Test game logic and conflict detection."""
from src.board import SudokuBoard, sample_puzzle


def test_conflict_detection_row():
    """Test conflict detection in rows."""
    puzzle, solution = sample_puzzle()
    board = SudokuBoard(puzzle, solution)
    
    # Set two conflicting values in same row (both must be non-fixed)
    # Row 0: [5, 3, 0, 0, 7, 0, 0, 0, 0] - positions 2 and 3 are non-fixed
    board.set_cell(0, 2, 9)  # First position
    board.set_cell(0, 3, 9)  # Same row, different column, same value
    
    # Should detect conflict
    assert board.get_conflicts(0, 2), "Should detect row conflict"
    assert board.get_conflicts(0, 3), "Should detect row conflict"


def test_conflict_detection_column():
    """Test conflict detection in columns."""
    puzzle, solution = sample_puzzle()
    board = SudokuBoard(puzzle, solution)
    
    # Set two conflicting values in same column (use column 2 which has non-fixed cells)
    # Column 2: [0, 0, 8, 0, 0, 0, 0, 0, 0] - positions 0, 1, 3, 4, 5, 6, 7, 8 are non-fixed
    board.set_cell(0, 2, 9)  # First position
    board.set_cell(1, 2, 9)  # Same column, different row, same value
    
    # Should detect conflict
    assert board.get_conflicts(0, 2), "Should detect column conflict"
    assert board.get_conflicts(1, 2), "Should detect column conflict"


def test_conflict_detection_box():
    """Test conflict detection in 3x3 boxes."""
    puzzle, solution = sample_puzzle()
    board = SudokuBoard(puzzle, solution)
    
    # Set two conflicting values in same 3x3 box
    board.set_cell(3, 3, 3)  # Center box, first position
    board.set_cell(4, 4, 3)  # Center box, different position, same value
    
    # Should detect conflict
    assert board.get_conflicts(3, 3), "Should detect box conflict"
    assert board.get_conflicts(4, 4), "Should detect box conflict"


def test_no_conflict_valid_placement():
    """Test that valid placements don't show conflicts."""
    puzzle, solution = sample_puzzle()
    board = SudokuBoard(puzzle, solution)
    
    # Place the correct value from the solution
    if not board.fixed[0][2]:
        correct_value = solution[0][2]
        board.set_cell(0, 2, correct_value)
        
        # Should not show conflict for correct placement
        assert not board.get_conflicts(0, 2), "Should not detect conflict for valid placement"


def test_hint_provides_correct_value():
    """Test that hints provide the correct solution value."""
    puzzle, solution = sample_puzzle()
    board = SudokuBoard(puzzle, solution)
    
    # Get a hint
    hint = board.get_hint_cell()
    assert hint is not None, "Should provide a hint"
    
    r, c, value = hint
    # Hint should match solution
    assert value == solution[r][c], "Hint should provide correct solution value"


def test_completion_detection():
    """Test that completion is correctly detected."""
    puzzle, solution = sample_puzzle()
    board = SudokuBoard(puzzle, solution)
    
    # Initially not complete
    assert not board.is_complete(), "Board should not be complete initially"
    
    # Fill in all cells with solution
    for r in range(9):
        for c in range(9):
            if not board.fixed[r][c]:
                board.set_cell(r, c, solution[r][c])
    
    # Now should be complete
    assert board.is_complete(), "Board should be complete after filling all cells correctly"


def test_fixed_cells_cannot_be_changed():
    """Test that fixed cells (puzzle givens) cannot be modified."""
    puzzle, solution = sample_puzzle()
    board = SudokuBoard(puzzle, solution)
    
    # Find a fixed cell
    for r in range(9):
        for c in range(9):
            if board.fixed[r][c]:
                original_value = board.user[r][c]
                
                # Try to change it
                board.set_cell(r, c, 9 if original_value != 9 else 1)
                
                # Should remain unchanged
                assert board.user[r][c] == original_value, \
                    "Fixed cells should not be modifiable"
                return
    
    # If we get here, there were no fixed cells, which should not happen
    assert False, "Puzzle should have at least one fixed cell"


def test_clear_cell():
    """Test that clearing cells works correctly."""
    puzzle, solution = sample_puzzle()
    board = SudokuBoard(puzzle, solution)
    
    # Find a non-fixed cell and set a value
    for r in range(9):
        for c in range(9):
            if not board.fixed[r][c]:
                board.set_cell(r, c, 5)
                assert board.user[r][c] == 5, "Cell should be set to 5"
                
                # Clear it
                board.clear_cell(r, c)
                assert board.user[r][c] == 0, "Cell should be cleared to 0"
                return
    
    # If we get here, there were no non-fixed cells
    assert False, "Puzzle should have at least one non-fixed cell"
