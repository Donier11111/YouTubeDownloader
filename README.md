# YouTubeDownloader
Установщик видео и аудио с YouTube и иных стриммингов.
Для работы кода потребуется [python 3.14+](https://www.python.org/downloads/).
Пакет библиотек: pygame , customtkinter , yt_dlp , mutagen
___
Установка разом: 
```bash
pip install yt_dlp  customtkinter mutagen
````
Устанока по одной:
```bash

pip install yt_dlp
pip install customtkinter
pip install mutagen
```

``
|  | Название | Назначение |
|--|----------|------------|
| [<img src="https://www.python.org/static/favicon.ico" width="16">](https://www.python.org/downloads/) | [Python 3.14+](https://www.python.org/downloads/) | Интерпретатор |
| [<img src="https://raw.githubusercontent.com/yt-dlp/yt-dlp/master/.github/assets/icon.svg" width="16">](https://github.com/yt-dlp/yt-dlp) | [yt-dlp](https://github.com/yt-dlp/yt-dlp) | Загрузка контента |
| [<img src="https://ffmpeg.org/favicon.ico" width="16">](https://ffmpeg.org/) | [FFmpeg](https://ffmpeg.org/) | Конвертация аудио/видео |
| [<img src="https://customtkinter.tomschimansky.com/img/customtkinter_icon.png" width="16">](https://github.com/TomSchimansky/CustomTkinter) | [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) | Графический интерфейс |

___
Так же понадобиться программа ffmpeg [ссылка](https://www.ffmpeg.org/). Установленные пакеты нужно будет положить в одну папку с python файлом.
В строке 203 нужно прописать путь к ffmpeg.exe(если windows) или просто ffmpeg(если unix подобная система).
Для стабильной работы программы потребуется создать файл Cookies.txt и в строке 207  прописать к ней путь.
В файл Cookies.txt, важно добавить куки из своего браузера , получить нужный формат можно с помощью расширения [Cookies.txt](https://github.com/hrdl-github/cookies-txt) или иных расширений. Главное чтобы формат кук был  Netscape , установив расширение зайдите на сайт с которого хотите скачивать контент и скопируйте куки с сайта или все куки. После чего в txt файл нужно будет вставить скопированные данные.

___
Основной интерфейс:
<img width="1918" height="1078" alt="изображение" src="https://github.com/user-attachments/assets/327cf818-8e53-4309-aa4b-1353b5e13213" />
Функция плеера была вырезана.
