@echo off
REM --- Ativar o ambiente virtual ---
call .\.venv\Scripts\activate
REM --- Rodar o PyInstaller para gerar o executável ---
PyInstaller --onefile --add-data "assets/ffmpeg;." --name "YoutubeDownloader" src\main.py
pause
