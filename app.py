import random

import streamlit as st

from logic_utils import check_guess, get_range_for_difficulty, parse_guess, update_score


def reset_game(difficulty: str, score: int = 0):
    low, high = get_range_for_difficulty(difficulty)
    st.session_state.secret = random.randint(low, high)
    st.session_state.attempts = 0
    st.session_state.score = score
    st.session_state.status = "playing"
    st.session_state.history = []
    st.session_state.last_difficulty = difficulty


def history_rows(secret: int):
    rows = []
    for index, guess in enumerate(st.session_state.history, start=1):
        rows.append(
            {
                "Attempt": index,
                "Guess": guess,
                "Result": check_guess(guess, secret),
            }
        )
    return rows


st.set_page_config(page_title="Glitchy Guesser", page_icon="GG", layout="wide")

st.markdown(
    """
    <style>
    .stApp {
        background:
            radial-gradient(circle at top left, rgba(255, 206, 84, 0.25), transparent 30%),
            radial-gradient(circle at top right, rgba(34, 197, 94, 0.18), transparent 25%),
            linear-gradient(180deg, #f7f2e8 0%, #eef4ef 100%);
    }
    .hero-card, .panel-card, .status-card {
        border-radius: 20px;
        padding: 1.2rem 1.3rem;
        background: rgba(255, 255, 255, 0.84);
        border: 1px solid rgba(25, 25, 25, 0.08);
        box-shadow: 0 14px 40px rgba(36, 39, 44, 0.08);
    }
    .hero-card {
        padding: 1.6rem;
        background: linear-gradient(135deg, rgba(255,255,255,0.95), rgba(255,248,231,0.96));
    }
    .eyebrow {
        text-transform: uppercase;
        letter-spacing: 0.14em;
        font-size: 0.72rem;
        color: #866118;
        font-weight: 700;
    }
    .hero-title {
        font-size: 2.2rem;
        line-height: 1.05;
        font-weight: 800;
        color: #1f2937;
        margin: 0.35rem 0 0.5rem 0;
    }
    .hero-copy {
        color: #4b5563;
        font-size: 1rem;
        margin: 0;
    }
    .metric-label {
        color: #6b7280;
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 0.35rem;
    }
    .metric-value {
        color: #111827;
        font-size: 1.8rem;
        font-weight: 800;
        line-height: 1;
    }
    .metric-note {
        color: #4b5563;
        font-size: 0.95rem;
        margin-top: 0.4rem;
    }
    .panel-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #1f2937;
        margin-bottom: 0.5rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.sidebar.header("Settings")
difficulty = st.sidebar.selectbox("Difficulty", ["Easy", "Normal", "Hard"], index=1)

attempt_limit_map = {"Easy": 6, "Normal": 8, "Hard": 5}
attempt_limit = attempt_limit_map[difficulty]
low, high = get_range_for_difficulty(difficulty)

if "secret" not in st.session_state:
    reset_game(difficulty)
elif st.session_state.get("last_difficulty") != difficulty:
    reset_game(difficulty, score=st.session_state.get("score", 0))

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

attempts_left = max(0, attempt_limit - st.session_state.attempts)

left_col, right_col = st.columns([1.6, 1], gap="large")

with left_col:
    st.markdown(
        f"""
        <div class="hero-card">
            <div class="eyebrow">Enhanced UI</div>
            <div class="hero-title">Game Glitch Investigator</div>
            <p class="hero-copy">
                Guess the hidden number, use the corrected hints, and beat the bugged AI.
                Your current target range is <strong>{low} to {high}</strong>.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with right_col:
    st.markdown(
        f"""
        <div class="status-card">
            <div class="metric-label">Game Status</div>
            <div class="metric-value">{st.session_state.status.title()}</div>
            <div class="metric-note">Attempts left: {attempts_left}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

metric_1, metric_2, metric_3 = st.columns(3)
with metric_1:
    st.markdown(
        f"""
        <div class="panel-card">
            <div class="metric-label">Difficulty</div>
            <div class="metric-value">{difficulty}</div>
            <div class="metric-note">Range {low}-{high}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with metric_2:
    st.markdown(
        f"""
        <div class="panel-card">
            <div class="metric-label">Score</div>
            <div class="metric-value">{st.session_state.score}</div>
            <div class="metric-note">Higher is better</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with metric_3:
    st.markdown(
        f"""
        <div class="panel-card">
            <div class="metric-label">Attempts Used</div>
            <div class="metric-value">{st.session_state.attempts}</div>
            <div class="metric-note">Limit: {attempt_limit}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

play_col, history_col = st.columns([1.2, 1], gap="large")

with play_col:
    st.markdown('<div class="panel-card">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">Make a guess</div>', unsafe_allow_html=True)
    st.write(f"Enter a whole number between `{low}` and `{high}`.")

    raw_guess = st.text_input("Enter your guess:", key="guess_input")

    col1, col2, col3 = st.columns(3)
    with col1:
        submit = st.button("Submit Guess", use_container_width=True)
    with col2:
        new_game = st.button("New Game", use_container_width=True)
    with col3:
        show_hint = st.checkbox("Show hint", value=True)
    st.markdown("</div>", unsafe_allow_html=True)

with history_col:
    st.markdown('<div class="panel-card">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">Guess history</div>', unsafe_allow_html=True)
    if st.session_state.history:
        st.dataframe(
            history_rows(st.session_state.secret),
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.write("No guesses yet. Start with your best shot.")
    st.markdown("</div>", unsafe_allow_html=True)

with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

if new_game:
    reset_game(difficulty)
    st.success("New game started.")
    st.rerun()

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    st.stop()

if submit:
    ok, guess_int, err = parse_guess(raw_guess)

    if not ok:
        st.error(err)
    elif not low <= guess_int <= high:
        st.error(f"Choose a number between {low} and {high}.")
    else:
        st.session_state.attempts += 1
        st.session_state.history.append(guess_int)

        outcome, message = check_guess(
            guess_int,
            st.session_state.secret,
            include_message=True,
        )

        if show_hint:
            if outcome == "Win":
                st.success(message)
            else:
                st.warning(message)

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.session_state.status = "won"
            st.balloons()
            st.success(
                f"You won. The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}"
            )
        elif st.session_state.attempts >= attempt_limit:
            st.session_state.status = "lost"
            st.error(
                f"Out of attempts. The secret was {st.session_state.secret}. "
                f"Score: {st.session_state.score}"
            )

st.divider()
st.caption("Built by an AI that needed a careful human debugging partner.")
