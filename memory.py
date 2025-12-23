import streamlit as st
import numpy as np
import time
import puzzle_generator
import logging
import json
import os
import random
import glob


IMAGE_FOLDER = "images"
SUCCESS_MESSAGES = ["Ouais ! Super ! Elle est forte", "Bravo Choupette !", "Muscles !", "Mais qu'est-ce qu'elle est fooooorte !"]
ERROR_MESSAGES = ["Pov Choupette", "Oh noooooon", "Pov choupette, elle a besoin d'un bisou", "oh noon, méchant memory"]

def get_images():
    if os.path.exists(IMAGE_FOLDER):
        images = glob.glob(os.path.join(IMAGE_FOLDER, "*.png")) + glob.glob(os.path.join(IMAGE_FOLDER, "*.jpg")) + glob.glob(os.path.join(IMAGE_FOLDER, "*.jpeg"))
        return images[:8] if len(images) >= 8 else ["🐱", "🐾", "💖", "🎯", "⭐", "🌟", "💫", "✨"]
    return ["🐱", "🐾", "💖", "🎯", "⭐", "🌟", "💫", "✨"]

def memory():
    st.title("Memory du Chaton")
    
    # Initialize memory game
    if 'memory_grid' not in st.session_state:
        images = get_images()
        pairs = images * 2
        random.shuffle(pairs)
        st.session_state.memory_grid = np.array(pairs).reshape(4, 4)
        st.session_state.revealed = np.zeros((4, 4), dtype=bool)
        st.session_state.matched = np.zeros((4, 4), dtype=bool)
        st.session_state.selected = []
        st.session_state.moves = 0
        st.session_state.checking = False

    # Display grid
    for i in range(4):
        cols = st.columns(4)
        for j in range(4):
            with cols[j]:
                if st.session_state.matched[i, j] or st.session_state.revealed[i, j]:
                    if IMAGE_FOLDER in st.session_state.memory_grid[i, j]:
                        st.image(st.session_state.memory_grid[i, j], width=100)
                    else:
                        st.markdown(f"<div style='font-size:60px;text-align:center;height:100px;display:flex;align-items:center;justify-content:center;border:1px solid #ccc;'>{st.session_state.memory_grid[i, j]}</div>", unsafe_allow_html=True)
                else:
                    if st.button("❓", key=f"card_{i}_{j}", use_container_width=True):
                        if len(st.session_state.selected) < 2 and not st.session_state.revealed[i, j] and not st.session_state.checking:
                            st.session_state.revealed[i, j] = True
                            st.session_state.selected.append((i, j))
                            
                            if len(st.session_state.selected) == 2:
                                st.session_state.moves += 1
                                st.session_state.checking = True
                                st.rerun()

    # Check for matches after both cards are revealed
    if st.session_state.checking and len(st.session_state.selected) == 2:
        time.sleep(2)  # Brief pause to show both cards
        pos1, pos2 = st.session_state.selected
        if st.session_state.memory_grid[pos1] == st.session_state.memory_grid[pos2]:
            st.session_state.matched[pos1] = True
            st.session_state.matched[pos2] = True
            st.success(random.choice(SUCCESS_MESSAGES))
            time.sleep(2)
        else:
            st.session_state.revealed[pos1] = False
            st.session_state.revealed[pos2] = False
            st.error(random.choice(ERROR_MESSAGES))
            time.sleep(2)
        st.session_state.selected = []
        st.session_state.checking = False
        st.rerun()

    st.write(f"Moves: {st.session_state.moves}")
    
    if np.all(st.session_state.matched):
        st.success("Wooow, elle est fooooorte !")
        st.balloons()
    
    if st.button("Nouveau jeu"):
        del st.session_state.memory_grid
        del st.session_state.revealed
        del st.session_state.matched
        del st.session_state.selected
        del st.session_state.moves
        del st.session_state.checking
        st.rerun()