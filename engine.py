import random
import chess

# how much each piece is worth
piece_values = {
    chess.PAWN: 1,
    chess.KNIGHT: 3,
    chess.BISHOP: 3,
    chess.ROOK: 5,
    chess.QUEEN: 9,
    chess.KING: 0
}

WIN = 1000


def evaluate(board):
    # positive number = good for white, negative = good for black
    if board.is_checkmate():
        if board.turn == chess.WHITE:
            return -WIN   # white is checkmated
        else:
            return WIN    # black is checkmated

    if board.is_stalemate() or board.is_insufficient_material():
        return 0

    score = 0
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece is not None:
            value = piece_values[piece.piece_type]
            if piece.color == chess.WHITE:
                score += value
            else:
                score -= value
    return score


def _move_order_score(board, move):
    score = 0
    if move.promotion:
        score += 100 + piece_values[move.promotion]
    if board.is_capture(move):
        captured_piece = board.piece_at(move.to_square)
        captured_value = (
            piece_values[chess.PAWN]
            if captured_piece is None
            else piece_values[captured_piece.piece_type]
        )
        attacker = board.piece_at(move.from_square)
        attacker_value = (
            0 if attacker is None else piece_values[attacker.piece_type]
        )
        score += 10 * captured_value - attacker_value
    return score


def _order_moves(board, moves):
    def move_order_key(move):
        return _move_order_score(board, move)

    return sorted(moves, key=move_order_key, reverse=True)


def alphabeta(board, depth, alpha, beta):
    # white tries to maximize the score, black tries to minimize it
    if depth == 0 or board.is_game_over():
        return evaluate(board)

    moves = _order_moves(board, board.legal_moves)

    if board.turn == chess.WHITE:
        best = -10000
        for move in moves:
            board.push(move)
            value = alphabeta(board, depth - 1, alpha, beta)
            board.pop()

            best = max(best, value)
            alpha = max(alpha, best)
            if beta <= alpha:
                break  # prune: black will never let this happen
        return best
    else:
        best = 10000
        for move in moves:
            board.push(move)
            value = alphabeta(board, depth - 1, alpha, beta)
            board.pop()

            best = min(best, value)
            beta = min(beta, best)
            if beta <= alpha:
                break  # prune: white will never let this happen
        return best


def get_best_move(board, depth):
    # try every move and pick the one with the best score for the side to move
    moves = list(board.legal_moves)
    random.shuffle(moves)  # so the engine doesn't always play the same game
    moves = _order_moves(board, moves)

    best_move = None
    alpha = -10000
    beta = 10000
    if board.turn == chess.WHITE:
        best_score = -10000
    else:
        best_score = 10000

    for move in moves:
        board.push(move)
        score = alphabeta(board, depth - 1, alpha, beta)
        board.pop()

        if board.turn == chess.WHITE and score > best_score:
            best_score = score
            best_move = move
            alpha = max(alpha, best_score)
        elif board.turn == chess.BLACK and score < best_score:
            best_score = score
            best_move = move
            beta = min(beta, best_score)

    return best_move
