import customtkinter
import os
import logging
from tkinter import filedialog
import yt_dlp
import threading
import sys
from pygame import mixer

save =""

COLOR_BG = "#1A1B26"         # Глубокий темный
COLOR_FRAME = "#24283B"      # Холодный синий фрейм
COLOR_HIGHLIGHT = "#3B4261"  # Цвет активного трека
COLOR_ACCENT = "#7AA2F7"     # Ледяной голубой
COLOR_TEXT = "#C0CAF5"       # Светлый текст
COLOR_DANGER = "#F7768E"     # Красный 

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

class MusicPlayer:
    def __init__(self, scrollside):
        self.scroll = scrollside
        self.queue = []      
        self.current_index = 0
        self.paused = False
        self.current_file = None
        self.song_widgets = [] 

    def play(self, file_path):
        if not file_path: return
        if file_path in self.queue:
            self.current_index = self.queue.index(file_path)
            
        try:
            mixer.music.stop()
            mixer.music.load(file_path)
            mixer.music.play()
            self.current_file = file_path
            self.paused = False
            self.highlight_current_track()
        except Exception as e:
            log.error(f"Ошибка воспроизведения: {e}")

    def highlight_current_track(self):
        for i, frame in enumerate(self.song_widgets):
            if i == self.current_index and self.current_file:
                frame.configure(fg_color=COLOR_HIGHLIGHT)
            else:
                frame.configure(fg_color=COLOR_FRAME)

    def play_next(self):
        if not self.queue: return
        self.current_index = (self.current_index + 1) % len(self.queue)
        self.play(self.queue[self.current_index])

    def play_back(self):
        if not self.queue: return
        self.current_index = (self.current_index - 1) % len(self.queue)
        self.play(self.queue[self.current_index])

    def toggle_pause(self):
        if not self.current_file: return
        if self.paused:
            mixer.music.unpause()
            self.paused = False
        else:
            mixer.music.pause()
            self.paused = True

    def start_from_beginning(self):
        if self.queue: self.play(self.queue[0])

    def paint(self):
        for child in self.scroll.winfo_children():
            child.destroy()
        
        global songs
        self.queue = list(songs) 
        self.song_widgets = [] 
        
        for path in self.queue:
            song_name = os.path.basename(path)
            song_frame = customtkinter.CTkFrame(self.scroll, fg_color=COLOR_FRAME)
            song_frame.pack(fill="x", padx=5, pady=2)
            self.song_widgets.append(song_frame)
            
            lbl = customtkinter.CTkLabel(song_frame, text=song_name, text_color=COLOR_TEXT, anchor="w")
            lbl.pack(side="left", padx=10, fill="x", expand=True)
            
            btn = customtkinter.CTkButton(
                song_frame, text="▶", width=40, 
                fg_color=COLOR_ACCENT, hover_color="#89B4FA", text_color=COLOR_BG,
                command=lambda p=path: self.play(p)
            )
            btn.pack(side="right", padx=5)
        self.highlight_current_track()


songs = []
links_from_file = ""

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def folder_scaner(folder_path):
    global songs 
    songs.clear()
    if os.path.exists(folder_path):
        for i in os.listdir(folder_path):
            if i.endswith(".mp3" ) and i.endswith(".flac" ) :
                songs.append(os.path.join(folder_path, i).replace("\\", "/"))
    player.paint()

def choise_folder():
    folder = filedialog.askdirectory(title="Выберите папку с музыкой")
    if folder:
        Folder_status.configure(text=folder)
        folder_scaner(folder)
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
    post_procs = [{'key': "EmbedThumbnail"}, {'key': "FFmpegMetadata"}]
    
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
        'ffmpeg_location': r"C:\ffmpeg\bin\ffmpeg.exe",  # <-- свой путь
        'outtmpl': rf'{folder_name}/%(title)s.%(ext)s',
        'nocheckcertificate': True,
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:148.0) Gecko/20100101 Firefox/148.0',
        'download_archive':rf'{folder_name}/archive.txt',
        'cookies':rf'Cookies.txt', # <-- свой путь
        'ignoreerrors':True,
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
mixer.init()

tabview = customtkinter.CTkTabview(app, fg_color=COLOR_FRAME, 
                                   segmented_button_selected_color=COLOR_ACCENT,
                                   segmented_button_selected_hover_color="#89B4FA",
                                   segmented_button_unselected_hover_color=COLOR_HIGHLIGHT)
