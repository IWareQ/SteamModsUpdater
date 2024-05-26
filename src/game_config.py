import os
from dataclasses import dataclass
from pathlib import Path
from typing import Union, Optional

import yaml
from schema import Schema, And, Use, SchemaError

from src.utils import get_mod_id_from_url, get_workshop_game_id_from_url


@dataclass(frozen=True, eq=True)
class GameConfig:
    download_path: Path
    game_id: int
    mods_id: set[int]


config_validation_schema = Schema(
    {
        "download_path": And(str, len),
        "workshop_game_url": Use(get_workshop_game_id_from_url),
        "mods": [Use(get_mod_id_from_url)],
    },
)


def get_configs(dir_path: Path) -> list[GameConfig]:
    print(f"Загрузка конфигов из {dir_path}")
    configs: list[GameConfig] = []
    if not dir_path.exists():
        dir_path.mkdir()

    for file_path in os.listdir(dir_path):
        if not os.path.isfile(dir_path / file_path):
            continue

        filename, file_extension = os.path.splitext(dir_path / file_path)
        if file_extension not in {".yml", ".yaml"}:
            continue

        filename, _ = os.path.splitext(file_path)
        if filename.startswith("!"):
            continue

        print(f"Загрузка конфига {filename + file_extension}")
        cfg = _get_config(dir_path / file_path, filename)
        if cfg is not None:
            configs.append(cfg)

    return configs


def _get_config(
        filepath: Union[str, os.PathLike], config_name: str
) -> Optional[GameConfig]:
    with open(filepath, encoding="utf-8") as cfg_file:
        cfg_data = yaml.safe_load(cfg_file)

    try:
        cfg_data = config_validation_schema.validate(cfg_data)
    except SchemaError as error:
        print(f"Конфиг {config_name} неверный!", error)
        return None

    unique_mods_id: set[int] = set()
    for mod in cfg_data["mods"]:
        unique_mods_id.add(mod)

    return GameConfig(Path(cfg_data["download_path"]), cfg_data["workshop_game_url"], unique_mods_id)
