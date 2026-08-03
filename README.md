# YouTubeDownloader
Установщик видео и аудио с YouTube и иных стриммингов.
Для работы кода потребуется [python 3.14+](https://www.python.org/downloads/).
Пакет библиотек: pygame , customtkinter , yt_dlp , mutagen
___
Установка разом: 
```bash
pip install pygame-ce yt_dlp  customtkinter mutagen
````
Устанока по одной:
```bash
pip install pygame-ce
pip install yt_dlp
pip install customtkinter
pip install mutagen
`````
___
Так же понадобиться программа ffmpeg [ссылка](https://www.ffmpeg.org/). Установленные пакеты нужно будет положить в одну папку с python файлом.
В строке 203 нужно прописать путь к ffmpeg.exe(если windows) или просто ffmpeg(если unix подобная система).
Для стабильной работы программы потребуется создать файл Cookies.txt и в строке 208  прописать к ней путь.
В файл Cookies.txt, важно добавить куки из своего браузера , получить нужный формат можно с помощью расширения [Cookies.txt](https://github.com/hrdl-github/cookies-txt) или иных расширений. Главное чтобы формат кук был  Netscape , установив расширение зайдите на сайт с которого хотите скачивать контент и скопируйте куки с сайта или все куки. После чего в txt файл нужно будет вставить скопированные данные.

___
Основной интерфейс:
<img width="1918" height="1078" alt="изображение" src="https://github.com/user-attachments/assets/327cf818-8e53-4309-aa4b-1353b5e13213" />
Программа имеет фукцию аудио плеера , но работает с переменным успехом и только на mp3 формате, сама функция не обновлялась с самого добавления:
<img width="959" height="1038" alt="изображение" src="https://github.com/user-attachments/assets/04918f73-5fb4-4b12-8dc0-2d14b2c092fe" />
