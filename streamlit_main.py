import streamlit as st
import numpy as np
import puzzle_generator
import logging
import json
import os
import random
import glob

import sudoku_choupette
import memory
import entre_1_et_4


st.markdown("""
<style>
    .stTextInput > div > div > input {
        text-align: center;
        font-size: 20px;
        font-weight: bold;
        height: 40px;
        width: 40px;
        padding: 0;
        border: 1px solid #333;
        box-shadow: none;
        background-color: #ffffff;
        color: #000000;
    }
    .stTextInput > div > div > input:disabled {
        background-color: #f0f0f0;
        color: #000000;
        font-weight: bold;
        box-shadow: none;
    }
    .stTextInput > div > div > input:focus {
        border: 2px solid #1f77b4;
        box-shadow: none;
        outline: none;
    }
    .stButton > button {
        width: 100%;
        margin: 5px 0;
        box-shadow: none;
        height: 100px;
        font-size: 40px;
    }
    * {
        box-shadow: none !important;
    }
    
</style>
""", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["SudoChoupette", "Memory", "Entre 1 et 4"])

with tab1 : 
    sudoku_choupette.sudoku()
    
with tab2 :
    memory.memory()
    
with tab3:
    entre_1_et_4.entre_1_et_4()