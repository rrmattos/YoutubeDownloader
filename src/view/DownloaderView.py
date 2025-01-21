import os
import re
from pathlib import Path

def get_user_urls():

    import re
from pathlib import Path

def get_user_urls():

    import re
from pathlib import Path

def get_user_urls():

    urls = input("Informe a(s) URL(s) do vídeo (ou caminho de um arquivo com as URLs): ").strip()

    # --- Verifica o sistema operacional ---
    if os.name == 'nt':  # --- Se o sistema for Windows ---
        # --- Substitui barras invertidas por barras normais ---
        urls = urls.replace("\\", "/")

    # --- Verifica se o input é um caminho de arquivo válido ---
    file_path = Path(urls)
    if file_path.exists():
        if file_path.is_file():
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    urls = [line.strip() for line in file if line.strip()]
                if not urls:
                    print(f"O arquivo '{file_path}' não contém URLs válidas.")
                    return []
                print(f"URLs carregadas do arquivo: {file_path}")
                return urls
            except Exception as e:
                print(f"Erro ao abrir o arquivo {file_path}: {e}")
                return []
        else:
            print(f"'{urls}' não é um arquivo, é um diretório ou outro tipo de caminho.")
            return []
    else:
        print(f"O caminho '{urls}' não existe.")
    
    # --- Verifica se o input é uma URL válida ---
    if re.match(r'^(https?://|www\.)[^\s/$.?#].[^\s]*$', urls):
        return [urls]

    # --- Caso múltiplas URLs sejam separadas por vírgula ---
    if ',' in urls:
        return [url.strip() for url in urls.split(',') if url.strip()]

    # --- Caso contrário, considera como uma URL inválida ---
    else:
        print("Entrada inválida. Certifique-se de fornecer uma URL ou arquivo válido. (OBS: Está inserindo a extensão do arquivo?)")
        return []


def display_options(valid_formats):
    print("\nOpções disponíveis:")
    print("0: Cancelar")
    for i, fmt in enumerate(valid_formats, start=1):
        print(f"{i}: {fmt['type']} - {fmt['details']}")

def get_user_choice(total_options):
    while True:
        try:
            choice = int(input("\nEscolha o número da opção: "))
            if 0 <= choice <= total_options:
                if choice == 0:
                    return None  # --- Cancelar operação ---
                return choice - 1
            print(f"Escolha inválida. Digite um número entre 1 e {total_options} ou 0 para cancelar.")
        except ValueError:
            print("Entrada inválida. Digite um número.")

def display_header():
    print("=" * 50)
    print("Youtube Downloader - Versão 1.0")
    print("Criado por: Rafael Réus Mattos | Contato: rafael.r.mattos04@gmail.com")
    print("=" * 50)
    print("\n")
