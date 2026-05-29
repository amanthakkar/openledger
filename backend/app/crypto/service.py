from pathlib import Path


def import_cointracker_csv(path: str) -> bool:
    return Path(path).exists()
