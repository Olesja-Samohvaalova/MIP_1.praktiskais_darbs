from __future__ import annotations

try:
    from engine import GameState, legal_moves, apply_move, is_terminal, final_result
except Exception:
    from main import GameState, legal_moves, apply_move, is_terminal, final_result


def vertiba(state: GameState) -> int:
    # ja spēle beigusies
    if is_terminal(state):
        rez = final_result(state)
        if "AI" in rez["winner"]:
            return 1000
        return -1000

    # aptuvens stāvokļa vērtējums
    gala = state.score - state.bank if state.score % 2 == 0 else state.score + state.bank
    v = 0

    # AI grib sev labu gala rezultātu
    if gala % 2 == 1:
        v += 10
    else:
        v -= 10

    # banka ir neliels bonuss
    v += state.bank

    # mazāk gājienu = tuvāk beigām
    if len(legal_moves(state)) == 1:
        v += 1

    return v


def minimax(state: GameState, depth: int, maximizing: bool):
    # apstājas pie dziļuma vai beigām
    if depth == 0 or is_terminal(state):
        return vertiba(state), None

    gajieni = legal_moves(state)

    if maximizing:
        best_value = float("-inf")
        best_move = None

        for g in gajieni:
            child = apply_move(state, g)
            value, _ = minimax(child, depth - 1, False)

            if value > best_value:
                best_value = value
                best_move = g

        return best_value, best_move

    best_value = float("inf")
    best_move = None

    for g in gajieni:
        child = apply_move(state, g)
        value, _ = minimax(child, depth - 1, True)

        if value < best_value:
            best_value = value
            best_move = g

    return best_value, best_move


def alphabeta(state: GameState, depth: int, alpha: float, beta: float, maximizing: bool):
    # tas pats minimax, tikai ar nogriešanu
    if depth == 0 or is_terminal(state):
        return vertiba(state), None

    gajieni = legal_moves(state)

    if maximizing:
        best_value = float("-inf")
        best_move = None

        for g in gajieni:
            child = apply_move(state, g)
            value, _ = alphabeta(child, depth - 1, alpha, beta, False)

            if value > best_value:
                best_value = value
                best_move = g

            alpha = max(alpha, best_value)

            if beta <= alpha:
                break

        return best_value, best_move

    best_value = float("inf")
    best_move = None

    for g in gajieni:
        child = apply_move(state, g)
        value, _ = alphabeta(child, depth - 1, alpha, beta, True)

        if value < best_value:
            best_value = value
            best_move = g

        beta = min(beta, best_value)

        if beta <= alpha:
            break

    return best_value, best_move


def choose_move(state: GameState, algorithm: str = "alphabeta", depth: int = 6) -> int:
    # izvēlas algoritmu
    gajieni = legal_moves(state)

    if algorithm == "minimax":
        _, move = minimax(state, depth, True)
    else:
        _, move = alphabeta(state, depth, float("-inf"), float("inf"), True)

    # ja nav atrasts, paņem pirmo
    if move is None:
        return gajieni[0]

    return move