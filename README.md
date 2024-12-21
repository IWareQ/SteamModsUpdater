## Что это такое

Данная программа позволяет скачивать указанные пользователем моды из "Steam Workshop" и затем автоматически
распаковывать архивы в указанную им же папку.

Для добавления списка модов для определённой игры создайте файл `название_игры.yml` в папке `configs/` и укажите путь к
папке где должны храниться моды.

## Как собрать в exe?
```bash
pyinstaller.exe .\main.py --onefile --name SteamModsUpdater
```
Исполняемый файл появится в папке `dist`

## Пример конфига для RimWorld

В папке `configs/` файл `rimworld.yml` имеет следующее содержание:

```yml
# Путь куда будут скачиваться моды, вместо ИМЯ_ПОЛЬЗОВАТЕЛЯ укажите свое
download_path: C:\Users\ИМЯ_ПОЛЬЗОВАТЕЛЯ\Games\RimWorld\Mods

# Ссылка на мастерскую игры
# например https://steamcommunity.com/app/294100/workshop/ - это RimWorld
workshop_game_url: https://steamcommunity.com/app/294100/workshop/

# Ссылки на моды или их ID
# Например https://steamcommunity.com/sharedfiles/filedetails/?id=818773962 - это HugsLib
mods:
  - "818773962" # HugsLib
  - "https://steamcommunity.com/sharedfiles/filedetails/?id=1127530465" # Dubs Rimatomics
  - "https://steamcommunity.com/sharedfiles/filedetails/?id=2009463077" # Harmony
```

> [!IMPORTANT]
> Если название файла будет начинаться с `!`, то он будет проигнорирован!
>
> Например `!rimworld.yml`
>
> Таким образом вы можете отключать ненужные вам игры, но сохранять их файлы

Таким образом, будут скачаны архивы всех перечисленных модов, а затем распакованы по
пути `C:\Users\ИМЯ_ПОЛЬЗОВАТЕЛЯ\Games\RimWorld\Mods` в отдельные папки.

## Скачать и запустить

Перейдите в [сюда](https://github.com/IWareQ/SteamModsUpdater/tree/master/dist), скачайте и запустите
файл `SteamModsUpdater.exe`