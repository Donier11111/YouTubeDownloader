import customtkinter
import os
from DownloadMaster import YTDL 
import logging
from tkinter import filedialog
app = customtkinter.CTk()
links = ""


log = logging.getLogger()#Определение логгера
logging.basicConfig(
    level=logging.INFO,#Минимальный уровень который будет высвечиваться
    format='%(asctime)s - %(levelname)s - %(message)s',#Формат начала логга
    handlers=[#параметры файла сохранения
        logging.FileHandler("downloads.log", encoding='utf-8'),
        logging.StreamHandler() 
    ]
)

class DownloadManager():
    def __init__(self,prop):
        self.prop = prop
        pass
    def get_provide(self,link):
        log.info(f"Загрузка {len(link)} треков началась")
        Download_status.configure(text=f"Загрузка {len(link)} треков началась")
        for i in link:
            YTDL(i,self.prop)
        log.info(f"Загрузка треков законченна")
        Download_status.configure(text=f"Загрузка {len(link)} треков закончилась")



def selectfile():
    global links, filesk_txt
    with filedialog.askopenfile(filetypes = (("Text Files", "*.txt"),("All files", "*.*"))) as file:
        File_status.configure(text=file.name)
        links = file.read()
  


def select_one(choice):
    # Логика исключения: оставляем только одну галочку
    if choice != "144p":  cb1.deselect()
    if choice != "360p":  cb2.deselect()
    if choice != "480p":  cb3.deselect()
    if choice != "720p":  cb4.deselect()
    if choice != "1080p": cb5.deselect()
    if choice != "mp3":   cb6.deselect()

def get_quality():
    # Проверяем, какой чекбокс нажат, и возвращаем параметры
    if cb1.get(): return "bv[height<=144][vcodec^=avc1]+ba[ext=m4a]/b[height<=144][ext=mp4]", "mp4"
    if cb2.get(): return "bv[height<=360][vcodec^=avc1]+ba[ext=m4a]/b[height<=360][ext=mp4]", "mp4"
    if cb3.get(): return "bv[height<=480][vcodec^=avc1]+ba[ext=m4a]/b[height<=480][ext=mp4]", "mp4"
    if cb4.get(): return "bv[height<=720][vcodec^=avc1]+ba[ext=m4a]/b[height<=720][ext=mp4]", "mp4"
    if cb5.get(): return "bv[height<=1080][vcodec^=avc1]+ba[ext=m4a]/b[height<=1080][ext=mp4]", "mp4"
    if cb6.get(): return "bestaudio/best", "mp3"
    return "bestaudio/best", "mp3" # По умолчанию

def space():
    os.makedirs(rf"{path_dir.get()}", exist_ok=True)
    
    q_val, ext_type = get_quality() 
    
    # Базовые постпроцессоры (превью и метаданные)
    post_procs = [
        {'key': "EmbedThumbnail"}, 
        {'key': "FFmpegMetadata"}
    ]
    
    # Если выбран режим mp3, добавляем извлечение аудио
    if ext_type == "mp3":
        post_procs.insert(0, {
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        })

    prop = {
        'writethumbnail': True,
        'format': q_val,
        'retries': 15,
        'fragment_retries': 15,
        'socket_timeout': 30,              # Ждать ответа сервера 30 секунд
        'retry_sleep_functions': {'http': lambda n: 5},
        'ignoreerrors': True,              # Чтобы один битый файл не ломал всю очередь
        'postprocessors': post_procs,
        'ffmpeg_location': r'C:\Users\egamd\Downloads\ffmpeg\bin\ffmpeg.exe',
        'outtmpl': rf'{path_dir.get()}/%(title)s.%(ext)s',
        'cookies': 'VK.txt',
        'nocheckcertificate': True,        # Помогает при проблемах с SSL/прокси
    }
    
    Request = DownloadManager(prop)
    
    # Очистка ссылок от пустых строк
    if url.get():
        links_list = [l.strip() for l in url.get().split("\n") if l.strip()]
        Request.get_provide(links_list)
    if links != "":
        links_list = [l.strip() for l in links.split("\n") if l.strip()]
        Request.get_provide(links_list)

# --- ВИДЖЕТЫ ---
sidebarleft = customtkinter.CTkFrame(app, width=600, corner_radius=15)
path_dir = customtkinter.CTkEntry(sidebarleft, placeholder_text="Название папки")
url = customtkinter.CTkEntry(sidebarleft, placeholder_text="Ссылка на музыку")

# Фрейм для чекбоксов качества
quality_frame = customtkinter.CTkFrame(sidebarleft)

cb1 = customtkinter.CTkCheckBox(quality_frame, text="144p", command=lambda: select_one("144p"), width=80)
cb2 = customtkinter.CTkCheckBox(quality_frame, text="360p", command=lambda: select_one("360p"), width=80)
cb3 = customtkinter.CTkCheckBox(quality_frame, text="480p", command=lambda: select_one("480p"), width=80)
cb4 = customtkinter.CTkCheckBox(quality_frame, text="720p", command=lambda: select_one("720p"), width=80)
cb5 = customtkinter.CTkCheckBox(quality_frame, text="1080p", command=lambda: select_one("1080p"), width=80)
cb6 = customtkinter.CTkCheckBox(quality_frame, text="mp3", command=lambda: select_one("mp3"), width=80)
cb6.select() # Ставим mp3 по умолчанию

# Остальные виджеты
Download_status = customtkinter.CTkLabel(sidebarleft, text="--", wraplength=250)
File_status = customtkinter.CTkLabel(sidebarleft, text="Nonefile", wraplength=250)
filesk = customtkinter.CTkButton(sidebarleft, text="Выбрать файл", command=selectfile)
download = customtkinter.CTkButton(sidebarleft, text="Скачать", command=space)

if __name__ == "__main__":
    sidebarleft.pack(fill='x', padx=10, pady=10)
    url.pack(pady=5, fill='x', padx=10)
    path_dir.pack(pady=5, fill='x', padx=10)
    
    # Размещаем чекбоксы в сетку внутри их фрейма
    quality_frame.pack(pady=10)
    cb1.grid(row=0, column=0, padx=5, pady=2)
    cb2.grid(row=0, column=1, padx=5, pady=2)
    cb3.grid(row=1, column=0, padx=5, pady=2)
    cb4.grid(row=1, column=1, padx=5, pady=2)
    cb5.grid(row=2, column=0, padx=5, pady=2)
    cb6.grid(row=2, column=1, padx=5, pady=2)

    filesk.pack(pady=5, side='left', padx=10)
    File_status.pack(pady=5, side='left')
    download.pack(pady=5, side="right", padx=10)
    Download_status.pack(pady=5, side='right')

    app.geometry("600x450") # Увеличил высоту под чекбоксы
    app.mainloop()