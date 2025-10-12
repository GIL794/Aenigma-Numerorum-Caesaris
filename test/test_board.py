from src.board import SudokuBoard, sample_puzzle

def test_completion():
    p, s = sample_puzzle()
    b = SudokuBoard(p, s)
    # Fill with solution
    for r in range(9):
        for c in range(9):
            if not b.fixed[r][c]:
                b.set_cell(r, c, s[r][c])
    assert b.is_complete()
