import os


def is_debug() -> bool:
    return os.environ.get("LUMIGO_DEBUG", "").lower() == "true"
