def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    ranges = {
        "Easy": (1, 20),
        "Normal": (1, 100),
        "Hard": (1, 50),
    }
    return ranges.get(difficulty, (1, 100))


def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None:
        return False, None, "Enter a guess."

    cleaned = str(raw).strip()
    if cleaned == "":
        return False, None, "Enter a guess."

    try:
        guess = int(cleaned)
    except ValueError:
        return False, None, "That is not a whole number."

    return True, guess, None


def check_guess(guess, secret, include_message: bool = False):
    """
    Compare guess to secret and return (outcome, message).

    outcome examples: "Win", "Too High", "Too Low"
    """
    if guess == secret:
        outcome = "Win"
    elif guess > secret:
        outcome = "Too High"
    else:
        outcome = "Too Low"

    if include_message:
        return outcome, feedback_message(outcome)
    return outcome


def feedback_message(outcome: str):
    messages = {
        "Win": "Correct! You found the secret number.",
        "Too High": "Too high. Try a lower number.",
        "Too Low": "Too low. Try a higher number.",
    }
    return messages.get(outcome, "")


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    if outcome == "Win":
        points = max(10, 100 - 10 * (attempt_number - 1))
        return current_score + points

    if outcome in {"Too High", "Too Low"}:
        return max(0, current_score - 5)

    return current_score
