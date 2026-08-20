import customtkinter
import os
import logging
from tkinter import filedialog
import yt_dlp
import threading
import sys


save =""

COLOR_BG = "#160d0d"         
COLOR_FRAME = "#1e1313"      
COLOR_HIGHLIGHT = "#2a1819"  
COLOR_ACCENT = "#1a1010"   
COLOR_TEXT = "#f2aba1"      
COLOR_DANGER = "#F7768E"   

# Настройка логирования
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("log.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)
log = logging.getLogger()


links_from_file = ""

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)




def choise_save():
    global save
    app.after(0, lambda: path_dir.configure(text=f"Папка сохранения"))
    try:
        save = filedialog.askdirectory(title="Выберите папку сохранения")
    except:
        app.after(0, lambda: path_dir.configure(text=f"Попробуйте заново"))
    if save != '':
        app.after(0, lambda: path_dir.configure(text=f"Папка сохранения:{save}"))
    

def selectfile():
    global links_from_file
    file = filedialog.askopenfile(filetypes=(("Text Files", "*.txt"), ("All files", "*.*")))
    if file:
        File_status.configure(text=os.path.basename(file.name))
        links_from_file = file.read()

def select_one(choice):
    cbs = [cb1, cb2, cb3, cb4, cb5, cb6]
    names = ["144p", "360p", "480p", "720p", "1080p", "flac"]
    for cb, name in zip(cbs, names):
        if name != choice: cb.deselect()

def get_quality():
    if cb1.get(): return "bv[height<=144][vcodec^=avc1]+ba[ext=m4a]/b[height<=144][ext=mp4]", "mp4"
    if cb2.get(): return "bv[height<=360][vcodec^=avc1]+ba[ext=m4a]/b[height<=360][ext=mp4]", "mp4"
    if cb3.get(): return "bv[height<=480][vcodec^=avc1]+ba[ext=m4a]/b[height<=480][ext=mp4]", "mp4"
    if cb4.get(): return "bv[height<=720][vcodec^=avc1]+ba[ext=m4a]/b[height<=720][ext=mp4]", "mp4"
    if cb5.get(): return "bv[height<=1080][vcodec^=avc1]+ba[ext=m4a]/b[height<=1080][ext=mp4]", "mp4"
    return "bestaudio/best", "flac"

def progress_hook(process):
    if process["status"] == 'downloading':
        app.after(0, lambda: Download_status.configure(text="Идет скачивание...", text_color=COLOR_ACCENT))
    if process["status"] == 'finished':
        app.after(0, lambda: Download_status.configure(text="Обработка завершена", text_color="green"))

def space(): 
    folder_name = save.strip()
    if not save:
        Download_status.configure(text="Введите название папки!", text_color=COLOR_DANGER)
        return

    try:
        os.makedirs(save, exist_ok=True)
    except Exception as e:
        Download_status.configure(text="Ошибка создания папки", text_color=COLOR_DANGER)
        log.error(e)
        return

    q_val, ext_type = get_quality()
    post_procs = [{'key': "EmbedThumbnail" ,  'already_have_thumbnail': False,}, {'key': "FFmpegMetadata"}]
    
    if ext_type == "flac":
        post_procs.insert(0, {
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'flac',
            
        })

    prop = {
        'writethumbnail': True,
        'audio_quality': 0,
        'format': q_val,
        'retries': 15,
        'fragment_retries': 15,
        'socket_timeout': 30,
        'postprocessors': post_procs,
        'progress_hooks': [progress_hook],
        'ffmpeg_location': rf"ffmpeg/ffmpeg", #<<---Путь к ffmpeg
        'outtmpl': rf'{folder_name}/%(title)s.%(ext)s',
        'nocheckcertificate': True,
        'download_archive':rf'{folder_name}/archive.txt',
        'cookiefile': 'per.txt',#<<----Путь к файлам cookie
        'ignoreerrors':True,
        'add_metadata': True,
        'extractor_args': {
            'youtube': {
                'player_client': ['ios', 'android', 'tv'],
                'skip': ['web_music', 'web']
            }
        },
        'remote_components': ['ejs:github'], 
    }

    def run_download():
        target_links = []
        if url.get().strip():
            target_links.extend([l.strip() for l in url.get().split("\n") if l.strip()])
        if links_from_file.strip():
            target_links.extend([l.strip() for l in links_from_file.split("\n") if l.strip()])

        if not target_links:
            app.after(0, lambda: Download_status.configure(text="Нет ссылок для скачивания", text_color=COLOR_DANGER))
            return

        log.info(f"Запуск скачивания {len(target_links)} объектов")
        try:
            with yt_dlp.YoutubeDL(prop) as ydl:
                ydl.download(target_links)
            app.after(0, lambda: Download_status.configure(text="Все файлы готовы!", text_color="green"))
        except Exception as e:
            log.error(f"Ошибка в процессе скачивания: {e}")
            app.after(0, lambda: Download_status.configure(text="Ошибка при скачивании", text_color=COLOR_DANGER))

    threading.Thread(target=run_download, daemon=True).start()


