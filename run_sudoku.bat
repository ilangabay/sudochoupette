@echo off
REM Run Streamlit with suppressed warnings
set STREAMLIT_LOGGER_LEVEL=ERROR
streamlit run sudoku_app_fixed.py --logger.level=error