tabview.pack(padx=20, pady=20, fill="both", expand=True)
tabview.add("Скачать трек")
tabview.add("Библиотека")

# Вкладка Скачать
tab_dl = tabview.tab("Скачать трек")
url = customtkinter.CTkEntry(tab_dl, placeholder_text="Ссылка", width=450, fg_color=COLOR_BG, border_color=COLOR_ACCENT)
url.pack(pady=15)
path_dir = customtkinter.CTkButton(tab_dl, text="Папка сохранения", width=450, fg_color=COLOR_BG, border_color=COLOR_ACCENT , command=choise_save)
path_dir.pack(pady=5)

q_frame = customtkinter.CTkFrame(tab_dl, fg_color="transparent")
q_frame.pack(pady=15)
cb1 = customtkinter.CTkCheckBox(q_frame, text="144p", command=lambda: select_one("144p"))
cb2 = customtkinter.CTkCheckBox(q_frame, text="360p", command=lambda: select_one("360p"))
cb3 = customtkinter.CTkCheckBox(q_frame, text="480p", command=lambda: select_one("480p"))
cb4 = customtkinter.CTkCheckBox(q_frame, text="720p", command=lambda: select_one("720p"))
cb5 = customtkinter.CTkCheckBox(q_frame, text="1080p", command=lambda: select_one("1080p"))
cb6 = customtkinter.CTkCheckBox(q_frame, text="flac", command=lambda: select_one("flac"))
cb6.select()
for i, cb in enumerate([cb1, cb2, cb3, cb4, cb5, cb6]):
    cb.grid(row=i//2, column=i%2, padx=20, pady=5)

btn_group = customtkinter.CTkFrame(tab_dl, fg_color="transparent")
btn_group.pack(pady=10)
customtkinter.CTkButton(btn_group, text="📄 Файл со ссылками", width=160, command=selectfile).pack(side="left", padx=10)
customtkinter.CTkButton(btn_group, text="🚀 СКАЧАТЬ", width=160, fg_color=COLOR_ACCENT, text_color=COLOR_BG, font=("Arial", 14, "bold"), command=space).pack(side="left", padx=10)

Download_status = customtkinter.CTkLabel(tab_dl, text="Готов к работе", text_color=COLOR_TEXT)
Download_status.pack(pady=5)
File_status = customtkinter.CTkLabel(tab_dl, text="Файл не выбран", font=("Arial", 11, "italic"))
File_status.pack()

# Вкладка Библиотека
tab_lib = tabview.tab("Библиотека")
lib_top = customtkinter.CTkFrame(tab_lib, fg_color="transparent")
lib_top.pack(fill="x", pady=10)
Folder_status = customtkinter.CTkLabel(lib_top, text="Выберите папку...", text_color=COLOR_TEXT, wraplength=250)
Folder_status.pack(side="left", padx=10)
customtkinter.CTkButton(lib_top, text="📁 Обзор", width=90, fg_color=COLOR_HIGHLIGHT, command=choise_folder).pack(side="right", padx=5)
customtkinter.CTkButton(lib_top, text="🔄 Обновить", width=90, fg_color=COLOR_HIGHLIGHT, command=lambda: player.paint()).pack(side="right", padx=5)

slidebar = customtkinter.CTkScrollableFrame(tab_lib, fg_color=COLOR_BG, border_color=COLOR_HIGHLIGHT, border_width=1)
slidebar.pack(fill="both", expand=True, padx=10, pady=10)
player = MusicPlayer(slidebar)

ctrls = customtkinter.CTkFrame(tab_lib, fg_color=COLOR_HIGHLIGHT, corner_radius=10)
ctrls.pack(fill="x", padx=10, pady=10)
customtkinter.CTkButton(ctrls, text="⏮", width=40, fg_color="transparent", command=player.play_back).pack(side="left", padx=10)
customtkinter.CTkButton(ctrls, text="⏸ / ▶", width=80, fg_color=COLOR_ACCENT, text_color=COLOR_BG, command=player.toggle_pause).pack(side="left", padx=5)
customtkinter.CTkButton(ctrls, text="⏭", width=40, fg_color="transparent", command=player.play_next).pack(side="left", padx=5)
customtkinter.CTkButton(ctrls, text="Сначала", width=80, fg_color="transparent", border_width=1, command=player.start_from_beginning).pack(side="right", padx=10)

if __name__ == "__main__":
    def check_music():
        if not mixer.music.get_busy() and player.current_file and not player.paused:
            player.play_next()
        app.after(1000, check_music)
    check_music()
    app.mainloop()
