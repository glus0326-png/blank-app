@echo off
python -m venv .venv
call .venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
python -m streamlit run streamlit_app.py --server.port 8502
pause
