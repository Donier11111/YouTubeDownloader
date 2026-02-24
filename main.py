import yt_dlp
import os
import logging
import ast
from tkinter.filedialog import askopenfile


log = logging.getLogger()#Определение логгера
logging.basicConfig(
    level=logging.INFO,#Минимальный уровень который будет высвечиваться
    format='%(asctime)s - %(levelname)s - %(message)s',#Формат начала логга
    handlers=[#параметры файла сохранения
        logging.FileHandler("downloads.log", encoding='utf-8'),
        logging.StreamHandler() 
    ]
)

def download(link,prop):#Скачивание с использованием propeties.cfg
    os.makedirs("YT_music", exist_ok=True)#Создание папки для сохранения музыки
    try:
        log.info(f"Try to Download music")
        with yt_dlp.YoutubeDL(prop) as ydl:#определение ydl
            ydl.download([link])
        log.info("Загрузка  успешно завершена!")
    except Exception as e:
        log.error(e,exc_info=True)

def main(prop):#Меню выбора 
    print("Your link\n1.Just link on music or playlist\n2.Txt file with links\n")
    choise = int(input("Your choose:"))
    if choise == 1:
        link = input("Type your link: ").strip()
        download(link , prop)
    elif choise == 2:
        try:
            with askopenfile(filetypes = (("Text Files", "*.txt"),("All files", "*.*"))) as f:
                links = f.read().strip().split("\n")
                log.info(links)
                for i in links:
                    download(i , prop)
        except TypeError:
            log.error("Type again")
        except Exception as e:
            log.error("Error: ",e)
        

if __name__ == "__main__":
    with open('propeties.cfg', 'r', encoding='utf-8') as f:
        file = f.read()
        prop = ast.literal_eval(file)
        main(prop)