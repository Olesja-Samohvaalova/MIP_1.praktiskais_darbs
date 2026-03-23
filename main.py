from __future__ import annotations
import random
from dataclasses import dataclass
from typing import List, Optional

try:
    from engine import GameState, legal_moves, apply_move, is_terminal, final_result
except Exception:
    # sis ir pagaidu engine
    @dataclass(frozen=True)
    class GameState:
        n: int
        score: int = 0
        bank: int = 0
        turn: int = 0  # 0=cilvēks, 1=AI

    def legal_moves(state: GameState) -> List[int]:
        return [d for d in (3, 4, 5) if state.n % d == 0]

    def apply_move(state: GameState, move: int) -> GameState:
        new_n = state.n // move
        new_score = state.score + (1 if new_n % 2 == 0 else -1)
        new_bank = state.bank + (1 if (new_n % 10 == 0 or new_n % 10 == 5) else 0)
        return GameState(n=new_n, score=new_score, bank=new_bank, turn=1 - state.turn)

    def is_terminal(state: GameState) -> bool:
        return len(legal_moves(state)) == 0

    def final_result(state: GameState) -> dict:
        corrected = state.score - state.bank if state.score % 2 == 0 else state.score + state.bank
        winner = "CILVĒKS (1. spēlētājs)" if corrected % 2 == 0 else "AI (2. spēlētājs)"
        return {"raw_score": state.score, "bank": state.bank, "final_score": corrected, "winner": winner}

try:
    from ai_player import choose_move
except Exception:
    # sis ir pagaidu AI, te jāieliek tas kurs taisa ai
    def choose_move(state: GameState) -> int:
        return random.choice(legal_moves(state))


def generate_start_numbers(k: int = 5, low: int = 40000, high: int = 50000) -> List[int]:
    result = set()
    while len(result) < k:
        x = random.randint(low, high)
        x -= x % 60  
        if low <= x <= high and x % 60 == 0:
            result.add(x)
    return sorted(result)


def render(state: GameState) -> None:
    print("\n" + "=" * 48)
    print(f"Pašreizējais skaitlis: {state.n}")
    print(f"Punkti (kopā):        {state.score}")
    print(f"Banka:                {state.bank}")
    print(f"Gājiens:              {'CILVĒKS' if state.turn == 0 else 'AI'}")
    moves = legal_moves(state)
    print(f"Pieejamie dalītāji:   {moves if moves else 'nav (spēle beidzas)'}")
    print("=" * 48)


def ask_human_move(state: GameState) -> int:
    moves = legal_moves(state)
    while True:
        raw = input(f"Izvēlies dalītāju {moves} (3/4/5): ").strip()
        if not raw.isdigit():
            print("Ievadi skaitli (3/4/5).")
            continue
        m = int(raw)
        if m not in moves:
            print("Nederīgs gājiens.")
            continue
        return m


def main() -> None:
    print("Spēle: dalīšana ar 3/4/5 (Cilvēks vs AI)\n")

    start_nums = generate_start_numbers()
    print("Sākuma skaitļi (izvēlies vienu):")
    for i, x in enumerate(start_nums, start=1):
        print(f"  {i}) {x}")

    choice: Optional[int] = None
    while choice is None:
        raw = input(f"Ievadi izvēli (1-{len(start_nums)}): ").strip()
        if raw.isdigit() and 1 <= int(raw) <= len(start_nums):
            choice = int(raw)
        else:
            print("Nepareiza izvēle.")

    state = GameState(n=start_nums[choice - 1], score=0, bank=0, turn=0)

    while not is_terminal(state):
        render(state)
        if state.turn == 0:
            state = apply_move(state, ask_human_move(state))
        else:
            m = choose_move(state)
            print(f"AI izvēlējās: {m}")
            state = apply_move(state, m)

    render(state)
    r = final_result(state)
    print("\nSPĒLE BEIGUSIES ")
    print(f"Punkti (pirms bankas): {r['raw_score']}")
    print(f"Banka:                 {r['bank']}")
    print(f"Gala punkti:           {r['final_score']}")
    print(f"Uzvarētājs:            {r['winner']}")


if __name__ == "__main__":
    main()