customtkinter.set_appearance_mode("dark")
app = customtkinter.CTk()
app.title("YouTube Frosty Downloader")
app.geometry("600x650")
app.configure(fg_color=COLOR_BG)


tabview = customtkinter.CTkTabview(app, fg_color=COLOR_FRAME, 
                                   segmented_button_selected_color=COLOR_ACCENT,
                                   segmented_button_selected_hover_color="#f2aba1",
                                   segmented_button_unselected_hover_color=COLOR_HIGHLIGHT)
tabview.pack(padx=20, pady=20, fill="both", expand=True)
tabview.add("Скачать трек")


# Вкладка Скачать
tab_dl = tabview.tab("Скачать трек")
url = customtkinter.CTkEntry(tab_dl, placeholder_text="Ссылка", width=450, fg_color=COLOR_BG, border_color=COLOR_ACCENT)
url.pack(pady=15)
path_dir = customtkinter.CTkButton(tab_dl, text="Папка сохранения", width=450, fg_color=COLOR_BG, border_color=COLOR_ACCENT , command=choise_save)
path_dir.pack(pady=5)

q_frame = customtkinter.CTkFrame(tab_dl, fg_color="transparent")
q_frame.pack(pady=15)
cb1 = customtkinter.CTkCheckBox(q_frame, text="144p",fg_color="#160d0d", command=lambda: select_one("144p"))
cb2 = customtkinter.CTkCheckBox(q_frame, text="360p",fg_color="#160d0d", command=lambda: select_one("360p"))
cb3 = customtkinter.CTkCheckBox(q_frame, text="480p",fg_color="#160d0d", command=lambda: select_one("480p"))
cb4 = customtkinter.CTkCheckBox(q_frame, text="720p",fg_color="#160d0d", command=lambda: select_one("720p"))
cb5 = customtkinter.CTkCheckBox(q_frame, text="1080p",fg_color="#160d0d", command=lambda: select_one("1080p"))
cb6 = customtkinter.CTkCheckBox(q_frame, text="flac",fg_color="#160d0d", command=lambda: select_one("flac"))
cb6.select()
for i, cb in enumerate([cb1, cb2, cb3, cb4, cb5, cb6]):
    cb.grid(row=i//2, column=i%2, padx=20, pady=5 )

btn_group = customtkinter.CTkFrame(tab_dl, fg_color="transparent")
btn_group.pack(pady=10)
customtkinter.CTkButton(btn_group, text="📄 Файл со ссылками", fg_color=COLOR_ACCENT, text_color="#ffdad6", width=160, command=selectfile).pack(side="left", padx=10)
customtkinter.CTkButton(btn_group, text="🚀 СКАЧАТЬ", width=160, fg_color=COLOR_ACCENT, text_color="#ffdad6", font=("Arial", 14, "bold"), command=space).pack(side="left", padx=10)

Download_status = customtkinter.CTkLabel(tab_dl, text="Готов к работе", text_color=COLOR_TEXT)
Download_status.pack(pady=5)
File_status = customtkinter.CTkLabel(tab_dl, text="Файл не выбран", font=("Arial", 11, "italic"))
File_status.pack()


if __name__ == "__main__":
    
    app.mainloop()