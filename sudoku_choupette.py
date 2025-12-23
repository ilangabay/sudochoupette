import streamlit as st
import numpy as np
import puzzle_generator
import logging
import json
import os
import random
import glob

logging.getLogger('streamlit').setLevel(logging.ERROR)
st.set_page_config(page_title="SudoChoupette", layout="centered")


SAVE_FILE = "sudochoupette_save.json"
IMAGE_FOLDER = "images"

# Messages
SUCCESS_MESSAGES = ["Ouais ! Super ! Elle est forte", "Bravo Choupette !", "Muscles !", "Mais qu'est-ce qu'elle est fooooorte !"]
ERROR_MESSAGES = ["Pov Choupette", "Oh noooooon", "Pov choupette, elle a besoin d'un bisou", "oh noon, méchant sudoku"]
COMPLETE_ERROR_MESSAGES = ["ohhhhhh! Nooooooon! Poooooooov Choupeeeeettte !", "C'est difficiiiiiiile !", "Recommence Choupette !"]
INCOMPLETE_MESSAGES = ["Non non non ! Pas fini !", "Non, pas fini, bisous ?", "Faut continuer ma gentil Choupette !"]

def save_state(puzzle, current_progress, solution):
    state = {"puzzle": puzzle.tolist(), "current_progress": current_progress.tolist(), "solution": solution.tolist()}
    with open(SAVE_FILE, 'w') as f:
        json.dump(state, f)

def load_state():
    if not os.path.exists(SAVE_FILE):
        return None
    with open(SAVE_FILE, 'r') as f:
        state = json.load(f)
    return np.array(state["puzzle"]), np.array(state["current_progress"]), np.array(state["solution"])

def get_random_image():
    if os.path.exists(IMAGE_FOLDER):
        images = glob.glob(os.path.join(IMAGE_FOLDER, "*.png")) + glob.glob(os.path.join(IMAGE_FOLDER, "*.jpg")) + glob.glob(os.path.join(IMAGE_FOLDER, "*.jpeg"))
        if images:
            return random.choice(images)
    return "https://via.placeholder.com/300x200/00ff00/ffffff?text=Choupette!"

def check_entries_match_solution(current_grid, solution):
    for i in range(9):
        for j in range(9):
            if current_grid[i, j] != 0:
                if current_grid[i, j] != solution[i, j]:
                    return False
    return True

def is_complete_and_correct(current_grid, solution):
    return np.array_equal(current_grid, solution) and np.all(current_grid != 0)

def sudoku(): 
    # Initialize
    if 'initialized' not in st.session_state:
        loaded = load_state()
        if loaded:
            st.session_state.puzzle, st.session_state.current_progress, st.session_state.solution = loaded
        else:
            generator = puzzle_generator.PuzzleGenerator()
            puzzle, solution = generator.generate_sudoku()
            st.session_state.puzzle = np.array(puzzle)
            st.session_state.solution = np.array(solution)
            st.session_state.current_progress = np.array(puzzle)
        st.session_state.initialized = True

    # Initialize all input keys BEFORE creating widgets (moved outside the initialization check)
    for row in range(9):
        for col in range(9):
            if st.session_state.puzzle[row, col] == 0:  # Only for empty cells
                if f"input_{row}_{col}" not in st.session_state:
                    st.session_state[f"input_{row}_{col}"] = str(st.session_state.current_progress[row, col]) if st.session_state.current_progress[row, col] != 0 else ""

    st.title("SudoChoupette")
    # Create grid
    current_grid = np.zeros((9, 9), dtype=int)

    for block_row in range(3):
        for i in range(3):
            row = block_row * 3 + i
            cols = st.columns([1, 1, 1, 0.2, 1, 1, 1, 0.2, 1, 1, 1])
            
            col_idx = 0
            for block_col in range(3):
                for j in range(3):
                    col = block_col * 3 + j
                    with cols[col_idx]:
                        if st.session_state.puzzle[row, col] != 0:
                            st.text_input(f"Cell {row+1}-{col+1}", value=str(st.session_state.puzzle[row, col]),
                                        disabled=True, key=f"given_{row}_{col}", label_visibility="hidden")
                            current_grid[row, col] = st.session_state.puzzle[row, col]
                        else:
                            st.text_input(f"Input {row+1}-{col+1}", key=f"input_{row}_{col}",
                                        label_visibility="hidden", max_chars=1)
                            
                            # Get the value from session state
                            value = st.session_state[f"input_{row}_{col}"]
                            if value.isdigit() and 1 <= int(value) <= 9:
                                current_grid[row, col] = int(value)
                    col_idx += 1
                if block_col < 2:
                    col_idx += 1
        if block_row < 2:
            st.write("")

    # Update progress and save
    st.session_state.current_progress = current_grid.copy()
    save_state(st.session_state.puzzle, st.session_state.current_progress, st.session_state.solution)

    # Buttons
    col_a, col_b, col_c = st.columns([1, 1, 1])

    with col_a:
        if st.button("Vérifier les chiffres", use_container_width=True):
            if check_entries_match_solution(current_grid, st.session_state.solution):
                st.success(random.choice(SUCCESS_MESSAGES))
                st.image(get_random_image())
            else:
                st.error(random.choice(ERROR_MESSAGES))
                st.image(get_random_image())

    with col_b:
        if st.button("J'ai fini", use_container_width=True):
            if np.all(current_grid != 0):
                if is_complete_and_correct(current_grid, st.session_state.solution):
                    st.success("Mais qu'est-ce qu'elle est foooooooorteeee !")
                    st.balloons() 
                    st.image(get_random_image())
                else:
                    st.error(random.choice(COMPLETE_ERROR_MESSAGES))
                    st.image(get_random_image())
            else:
                st.warning(random.choice(INCOMPLETE_MESSAGES))

    with col_c:
        if st.button("Nouvelle Grille de Chaton", use_container_width=True):
            # Set a reset flag instead of modifying widget keys
            st.session_state.reset_grid = True
            keys_to_delete = [key for key in st.session_state.keys() if key.startswith('input_')]
            for key in keys_to_delete:
                del st.session_state[key]
            
            if os.path.exists(SAVE_FILE):  # Replace with your actual filename
                os.remove(SAVE_FILE)
            
            generator = puzzle_generator.PuzzleGenerator()
            puzzle, solution = generator.generate_sudoku()
            st.session_state.puzzle = np.array(puzzle)
            st.session_state.solution = np.array(solution)
            st.session_state.current_progress = np.array(puzzle)
            save_state(st.session_state.puzzle, st.session_state.current_progress, st.session_state.solution)
            st.rerun()
