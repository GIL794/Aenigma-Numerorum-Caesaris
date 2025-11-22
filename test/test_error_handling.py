"""Test error handling in board save/load operations."""
import os
import json
import tempfile
from src.board import SudokuBoard, sample_puzzle


def test_load_with_corrupted_save():
    """Test that corrupted save files are handled gracefully."""
    # Create a temporary corrupted save file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        temp_file = f.name
        f.write("{ corrupted json content }")
    
    try:
        # Temporarily replace SAVE_FILE constant
        import src.board
        original_save_file = src.board.SAVE_FILE
        src.board.SAVE_FILE = temp_file
        
        # Should return None on corrupted file
        board = SudokuBoard.load_if_exists()
        assert board is None, "Should return None for corrupted save file"
        
        # Restore original SAVE_FILE
        src.board.SAVE_FILE = original_save_file
    finally:
        # Clean up temp file
        if os.path.exists(temp_file):
            os.remove(temp_file)


def test_load_nonexistent_file():
    """Test that loading nonexistent file returns None."""
    import src.board
    original_save_file = src.board.SAVE_FILE
    src.board.SAVE_FILE = "nonexistent_file_12345.json"
    
    try:
        board = SudokuBoard.load_if_exists()
        assert board is None, "Should return None for nonexistent file"
    finally:
        src.board.SAVE_FILE = original_save_file


def test_save_and_load_roundtrip():
    """Test that save and load work correctly."""
    import src.board
    
    # Use a temporary file for testing
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        temp_file = f.name
    
    original_save_file = src.board.SAVE_FILE
    src.board.SAVE_FILE = temp_file
    
    try:
        # Create a board and make some moves
        puzzle, solution = sample_puzzle()
        board1 = SudokuBoard(puzzle, solution)
        board1.set_cell(0, 2, 4)  # Set a value
        
        # Save the board
        board1.save()
        assert os.path.exists(temp_file), "Save file should be created"
        
        # Load it back
        board2 = SudokuBoard.load_if_exists()
        assert board2 is not None, "Should successfully load saved board"
        assert board2.user[0][2] == 4, "Should preserve user moves"
        
    finally:
        src.board.SAVE_FILE = original_save_file
        if os.path.exists(temp_file):
            os.remove(temp_file)
