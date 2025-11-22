"""Test error handling in board save/load operations."""
import os
import json
import tempfile
import unittest.mock as mock
from src.board import SudokuBoard, sample_puzzle, SAVE_FILE


def test_load_with_corrupted_save():
    """Test that corrupted save files are handled gracefully."""
    # Create a temporary corrupted save file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        temp_file = f.name
        f.write("{ corrupted json content }")
    
    try:
        # Use mock to patch SAVE_FILE
        with mock.patch('src.board.SAVE_FILE', temp_file):
            # Should return None on corrupted file
            board = SudokuBoard.load_if_exists()
            assert board is None, "Should return None for corrupted save file"
    finally:
        # Clean up temp file
        if os.path.exists(temp_file):
            os.remove(temp_file)


def test_load_nonexistent_file():
    """Test that loading nonexistent file returns None."""
    # Use mock to patch SAVE_FILE with a nonexistent file
    with mock.patch('src.board.SAVE_FILE', "nonexistent_file_12345.json"):
        board = SudokuBoard.load_if_exists()
        assert board is None, "Should return None for nonexistent file"


def test_save_and_load_roundtrip():
    """Test that save and load work correctly."""
    # Use a temporary file for testing
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        temp_file = f.name
    
    try:
        # Use mock to patch SAVE_FILE for both save and load
        with mock.patch('src.board.SAVE_FILE', temp_file):
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
        if os.path.exists(temp_file):
            os.remove(temp_file)
