import chess


piece_values = {
    chess.PAWN: 1,
    chess.KNIGHT: 3,
    chess.BISHOP: 3,
    chess.ROOK: 5,
    chess.QUEEN: 9,
    chess.KING: 0,
}
WIN = 1000


def evaluate(board):
    if board.is_checkmate():
        return -WIN if board.turn == chess.WHITE else WIN
    if board.is_game_over(claim_draw=True):
        return 0

    score = 0
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece is not None:
            value = piece_values[piece.piece_type]
            score += value if piece.color == chess.WHITE else -value
    return score


def minimax(board, depth):
    if depth <= 0 or board.is_game_over(claim_draw=True):
        return evaluate(board)

    scores = []
    for move in board.legal_moves:
        board.push(move)
        scores.append(minimax(board, depth - 1))
        board.pop()
    return max(scores) if board.turn == chess.WHITE else min(scores)


def get_best_move(board, depth):
    moves = list(board.legal_moves)
    if not moves:
        return None

    best_move = None
    best_score = float("-inf") if board.turn == chess.WHITE else float("inf")
    for move in moves:
        board.push(move)
        score = minimax(board, depth - 1)
        board.pop()
        if board.turn == chess.WHITE and score > best_score:
            best_score = score
            best_move = move
        elif board.turn == chess.BLACK and score < best_score:
            best_score = score
            best_move = move
    return best_move
