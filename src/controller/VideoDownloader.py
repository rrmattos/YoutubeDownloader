import os
import re
import requests
import subprocess
import sys
import tempfile
import shutil
from model.VideoConfig import get_unique_filename, filter_duplicate_formats, get_temp_directory
from view.DownloaderView import get_user_urls, display_options, get_user_choice
from utils.CheckInternet import check_internet_connection

YT_DLP_EXE = os.path.join(os.getcwd(), "yt-dlp.exe")  # externo
FFMPEG_NAME = "ffmpeg.exe"  # será embutido

# ---------------- Função principal ---------------- #
def download_yt():
    update_yt_dlp_exe()  # verifica e atualiza yt-dlp.exe

    urls = get_user_urls()

    if any(url.lower() in ['exit', 'sair', '0'] for url in urls):
        print("Saindo do programa...")
        return

    if not urls or all(url.strip() == '' for url in urls):
        print("Nenhuma URL válida fornecida. Abortando.")
        return

    download_dir = os.path.join(os.getcwd(), 'downloads')
    os.makedirs(download_dir, exist_ok=True)
    temp_dir = get_temp_directory()
    print(f"Arquivos temporários serão salvos em: {temp_dir}\n")
    print(f"Arquivos serão salvos em: {download_dir}\n")

    # Extrai ffmpeg embutido
    ffmpeg_path = extract_embedded_ffmpeg(temp_dir)

    for url in urls:
        if not url.strip():
            continue
        if not check_internet_connection():
            print("Sem conexão com a internet. Abortando o download.")
            break

        print(f"Verificando as opções de download para a URL: {url.strip()}")
        try:
            info = extract_info(url.strip())
            formats = filter_duplicate_formats(info.get('formats', []))

            # Melhor áudio
            audio_formats = [f for f in formats if f.get('vcodec') == 'none' and f.get('acodec') != 'none']
            best_audio = max(audio_formats, key=lambda x: x.get('abr', 0)) if audio_formats else None

            # Lista todas as opções de vídeo+áudio direto ou vídeo para merge
            video_options = []
            for fmt in formats:
                if fmt.get('vcodec') != 'none':
                    resolution = fmt.get('resolution', 'N/A')
                    fps = fmt.get('fps', 'N/A')
                    ext = fmt.get('ext')
                    video_options.append({
                        'id': fmt['format_id'],
                        'type': 'Video+Audio',
                        'details': f"{resolution} - {ext} - {fps}fps"
                    })

            # Adiciona última opção: somente áudio
            if best_audio:
                video_options.append({
                    'id': best_audio['format_id'],
                    'type': 'Somente Audio',
                    'details': f"Áudio somente - {best_audio.get('abr', 'N/A')} kbps - {best_audio['ext']}"
                })

            if not video_options:
                print("Nenhum formato válido encontrado (Video+Audio ou Somente Audio).")
                continue

            display_options(video_options)
            choice = get_user_choice(len(video_options))
            if choice is None:
                print("Download cancelado para esta URL.")
                continue

            selected = video_options[choice]
            output_filename = get_unique_filename(
                os.path.join(download_dir, sanitize_filename(f"{info['title']}.mp4"))
            )

            # --- Download e merge se necessário ---
            if selected['type'] == 'Video+Audio':
                video_filename = os.path.join(temp_dir, "video_temp.mp4")
                run_yt_dlp_exe(url, selected['id'], video_filename)

                fmt_selected = next((f for f in formats if f['format_id'] == selected['id']), None)
                if fmt_selected and fmt_selected.get('acodec') == 'none' and best_audio:
                    audio_filename = os.path.join(temp_dir, "audio_temp.webm")
                    run_yt_dlp_exe(url, best_audio['format_id'], audio_filename)
                    subprocess.run([
                        ffmpeg_path, '-y', '-i', video_filename, '-i', audio_filename,
                        '-c:v', 'copy', '-c:a', 'aac', output_filename
                    ], check=True)
                    os.remove(video_filename)
                    os.remove(audio_filename)
                else:
                    shutil.move(video_filename, output_filename)

                print(f"Download completo: {output_filename}")

            else:
                # Somente áudio
                run_yt_dlp_exe(url, selected['id'], output_filename)
                print(f"Download completo: {output_filename}")

        except Exception as e:
            print(f"Erro no download para {url}: {e}")

# ---------------- Funções auxiliares ---------------- #
def sanitize_filename(filename: str) -> str:
    return re.sub(r'[\\/:*?"<>|]', '_', filename)

def run_yt_dlp_exe(url: str, format_id: str, output_path: str):
    cmd = [YT_DLP_EXE, "-f", format_id, url, "-o", output_path]
    subprocess.run(cmd, check=True)

def extract_info(url: str) -> dict:
    import json
    cmd = [YT_DLP_EXE, "-j", url]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return json.loads(result.stdout)

def update_yt_dlp_exe(exe_path=None):
    if exe_path is None:
        exe_path = YT_DLP_EXE

    url = "https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp.exe"
    temp_path = exe_path + ".tmp"

    current_version = "0"
    if os.path.exists(exe_path):
        try:
            result = subprocess.run([exe_path, "--version"], capture_output=True, text=True, check=True)
            current_version = result.stdout.strip()
        except Exception:
            pass

    try:
        r = requests.get("https://api.github.com/repos/yt-dlp/yt-dlp/releases/latest")
        r.raise_for_status()
        latest_version = r.json()['tag_name'].lstrip('v')
    except Exception as e:
        print(f"[WARN] Não foi possível verificar versão mais recente: {e}")
        return

    if current_version == latest_version:
        print(f"[INFO] yt-dlp já está atualizado (v{current_version}).")
        return

    print(f"[INFO] Atualizando yt-dlp: {current_version} → v{latest_version} ...")
    try:
        r = requests.get(url, stream=True)
        r.raise_for_status()
        with open(temp_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
        if os.path.exists(exe_path):
            os.remove(exe_path)
        os.rename(temp_path, exe_path)

        print(f"[INFO] yt-dlp atualizado com sucesso para v{latest_version}!")
        print("⚠️ Feche e abra novamente o programa para usar a nova versão.")
        input("Pressione qualquer tecla para sair...")
        sys.exit(0)

    except Exception as e:
        print(f"[WARN] Não foi possível atualizar o yt-dlp automaticamente: {e}")
        if os.path.exists(temp_path):
            os.remove(temp_path)

def extract_embedded_ffmpeg(temp_dir: str) -> str:
    """
    Retorna o caminho do ffmpeg embutido (extrai para temp se necessário)
    """
    ffmpeg_path = os.path.join(temp_dir, FFMPEG_NAME)
    if getattr(sys, 'frozen', False):
        # PyInstaller: arquivo embutido
        import pkgutil
        ffmpeg_data = pkgutil.get_data(__package__, FFMPEG_NAME)
        if ffmpeg_data:
            with open(ffmpeg_path, "wb") as f:
                f.write(ffmpeg_data)
    else:
        # rodando do script: usa ffmpeg da pasta assets
        ffmpeg_path = os.path.join(os.getcwd(), "assets", FFMPEG_NAME)
    return ffmpeg_path
