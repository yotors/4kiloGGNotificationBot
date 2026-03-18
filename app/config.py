import json
import os

from dotenv import load_dotenv

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
CONFIG_PATH = os.path.join(BASE_DIR, 'config.json')
TRANSLATIONS_PATH = os.path.join(BASE_DIR, 'translations.json')

load_dotenv()

def _load_config_file() -> dict:
    try:
        with open(CONFIG_PATH, 'r', encoding='utf-8') as config_file:
            return json.load(config_file)
    except FileNotFoundError as exc:
        raise RuntimeError("config.json not found. Please add it next to bot.py.") from exc
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"config.json contains invalid JSON: {exc}") from exc


CONFIG = _load_config_file()


def _clean_str_list(values):
    cleaned: list[str] = []
    for value in values or []:
        text = str(value).strip()
        if text:
            cleaned.append(text)
    return cleaned


def _parse_bool_env(value: str | None) -> bool | None:
    if value is None:
        return None

    cleaned = value.strip().lower()
    if cleaned in {'1', 'true', 'yes', 'on'}:
        return True
    if cleaned in {'0', 'false', 'no', 'off'}:
        return False
    return None


options_config = CONFIG.get('options')
if not isinstance(options_config, dict):
    raise RuntimeError("config.json must include an 'options' object.")

raw_genders = _clean_str_list(options_config.get('genders'))
if not raw_genders:
    raise RuntimeError("config.json must include non-empty options.genders.")
GENDER_OPTIONS: tuple[str, ...] = tuple(raw_genders)

raw_departments = _clean_str_list(options_config.get('departments'))
if not raw_departments:
    raise RuntimeError("config.json must include non-empty options.departments.")
DEPARTMENTS: tuple[str, ...] = tuple(raw_departments)

raw_years = options_config.get('years')
if not isinstance(raw_years, list) or not raw_years:
    raise RuntimeError("config.json must include non-empty options.years.")
processed_years: list[int] = []
for entry in raw_years:
    try:
        processed_years.append(int(entry))
    except (TypeError, ValueError):
        continue
if not processed_years:
    raise RuntimeError("config.json options.years must contain valid integers.")
YEAR_CHOICES: tuple[int, ...] = tuple(processed_years)

configured_default_language = str(options_config.get('default_language', '')).strip()

debug_from_env = _parse_bool_env(os.getenv('DEBUG'))
if debug_from_env is None:
    DEBUG = bool(options_config.get('debug', False))
else:
    DEBUG = debug_from_env

USERS_TABLE = 'demo_users' if DEBUG else 'users'

try:
    with open(TRANSLATIONS_PATH, 'r', encoding='utf-8') as translations_file:
        TRANSLATIONS = json.load(translations_file)
except FileNotFoundError as exc:
    raise RuntimeError("translations.json not found. Please add it next to bot.py.") from exc
except json.JSONDecodeError as exc:
    raise RuntimeError(f"translations.json contains invalid JSON: {exc}") from exc

LANGUAGE_OPTIONS = list(TRANSLATIONS.keys())
if not LANGUAGE_OPTIONS:
    raise RuntimeError("translations.json must contain at least one language entry.")

if not configured_default_language:
    raise RuntimeError("config.json options.default_language is required.")
if configured_default_language not in LANGUAGE_OPTIONS:
    raise RuntimeError(
        "config.json options.default_language must match a key in translations.json."
    )
DEFAULT_LANGUAGE = configured_default_language
