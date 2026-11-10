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


def get_promotion_choice():
    pieces = {
        "q": chess.QUEEN,
        "queen": chess.QUEEN,
        "r": chess.ROOK,
        "rook": chess.ROOK,
        "b": chess.BISHOP,
        "bishop": chess.BISHOP,
        "n": chess.KNIGHT,
        "knight": chess.KNIGHT,
    }
    while True:
        choice = input("Promote to queen, rook, bishop, or knight: ").strip().lower()
        if choice == "quit":
            return None
        if choice in pieces:
            return pieces[choice]
        print("Choose queen, rook, bishop, knight, or 'quit'.")


def get_move_from_user(board):
    while True:
        text = input(
            "Enter your move (e.g. e2e4, 'help', or 'quit'): "
        ).strip().lower()
        if text == "quit":
            return None
        if text == "help":
            print("Enter moves as source square + destination square (e.g. e2e4).")
            print("Promotion: enter the pawn move (e.g. e7e8), then choose a piece.")
            continue

        try:
            move = chess.Move.from_uci(text)
        except ValueError:
            print("Wrong format. Use a move like e2e4, or type 'help'.")
            continue

        promotions = [
            legal_move
            for legal_move in board.legal_moves
            if legal_move.from_square == move.from_square
            and legal_move.to_square == move.to_square
            and legal_move.promotion is not None
        ]
        if promotions:
            if move in promotions:
                return move
            promotion = get_promotion_choice()
            if promotion is None:
                return None
            return chess.Move(
                move.from_square,
                move.to_square,
                promotion=promotion,
            )
        if move in board.legal_moves:
            return move
        print("That move is not legal, try again.")


def main():
    board = chess.Board()
    print("Two-player chess. White and Black take turns.")
    while not board.is_game_over():
        print_board(board)
        print("White to move" if board.turn == chess.WHITE else "Black to move")
        if board.is_check():
            print("Check!")
        move = get_move_from_user(board)
        if move is None:
            print("Game stopped.")
            return
        board.push(move)

    print_board(board)
    if board.is_checkmate():
        winner = "Black" if board.turn == chess.WHITE else "White"
        print(f"Checkmate! {winner} wins.")
    else:
        print("Game drawn.")


main()
