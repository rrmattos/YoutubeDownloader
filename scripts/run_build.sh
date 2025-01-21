# !/bin/bash
# --- Ativar o ambiente virtual ---
source ./venv/bin/activate
# --- Rodar o PyInstaller para gerar o executável ---
pyinstaller --onefile --add-data "assets/ffmpeg:." --name "YoutubeDownloader" src/main.py
