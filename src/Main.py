from controller.VideoDownloader import download_yt
from view.DownloaderView import display_header

def main():
    display_header()
    download_yt()
    input("...")

if __name__ == "__main__":
    main()