import os
import tempfile

def get_unique_filename(filename):
    # --- Adiciona um número ao final do nome do arquivo se já existir. ---
    base, ext = os.path.splitext(filename)
    counter = 1

    while os.path.exists(filename):
        filename = f"{base} ({counter}){ext}"
        counter += 1

    return filename


def filter_duplicate_formats(formats):
    # --- Remove formatos duplicados ou muito similares. ---
    unique_formats = {}
    for fmt in formats:
        key = (fmt.get('resolution', 'N/A'), fmt.get('ext', 'N/A'), fmt.get('fps', 'N/A'))
        current_tbr = fmt.get('tbr', 0) or 0  # --- Substitui None por 0 ---
        if key not in unique_formats or current_tbr > (unique_formats[key].get('tbr', 0) or 0):
            unique_formats[key] = fmt
    return list(unique_formats.values())


def get_temp_directory():
    # --- Retorna o diretório temporário do sistema operacional. ---
    return tempfile.gettempdir()
