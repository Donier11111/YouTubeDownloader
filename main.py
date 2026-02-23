import yt_dlp
import os
import logging


logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s',
    handlers=[
        logging.FileHandler("downloads.log", encoding='utf-8'),
        logging.StreamHandler() 
    ]
)
class YDL_Logger:
    def info(self, msg):
        logger.info(msg)

    def warning(self, msg):
        logger.warning(msg)

    def error(self, msg):
        logger.error(msg)

def download(link):
    os.makedirs("YT_music", exist_ok=True)
    prop = {
        'writethumbnail':True,
        'format':'bestaudio/best',

        'postprocessors' : [{           #<<<< Постпроцессы купи hifi плеер
            'key': 'FFmpegExtractAudio', 
            'preferredcodec': 'mp3',      
            'preferredquality': '320',
            },

            {'key':"EmbedThumbnail"},
            {'key':"FFmpegMetadata"}],

            'download_archive':'archive.txt',
            'ffmpeg_location': r'C:\Users\egamd\Downloads\ffmpeg\bin\ffmpeg.exe',
            'noplaylist': False,
            'outtmpl': 'YT_music/%(title)s.%(ext)s'
        }
    try:
        logger.info(f"Try to Download music")
        with yt_dlp.YoutubeDL(prop) as ydl:
            ydl.download([link])
        logger.info("Загрузка успешно завершена!")
    except Exception as e:
        logger.error(e,exc_info=True)
        pass

if __name__ == "__main__":
    link = input("your link: ").strip()
    try:
        download(link)
    except Exception as e:
        logger.error(e,exc_info=True)