import os
import subprocess
import yt_dlp
from model.VideoConfig import get_unique_filename, filter_duplicate_formats, get_temp_directory
from view.DownloaderView import get_user_urls, display_options, get_user_choice, display_header
from utils.CheckInternet import check_internet_connection

def download_yt():
    urls = get_user_urls()

    if any(url.lower() in ['exit', 'sair', '0'] for url in urls):
        print("Saindo do programa...")
        return
    
    # --- Verifica se não há URLs válidas ---
    elif not urls or all(url.strip() == '' for url in urls):
        print("Nenhuma URL válida fornecida. Abortando.")
        return

    # --- Verifica se a pasta 'downloads' existe, caso contrário cria ---
    download_dir = os.path.join(os.getcwd(), 'downloads')
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
        print(f"Diretório 'downloads' criado em: {download_dir}\n")
    
    temp_dir = get_temp_directory()
    print(f"Arquivos temporários serão salvos em: {temp_dir}\n")
    
    print("Testando conexão com a internet...\n")
    for url in urls:
        if not check_internet_connection():
            print("Sem conexão com a internet. Abortando o download.")
            break

    print("-----------------------------------------------")
    print(f"Arquivos serão salvos em: {download_dir}\n")

    for url in urls:
        # --- Ignora URLs vazias ---
        if not url.strip():
            continue

        if not check_internet_connection():
            print("Sem conexão com a internet. Abortando o download.")
            break
        
        print("-----------------------------------------------\n")
        print(f"Iniciando download para a URL: {url.strip()}")
        try:
            ydl_opts = {'quiet': True}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url.strip(), download=False)
                formats = filter_duplicate_formats(info.get('formats', []))

                valid_formats = []
                for fmt in formats:
                    if fmt.get('acodec') != 'none' and fmt.get('vcodec') != 'none':
                        resolution = fmt.get('resolution', 'N/A')
                        fps = fmt.get('fps', 'N/A')
                        valid_formats.append({
                            'id': fmt['format_id'],
                            'type': 'Video+Audio',
                            'details': f"{resolution} - {fmt['ext']} - {fps}fps"
                        })
                    elif fmt.get('acodec') == 'none' and fmt.get('vcodec') != 'none':
                        resolution = fmt.get('resolution', 'N/A')
                        fps = fmt.get('fps', 'N/A')
                        valid_formats.append({
                            'id': fmt['format_id'],
                            'type': 'Video-only',
                            'details': f"{resolution} - {fmt['ext']} - {fps}fps"
                        })
                    elif fmt.get('vcodec') == 'none' and fmt.get('acodec') != 'none' and fmt.get('abr') is not None:
                        abr = fmt.get('abr', 'N/A')
                        valid_formats.append({
                            'id': fmt['format_id'],
                            'type': 'Audio-only',
                            'details': f"{abr} kbps - {fmt['ext']}"
                        })

                display_options(valid_formats)
                choice = get_user_choice(len(valid_formats))
                if choice is None:
                    print("Download cancelado para esta URL.")
                    continue 
                selected_format = valid_formats[choice]

                if selected_format['type'] == 'Video-only':
                    print("\nSelecionado vídeo sem áudio. Buscando áudio compatível...")
                    audio_format = max(
                        (f for f in formats if f.get('vcodec') == 'none' and f.get('acodec') != 'none' and f.get('abr') is not None),
                        key=lambda x: x.get('abr', 0),
                        default=None
                    )

                    if not audio_format:
                        print(f"Erro: Não foi possível encontrar um áudio compatível para a URL {url}.")
                        continue 

                    # --- Inicia processo de união de vídeo com áudio ---
                    video_filename = os.path.join(download_dir, "video.mp4")
                    audio_filename = os.path.join(download_dir, "audio.webm")
                    output_filename = get_unique_filename(os.path.join(download_dir, f"{info['title']}.mp4"))

                    ydl_opts_video = {'format': selected_format['id'], 'outtmpl': video_filename}
                    ydl_opts_audio = {'format': audio_format['format_id'], 'outtmpl': audio_filename}

                    with yt_dlp.YoutubeDL(ydl_opts_video) as ydl:
                        ydl.download([url])
                    with yt_dlp.YoutubeDL(ydl_opts_audio) as ydl:
                        ydl.download([url])

                    subprocess.run([
                        'ffmpeg', '-i', video_filename, '-i', audio_filename, '-c:v', 'copy', '-c:a', 'aac', output_filename
                    ], check=True)
                    print(f"Download completo para a URL {url}: {output_filename}")

                    os.remove(video_filename)
                    os.remove(audio_filename)

                else:
                    output_filename = get_unique_filename(os.path.join(download_dir, f"{info['title']}.%(ext)s"))
                    ydl_opts = {'format': selected_format['id'], 'outtmpl': output_filename}

                    print(f"\nBaixando para a URL {url}: {selected_format['type']} - {selected_format['details']}")
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([url])
                    print(f"Download concluído para a URL {url}: {output_filename}")

        except Exception as e:
            print(f"Erro no download para {url}: {e}")
