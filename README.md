# Telegram Registration Bot

A Telegram bot for student registration with Supabase storage and multilingual prompts.

## Features
- Language-first onboarding flow
- Collects name, gender, department, year, and preferred language
- Admin broadcasts to all students or a specific year
- Config-driven options and admin roles

## Setup
1. Create a `.env` file with:
   - `TELEGRAM_BOT_TOKEN`
   - `SUPABASE_URL`
   - `SUPABASE_SERVICE_ROLE_KEY`
2. Update `config.json` with your admin IDs and options.
3. Ensure `translations.json` has your desired languages and prompt keys.

## Install
```bash
python -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt
```

## Run

# Telegram Registration Bot

A lightweight Telegram bot specifically for 4Kilo Gibi Gubae to register students (name, gender, department, year, preferred language) and send targeted broadcasts. Data is stored in a Supabase table.

**Features**
- Language-first onboarding with multilingual prompts
- Collects `name`, `gender`, `department`, `year`, and `preferred_language`
- Admin broadcast commands with optional filters: gender, department, year, language
- Config-driven: `config.json` centralizes admin IDs and allowed options

**Prerequisites**
- Python 3.10+ (use the project virtualenv to avoid system-package issues)
- A Supabase project and a `users` table with columns: `user_id`, `name`, `gender`, `department`, `year`, `preferred_language`
- A Telegram bot token (`TELEGRAM_BOT_TOKEN`) from BotFather

**Setup**
1. create `.env` and set the following environment variables:
   - `TELEGRAM_BOT_TOKEN`
   - `SUPABASE_URL`
   - `SUPABASE_SERVICE_ROLE_KEY`
2. Edit `config.json` to add your `MASTER_ADMINS`, `YEAR_ADMINS`, and options (`years`, `genders`, `departments`, `default_language`).
3. Verify `translations.json` contains keys for the languages you want to support.

**Install**
```bash
python -m venv .venv
# On Git Bash / WSL / Linux/macOS
source .venv/Scripts/activate
# On Windows PowerShell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

**Run**
```bash
source .venv/Scripts/activate   # or use the appropriate activate command for your shell
python bot.py
```

**Admin Broadcasts**
- `/all [<GENDER>] [<DEPARTMENT>] <message>` — send to all registered users, optional gender/department prefix filters.
- `/year <year> [<GENDER>] [<DEPARTMENT>] <message>` — send to a specific year.
- `/lang <language> [<GENDER>] [<DEPARTMENT>] <message>` — send to users with a preferred language (supports multi-word language names).
- `/yearlang <year> <language> [<GENDER>] [<DEPARTMENT>] <message>` — combined year+language targeting.

Notes about command arguments:
- Language names support spaces (for example: "Afan Oromo") and are matched using the longest-prefix strategy. If a language contains spaces, you can pass it directly without quotes.
- Prefix filters (gender, department) are optional and order-insensitive. Gender values must match one of the canonical values in `config.json`.
- Use `{name}` in the message body to personalize broadcasts (the placeholder will be replaced with each recipient's name).

**Permissions & per-chat commands**
- The bot attempts to register per-admin chat commands, but Telegram only allows setting chat-specific commands for chats the bot has already seen. Ask each admin to start a chat with the bot (send `/start`) before expecting per-chat command suggestions.

**Development notes**
- Config-driven options are in `config.json` and translations in `translations.json`.
- Database helpers are in `app/db.py`; handlers live in `app/handlers.py`.

