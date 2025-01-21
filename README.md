# YoutubeDownloader

This is a Python Exercise project. It can download YouTube audios or videos with the available resolutions in the source.

If you prefer not to build the project yourself, you can download a pre-compiled .exe file (for Windows) here: [google drive](https://drive.google.com/file/d/1B7DtESr5JM7fhm0sgY8lxS5pHCzhfry4/view?).

Se você não quiser criar o executável baixando o projeto, pode somente baixar uma versão pré-compilada .exe (para Windows) aqui: [google drive](https://drive.google.com/file/d/1B7DtESr5JM7fhm0sgY8lxS5pHCzhfry4/view?).

## Instructions

### --- English ---

#### Prerequisites:

1. Make sure you have **Python 3.x** installed on your machine. You can download Python from the official site: [https://www.python.org/downloads/](https://www.python.org/downloads/).
   
2. After cloning the repository, create a virtual environment to install dependencies:
   
   On Windows:
   ```bash
   python -m venv venv
   ```

   On Linux or Mac:
   ```bash
   python3 -m venv venv
   ```

3. Activate the virtual environment:
   
   On Windows (PowerShell):
   ```bash
   .\venv\Scripts\Activate
   ```

   On Linux or Mac:
   ```bash
   source venv/bin/activate
   ```

4. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

#### How to Generate the Program Build:

First, unzip the `ffmpeg.zip` into the `assets` folder. After that:

1. On Windows, open PowerShell in the project folder and run `scripts/run_build.bat`.
   
2. On Linux or Mac, open a terminal in the project folder and run `scripts/run_build.sh`.

#### How to Provide URLs:

You can provide the video URLs in three different ways:

- By entering a single URL;
- By entering multiple URLs, separated by commas (`,`);
- By creating a text file (e.g., `.txt`) containing all the URLs, with each one on a separate line.

#### Exiting the Program:

In the initial prompt, typing (without quotes) `exit`, `sair`, or `0` will close the program.

---

### --- Português ---

#### Pré-requisitos:

1. Certifique-se de ter o **Python 3.x** instalado na sua máquina. Você pode baixar o Python no site oficial: [https://www.python.org/downloads/](https://www.python.org/downloads/).
   
2. Após clonar o repositório, crie um ambiente virtual para instalar as dependências:
   
   No Windows:
   ```bash
   python -m venv venv
   ```

   No Linux ou Mac:
   ```bash
   python3 -m venv venv
   ```

3. Ative o ambiente virtual:
   
   No Windows (PowerShell):
   ```bash
   .\venv\Scripts\Activate
   ```

   No Linux ou Mac:
   ```bash
   source venv/bin/activate
   ```

4. Instale as dependências necessárias:
   ```bash
   pip install -r requirements.txt
   ```

#### Para gerar a build do programa:

Primeiro, extraia o arquivo `ffmpeg.zip` na pasta `assets`. Depois:

1. No Windows, abra o PowerShell na pasta do projeto e execute `scripts/run_build.bat`.

2. No Linux ou Mac, abra o terminal na pasta do projeto e execute `scripts/run_build.sh`.

#### Para informar as URLs:

Você pode passar as URLs dos vídeos que deseja baixar de 3 maneiras:

- Inserindo apenas uma URL;
- Inserindo mais de uma URL separando-as por vírgula (`,`);
- Criando um arquivo de texto (ex: `.txt`) com todas as URLs que deseja, separando-as com quebra de linha (Enter).

#### Na pergunta inicial, se digitar sem aspas: `exit`, `sair` ou `0`, o programa se encerra.
