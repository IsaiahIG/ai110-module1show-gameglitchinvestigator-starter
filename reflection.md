# Reflection: Game Glitch Investigator

## 1. What was broken when you started?

The game's purpose is to let the player guess a secret number, get accurate higher or lower feedback, and either win before the attempts run out or lose cleanly. When I started, the helper functions had not actually been moved into `logic_utils.py`, so the app logic was tangled inside `app.py`. I also found that the hint text was backwards, the app sometimes mixed string and integer comparisons, and the reset behavior did not consistently match the selected difficulty. Those issues made the game feel unreliable even when the UI still loaded.

## 2. How did you use AI as a teammate?

I used AI as a debugging partner to think through Streamlit reruns and how session state should be used to keep the secret number from changing unexpectedly between interactions. One suggestion that was correct was to initialize game values in `st.session_state` and only reset them when starting a new game or changing difficulty, and I verified that by tracing the rerun flow in the app. One misleading part came from the original AI-generated code itself, which reversed the hint messages and sometimes converted the secret value to a string before comparing it. I verified that was wrong by reading the comparison logic and then checking the corrected outcomes with tests.

## 3. Debugging and testing your fixes

I treated a bug as fixed only when both the code path made sense and the tests passed. I moved the pure logic into `logic_utils.py`, added a small `conftest.py` so `pytest` could import the module reliably, and then ran `python -m pytest` to verify the win, too-high, and too-low cases. I also reviewed the app flow to make sure the number is stored in session state, the attempts counter behaves correctly, and the range shown in the UI matches the selected difficulty. AI helped explain the rerun model, but the final proof came from the tests and code review.

## 4. What did you learn about Streamlit and state?

Streamlit reruns the whole script every time the user clicks a button or changes a widget, so plain Python variables do not automatically persist across interactions. `st.session_state` is what lets the app remember things like the secret number, attempts, score, and whether the game is over. I would explain it to a friend by saying that Streamlit redraws the app over and over, and session state is the memory that survives each redraw. Once I understood that, the state bug was much easier to reason about.

## 5. Looking ahead: your developer habits

One habit I want to reuse is separating game logic from UI code early, because that made the bugs easier to test and fix. Next time I work with AI on a coding task, I want to ask for smaller pieces and verify each piece sooner instead of trusting one big generated file. This project changed how I think about AI-generated code because it showed me that code can look polished while still hiding simple but important logic errors. AI can speed up the work, but I still need tests, careful reading, and my own judgment.
