import shutil
from pathlib import Path

from pysteamcmdwrapper import SteamCMD, SteamCMDException, SteamCMD_command

from src.config import STEAM_CMD_PATH, TEMP_DOWNLOAD_PATH
from src.game_config import get_configs
from src.utils import rename_mods_folder


def done():
    print("Используйте Ctrl + C чтобы закрыть")
    while True:
        pass


if __name__ == '__main__':
    if not STEAM_CMD_PATH.exists():
        STEAM_CMD_PATH.mkdir()

    steam_cmd = SteamCMD(STEAM_CMD_PATH)
    try:
        steam_cmd.install()
    except SteamCMDException:
        pass  # SteamCMD already installed

    steam_cmd.login("anonymous", "anonymous")

    sc = SteamCMD_command()
    sc.force_install_dir(TEMP_DOWNLOAD_PATH)

    game_configs = get_configs(Path("configs/"))
    if len(game_configs) == 0:
        print("Конфиги не найдены!")
        done()

    for game_config in game_configs:
        for mod_id in game_config.mods_id:
            sc.workshop_download_item(game_config.game_id, mod_id, True)

        steam_cmd.execute(sc, 5)

    temp_swc = TEMP_DOWNLOAD_PATH / "steamapps" / "workshop" / "content"
    for game_config in game_configs:
        download_path = Path(game_config.download_path)
        if not download_path.exists():
            download_path.mkdir()

        temp_mods_path = temp_swc / str(game_config.game_id)
        rename_mods_folder(temp_mods_path)
        try:
            shutil.copytree(temp_mods_path, download_path, dirs_exist_ok=True)
        except IOError as error:
            print("Unable to copy file.", error)

    shutil.rmtree(TEMP_DOWNLOAD_PATH)
    done()
