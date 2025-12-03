import os
from pathlib import Path

def get_project_root() -> str:

    return str(Path.cwd().parents[1])

def get_database_path(db_name: str = "fm_estatistica.db") -> str:
    return os.path.join(get_project_root(), "data", "db", db_name)


def get_raw_data_path(file_name: str) -> str:
    return os.path.join(get_project_root(), "data", "raw", file_name)

