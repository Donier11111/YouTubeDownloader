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
  

def space():
    os.makedirs("Download", exist_ok=True)#Создание папки для сохранения музыки
    prop = {'writethumbnail':True,
            'format':'bestaudio/best',
            'postprocessors':[{'key':'FFmpegExtractAudio','preferredcodec':'mp3','preferredquality':'320'},
                {'key':"EmbedThumbnail"},
                {'key':"FFmpegMetadata"}],
            'download_archive':rf'{path_dir.get()}/archive.txt',
            'ffmpeg_location':r'C:\Users\egamd\Downloads\ffmpeg\bin\ffmpeg.exe',
            'noplaylist':False,
            'outtmpl':rf'{path_dir.get()}/%(title)s.%(ext)s',
            'user_agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:147.0) Gecko/20100101 Firefox/147.0',
            'cookies':'VK.txt' , 
            'retries': 10,
            'nocheckcertificate': True}
    Request = DownloadManager(prop)
    if url.get():
        link = url.get().split("\n")
        Request.get_provide(link)
    if links != "":
        Request.get_provide(links.split("\n"))


sidebarleft = customtkinter.CTkFrame(app,width=400, corner_radius=15)
path_dir = customtkinter.CTkEntry(sidebarleft, placeholder_text="Название папки")
url = customtkinter.CTkEntry(sidebarleft, placeholder_text="Ссылка на музыку")
File_status = customtkinter.CTkLabel(sidebarleft , text = "Nonefile" , wraplength=250)
Download_status = customtkinter.CTkLabel(sidebarleft, text = "" , wraplength=250)
filesk = customtkinter.CTkButton(sidebarleft, text="Выберите файл", command=selectfile)
download = customtkinter.CTkButton(sidebarleft,text=("Скачать") , command = space)    
if __name__ == "__main__":
        sidebarleft.pack(side="left")
        url.pack(pady=20)
        path_dir.pack(pady=20)
        File_status.pack(pady=50,side='right')
        Download_status.pack(pady=50,side='left')
        download.pack(pady=50,side='left')
        filesk.pack(pady=50,side='right')
        
        app.mainloop()


            
            