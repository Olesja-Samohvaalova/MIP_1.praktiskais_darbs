from __future__ import annotations

import random
import tkinter as tk
from tkinter import messagebox
from typing import List

from engine import GameState, legal_moves, apply_move, is_terminal, final_result
from ai_player import choose_move


def generate_start_numbers(k: int = 5, low: int = 40000, high: int = 50000) -> List[int]:
    result = set()
    while len(result) < k:
        x = random.randint(low, high)
        x -= x % 60
        if low <= x <= high and x % 60 == 0:
            result.add(x)
    return sorted(result)


class GameGUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Dalīšanas spēle (3/4/5) — Cilvēks vs AI")
        self.root.geometry("700x440")
        self.root.minsize(700, 440)

        self.state: GameState | None = None
        self.algorithm = tk.StringVar(value="alphabeta")
        self.depth = tk.IntVar(value=6)

        tk.Label(root, text="Dalīšanas spēle: dalīt ar 3 / 4 / 5", font=("Arial", 16, "bold")).pack(pady=10)

        main = tk.Frame(root)
        main.pack(fill="both", expand=True, padx=12, pady=8)

        left = tk.Frame(main)
        left.pack(side="left", fill="both", expand=True, padx=(0, 10))

        right = tk.Frame(main)
        right.pack(side="right", fill="y")

        # --- Starta skaitļi (listbox) ---
        tk.Label(left, text="1) Izvēlies sākuma skaitli:", font=("Arial", 12, "bold")).pack(anchor="w")
        self.start_list = tk.Listbox(left, height=6, font=("Consolas", 12))
        self.start_list.pack(fill="x", pady=6)

        btnrow = tk.Frame(left)
        btnrow.pack(anchor="w", pady=(0, 6))
        tk.Button(btnrow, text="Ģenerēt 5 skaitļus", command=self.on_generate).pack(side="left", padx=(0, 6))
        tk.Button(btnrow, text="Sākt ar izvēlēto", command=self.on_start).pack(side="left")

        # --- AI iestatījumi (minimāli, bet “vizuāli elementi” ir) ---
        tk.Label(left, text="2) AI iestatījumi:", font=("Arial", 12, "bold")).pack(anchor="w", pady=(12, 0))
        algrow = tk.Frame(left)
        algrow.pack(anchor="w", pady=4)
        tk.Label(algrow, text="Algoritms:").pack(side="left")
        tk.Radiobutton(algrow, text="minimax", variable=self.algorithm, value="minimax").pack(side="left", padx=6)
        tk.Radiobutton(algrow, text="alphabeta", variable=self.algorithm, value="alphabeta").pack(side="left", padx=6)

        drow = tk.Frame(left)
        drow.pack(anchor="w", pady=4)
        tk.Label(drow, text="Dziļums:").pack(side="left")
        tk.Spinbox(drow, from_=1, to=12, textvariable=self.depth, width=5).pack(side="left", padx=6)

        # --- Status / info panelis ---
        tk.Label(left, text="3) Spēles stāvoklis:", font=("Arial", 12, "bold")).pack(anchor="w", pady=(12, 0))

        self.status = tk.StringVar(value="Spied “Ģenerēt 5 skaitļus”, izvēlies un sāc.")
        tk.Label(left, textvariable=self.status, anchor="w", justify="left").pack(fill="x", pady=6)

        self.n_var = tk.StringVar(value="-")
        self.score_var = tk.StringVar(value="-")
        self.bank_var = tk.StringVar(value="-")
        self.turn_var = tk.StringVar(value="-")
        self.moves_var = tk.StringVar(value="-")

        self._kv(left, "Skaitlis:", self.n_var)
        self._kv(left, "Punkti:", self.score_var)
        self._kv(left, "Banka:", self.bank_var)
        self._kv(left, "Gājiens:", self.turn_var)
        self._kv(left, "Pieejamie dalītāji:", self.moves_var)

        # --- Gājienu pogas ---
        tk.Label(right, text="Gājiens", font=("Arial", 12, "bold")).pack(pady=(0, 8))

        self.btn3 = tk.Button(right, text="Dalīt ar 3", width=18, command=lambda: self.on_human_move(3))
        self.btn4 = tk.Button(right, text="Dalīt ar 4", width=18, command=lambda: self.on_human_move(4))
        self.btn5 = tk.Button(right, text="Dalīt ar 5", width=18, command=lambda: self.on_human_move(5))
        self.btn3.pack(pady=4)
        self.btn4.pack(pady=4)
        self.btn5.pack(pady=4)

        tk.Button(right, text="Reset", width=18, command=self.on_reset).pack(pady=(18, 0))

        self._set_move_buttons(False)
        self.on_generate()

    def _kv(self, parent: tk.Widget, k: str, v: tk.StringVar) -> None:
        row = tk.Frame(parent)
        row.pack(fill="x", pady=2)
        tk.Label(row, text=k, width=18, anchor="w").pack(side="left")
        tk.Label(row, textvariable=v, anchor="w", font=("Consolas", 11)).pack(side="left")

    def _set_move_buttons(self, enabled: bool) -> None:
        s = tk.NORMAL if enabled else tk.DISABLED
        self.btn3.config(state=s)
        self.btn4.config(state=s)
        self.btn5.config(state=s)

    def _refresh(self) -> None:
        if self.state is None:
            self.n_var.set("-"); self.score_var.set("-"); self.bank_var.set("-")
            self.turn_var.set("-"); self.moves_var.set("-")
            self._set_move_buttons(False)
            return

        moves = legal_moves(self.state)
        self.n_var.set(str(self.state.n))
        self.score_var.set(str(self.state.score))
        self.bank_var.set(str(self.state.bank))
        self.turn_var.set("Cilvēks" if self.state.turn == 0 else "AI")
        self.moves_var.set(", ".join(map(str, moves)) if moves else "nav")

        # aktivizē tikai cilvēka gājienā un tikai legālos
        if self.state.turn == 0 and moves:
            self._set_move_buttons(True)
            self.btn3.config(state=(tk.NORMAL if 3 in moves else tk.DISABLED))
            self.btn4.config(state=(tk.NORMAL if 4 in moves else tk.DISABLED))
            self.btn5.config(state=(tk.NORMAL if 5 in moves else tk.DISABLED))
        else:
            self._set_move_buttons(False)

    def on_generate(self) -> None:
        self.start_list.delete(0, tk.END)
        for x in generate_start_numbers():
            self.start_list.insert(tk.END, str(x))
        self.state = None
        self.status.set("Izvēlies sākuma skaitli un spied “Sākt ar izvēlēto”.")
        self._refresh()

    def on_start(self) -> None:
        sel = self.start_list.curselection()
        if not sel:
            messagebox.showwarning("Nav izvēles", "Izvēlies vienu sākuma skaitli sarakstā.")
            return
        start_n = int(self.start_list.get(sel[0]))
        self.state = GameState(n=start_n, score=0, bank=0, turn=0)
        self.status.set("Spēle sākta. Tavs gājiens.")
        self._refresh()

    def on_human_move(self, move: int) -> None:
        if self.state is None or self.state.turn != 0:
            return
        if move not in legal_moves(self.state):
            messagebox.showerror("Nederīgs gājiens", "Šobrīd ar šo dalītāju dalīt nedrīkst.")
            return

        self.state = apply_move(self.state, move)
        self.status.set(f"Tu: dalīt ar {move}.")
        self._refresh()

        if self.state and is_terminal(self.state):
            self.finish()
            return

        # AI gājiens ar mazu aizturi, lai UI “dzīvs”
        self.root.after(200, self.do_ai)

    def do_ai(self) -> None:
        if self.state is None or self.state.turn != 1:
            return

        moves = legal_moves(self.state)
        if not moves:
            self.finish()
            return

        alg = self.algorithm.get()
        depth = int(self.depth.get())
        ai_move = choose_move(self.state, algorithm=alg, depth=depth)
        if ai_move not in moves:  # drošībai
            ai_move = moves[0]

        self.state = apply_move(self.state, ai_move)
        self.status.set(f"AI: dalīt ar {ai_move}.")
        self._refresh()

        if self.state and is_terminal(self.state):
            self.finish()

    def finish(self) -> None:
        if self.state is None:
            return
        r = final_result(self.state)
        self._set_move_buttons(False)
        messagebox.showinfo(
            "Spēle beigusies",
            "Spēle beigusies \n\n"
            f"Punkti (pirms bankas): {r['raw_score']}\n"
            f"Banka: {r['bank']}\n"
            f"Gala punkti: {r['final_score']}\n"
            f"Uzvarētājs: {r['winner']}"
        )
        self.status.set("Spēle beigusies. Spied “Ģenerēt 5 skaitļus”, lai sāktu no jauna.")

    def on_reset(self) -> None:
        self.state = None
        self.status.set("Reset. Izvēlies sākuma skaitli un sāc.")
        self._refresh()


def main() -> None:
    root = tk.Tk()
    GameGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
