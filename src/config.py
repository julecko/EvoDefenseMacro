from pathlib import Path


def _load_dotenv(dotenv_path: Path) -> dict[str, str]:
    if not dotenv_path.exists():
        return {}

    env_vars: dict[str, str] = {}
    with dotenv_path.open("r", encoding="utf-8") as dotenv_file:
        for line in dotenv_file:
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            if "=" not in stripped:
                continue

            key, value = stripped.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"\'')
            env_vars[key] = value

    return env_vars


_project_root = Path(__file__).resolve().parent.parent
_env = _load_dotenv(_project_root / ".env")

WINDOW_NAME = _env.get("WINDOW_NAME", "BlueStacks App Player")
LOCKED_WIDTH = int(_env.get("LOCKED_WIDTH", "540"))
LOCKED_HEIGHT = int(_env.get("LOCKED_HEIGHT", "960"))
ADB_PATH = _env.get("ADB_PATH", "adb")
ADB_HOST = _env.get("ADB_HOST", "127.0.0.1:5555")
TEMPLATES_FOLDER_NAME = _env.get("TEMPLATES_FOLDER_NAME", "templates")
