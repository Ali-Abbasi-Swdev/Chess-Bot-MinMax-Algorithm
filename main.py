import chess
import engine


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


def get_move_from_user(board):
    # keep asking until the user types a legal move
    while True:
        text = input("Enter your move (e.g. e2e4, 'help', or 'quit'): ").strip().lower()

        if text == "quit":
            return None

        if text == "help":
            print("Enter moves as source square + destination square (e.g. e2e4).")
            print("Castling: e1g1/e1c1 for White, e8g8/e8c8 for Black.")
            print("En passant: enter the pawn's capture squares like a normal move (e.g. e5d6).")
            print("Promotion: enter the pawn move (e.g. e7e8), then choose a piece.")
            continue

        try:
            move = chess.Move.from_uci(text)
        except ValueError:
            print("Wrong format. Use a move like e2e4, or type 'help'.")
            continue

        promotion_moves = [
            legal_move
            for legal_move in board.legal_moves
            if legal_move.from_square == move.from_square
            and legal_move.to_square == move.to_square
            and legal_move.promotion is not None
        ]
        if promotion_moves:
            if move.promotion is not None and move in promotion_moves:
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
        else:
            print("That move is not legal, try again.")


def get_promotion_choice():
    promotion_pieces = {
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
        choice = input(
            "Promote to (q)ueen, (r)ook, (b)ishop, or k(n)ight: "
        ).strip().lower()
        if choice == "quit":
            return None
        if choice in promotion_pieces:
            return promotion_pieces[choice]
        print("Choose queen, rook, bishop, knight, or 'quit'.")


def main():
    print("===== MINI CHESS ENGINE =====")
    print("1. Play against the engine")
    print("2. Two players")
    mode = input("Choose mode (1/2): ").strip()

    human_color = chess.WHITE
    depth = 3

    if mode != "2":
        mode = "1"
        side = input("Play as White or Black? (w/b): ").strip().lower()
        if side == "b":
            human_color = chess.BLACK
        while True:
            d = input("Difficulty / search depth (1-10, default 3): ").strip()
            if not d:
                break
            if d in ("1", "2", "3", "4", "5","6", "7", "8", "9", "10"):
                depth = int(d)
                break
            print("Please enter a number from 1 to 10, or press Enter for default 3.")
    else:
        print("Two-player mode: White and Black take turns on the same board.")
        print("Type 'help' during a turn for castling, en passant, and promotion move formats.")

    board = chess.Board()

    while not board.is_game_over():
        print_board(board)

        if board.turn == chess.WHITE:
            print("White to move")
        else:
            print("Black to move")
        if board.is_check():
            print("Check!")

        if mode == "2" or board.turn == human_color:
            move = get_move_from_user(board)
            if move is None:
                print("Game stopped.")
                return
        else:
            print("Engine is thinking...")
            move = engine.get_best_move(board, depth)
            if move.promotion:
                promoted_piece = chess.piece_name(move.promotion).capitalize()
                print(f"Engine plays: {move.uci()} (promotes to {promoted_piece})")
            else:
                print("Engine plays:", move.uci())

        board.push(move)

    # game finished
    print_board(board)
    if board.is_checkmate():
        if board.turn == chess.WHITE:
            print("Checkmate! Black wins.")
        else:
            print("Checkmate! White wins.")
    else:
        print("Game drawn.")


main()
