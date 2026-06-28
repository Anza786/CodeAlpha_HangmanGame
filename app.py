"""
============================================================
  CodeAlpha Hangman Game
  Flask Web Application
  Author  : CodeAlpha Intern
  Version : 1.0
============================================================
"""

from flask import Flask, render_template, request, session, redirect, url_for
import random

app = Flask(__name__)
app.secret_key = "codealpha_hangman_secret"

# ─────────────────────────────────────────────
#  PREDEFINED WORDS LIST
# ─────────────────────────────────────────────
WORDS = [
    {"word": "python",   "hint": "A popular programming language 🐍"},
    {"word": "flask",    "hint": "A Python web framework 🌐"},
    {"word": "github",   "hint": "A platform for hosting code 💻"},
    {"word": "keyboard", "hint": "You type with this ⌨️"},
    {"word": "program",  "hint": "A set of instructions for a computer 📋"},
]

MAX_WRONG = 6


def init_game():
    chosen   = random.choice(WORDS)
    session["word"]          = chosen["word"]
    session["hint"]          = chosen["hint"]
    session["guessed"]       = []
    session["wrong_count"]   = 0
    session["game_status"]   = "playing"  # playing / won / lost


@app.route("/")
def index():
    return render_template("hangman_index.html")


@app.route("/start")
def start():
    init_game()
    return redirect(url_for("game"))


@app.route("/game")
def game():
    if "word" not in session:
        return redirect(url_for("index"))

    word        = session["word"]
    guessed     = session["guessed"]
    wrong_count = session["wrong_count"]
    status      = session["game_status"]
    hint        = session["hint"]

    # Build display word  e.g. "_ y t _ _ n"
    display = [letter if letter in guessed else "_" for letter in word]

    # Wrong letters
    wrong_letters = [l for l in guessed if l not in word]

    # Remaining guesses
    remaining = MAX_WRONG - wrong_count

    return render_template(
        "hangman_game.html",
        word        = word,
        display     = display,
        guessed     = guessed,
        wrong_count = wrong_count,
        wrong_letters = wrong_letters,
        remaining   = remaining,
        max_wrong   = MAX_WRONG,
        status      = status,
        hint        = hint,
    )


@app.route("/guess", methods=["POST"])
def guess():
    if "word" not in session or session["game_status"] != "playing":
        return redirect(url_for("game"))

    letter = request.form.get("letter", "").lower().strip()

    # Validate
    if len(letter) != 1 or not letter.isalpha():
        return redirect(url_for("game"))

    word    = session["word"]
    guessed = session["guessed"]

    if letter not in guessed:
        guessed.append(letter)
        session["guessed"] = guessed

        if letter not in word:
            session["wrong_count"] += 1

    wrong_count = session["wrong_count"]

    # Check win
    if all(l in guessed for l in word):
        session["game_status"] = "won"
    # Check loss
    elif wrong_count >= MAX_WRONG:
        session["game_status"] = "lost"

    return redirect(url_for("game"))


if __name__ == "__main__":
    app.run(debug=True)