import chess


def print_board(board):
    print()
    border = "  +" + "---+" * 8
    print(border)
    for rank in range(7, -1, -1):
        line = str(rank + 1) + " |"
        for file in range(8):
            piece = board.piece_at(chess.square(file, rank))
            symbol = " " if piece is None else piece.symbol()
            line += f" {symbol} |"
        print(line)
        print(border)
    print("    a   b   c   d   e   f   g   h")
    print("(uppercase = White, lowercase = Black)\n")


def main():
    print_board(chess.Board())


if __name__ == "__main__":
    main()
