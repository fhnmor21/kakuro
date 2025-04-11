import argparse
import sys
from kakuro.generator import Board, boardRow, boardCol

def print_ascii_board(board_obj):
    """Prints the Kakuro board using ASCII characters."""
    board_data = board_obj.b # Access the raw board data
    rows = board_obj.br
    cols = board_obj.bc

    # Determine cell width based on max clue value or number length
    max_clue = 0
    for r in range(rows):
        for c in range(cols):
            cell = board_data[r][c]
            if isinstance(cell, tuple): # Clue cell (B, R)
                max_clue = max(max_clue, cell[0] if cell[0] != -1 else 0)
                max_clue = max(max_clue, cell[1] if cell[1] != -1 else 0)
            # No need to check number cells as they are 0 in the start board

    # Cell width needs space for '\', two clues, and padding
    # Example: \12|23
    cell_width = len(str(max_clue)) * 2 + 3 # Adjust as needed for aesthetics
    if cell_width < 5: # Minimum width for number cells like ' 9 '
        cell_width = 5

    border = "+" + ("-" * cell_width + "+") * cols
    print(border)

    for r in range(rows):
        row_str = "|"
        for c in range(cols):
            cell = board_data[r][c]
            cell_content = ""
            if cell == -1: # Block cell
                cell_content = "#" * cell_width
            elif isinstance(cell, tuple): # Clue cell (B, R)
                b_clue = str(cell[0]) if cell[0] != -1 else ""
                r_clue = str(cell[1]) if cell[1] != -1 else ""
                # Format: \B|R padded to cell_width
                clue_str = f"\\{b_clue}|{r_clue}"
                cell_content = clue_str.ljust(cell_width)
            elif isinstance(cell, int) and cell == 0: # Empty number cell
                cell_content = " " * cell_width
            else: # Should not happen in start board, but handle anyway
                cell_content = str(cell).center(cell_width)

            row_str += cell_content + "|"
        print(row_str)
        print(border)

def main():
    parser = argparse.ArgumentParser(description="Generate a Kakuro puzzle.")
    parser.add_argument(
        "--rows",
        type=int,
        default=boardRow, # Default from generator.py
        help=f"Number of rows for the puzzle (default: {boardRow})",
    )
    parser.add_argument(
        "--cols",
        type=int,
        default=boardCol, # Default from generator.py
        help=f"Number of columns for the puzzle (default: {boardCol})",
    )
    args = parser.parse_args()

    print(f"Generating a {args.rows}x{args.cols} Kakuro puzzle...")
    print("(This may take a moment as it verifies the solution)...")

    try:
        # Generate the solved board first (includes verification)
        # The generator function itself might print "Random start runs" etc.
        generated_board_solved = Board.generator(args.rows, args.cols)

        # Get the board state with clues but empty cells (0)
        start_board = generated_board_solved.getStartBoard()

        print("\nGenerated Kakuro Puzzle:")
        print_ascii_board(start_board)

    except Exception as e:
        print(f"\nAn error occurred during generation: {e}", file=sys.stderr)
        # Potentially add more specific error handling if needed
        # For example, the generator might fail if dimensions are too small

if __name__ == "__main__":
    main()
