import os
from typing import Any
from urllib import parse
from xml.etree import ElementTree


def get_mod_id_from_url(mod_url: Any) -> int:
    if isinstance(mod_url, int):
        return mod_url

    if not isinstance(mod_url, str):
        raise ValueError(f"Это не строка: {mod_url}")

    if mod_url.isdecimal():
        return int(mod_url)

    parsed_url = parse.urlparse(mod_url)
    qs = parse.parse_qs(parsed_url.query)
    try:
        return int(qs["id"][0])
    except KeyError:
        raise ValueError(f"Невозможно получить Mod ID из {mod_url}")


def get_workshop_game_id_from_url(workshop_game_url: Any) -> int:
    if not isinstance(workshop_game_url, str):
        raise ValueError(f"Это не строка: {workshop_game_url}")

    try:
        parsed_url = parse.urlparse(workshop_game_url)
        for path in parsed_url.path.split("/"):
            if path.isdecimal():
                return int(path)
    except KeyError:
        raise ValueError(f"Невозможно получить App ID из {workshop_game_url}")


def rename_mods_folder(mods_folder):
    for folder_name in os.listdir(mods_folder):
        folder_path = os.path.join(mods_folder, folder_name)
        if not os.path.isdir(folder_path):
            continue

        about_folder_path = os.path.join(folder_path, "About")
        about_file_path = os.path.join(about_folder_path, "About.xml")

        if not os.path.exists(about_file_path):
            print(f'No About.xml found in "{folder_path}". Skipping.')
            continue

        try:
            tree = ElementTree.parse(about_file_path)
            root = tree.getroot()

            name_tag = root.find("name")
            if name_tag is None or not name_tag.text:
                print(f'No <name> tag found in "{about_file_path}". Skipping.')
                continue

            mod_name = name_tag.text.strip()
            new_folder_path = os.path.join(mods_folder, mod_name)
            if not os.path.exists(new_folder_path):
                os.rename(folder_path, new_folder_path)
        except ElementTree.ParseError as error:
            print(f'Error parsing XML in "{about_file_path}": {error}')
