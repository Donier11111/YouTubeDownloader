import yt_dlp
import logging



log = logging.getLogger()#Определение логгера
logging.basicConfig(
    level=logging.INFO,#Минимальный уровень который будет высвечиваться
    format='%(asctime)s - %(levelname)s - %(message)s',#Формат начала логга
    handlers=[#параметры файла сохранения
        logging.FileHandler("downloads.log", encoding='utf-8'),
        logging.StreamHandler() 
    ]
)

def YTDL(link,prop):#Скачивание с использованием propeties.cfg
    
    try:
        with yt_dlp.YoutubeDL(prop) as ydl:#определение ydl
                ydl.download([link])
    except Exception as e:
        log.error(e,exc_info=True)
    return
