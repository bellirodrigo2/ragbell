from pathlib import Path


def extract_filename(path: str) -> str:
    return Path(path).stem
