# Telegram Registration Bot

A lightweight Telegram bot for 4Kilo Gibi Gubae to register students and send targeted broadcasts. Data is stored in a Supabase table.

## Features
- Language-first onboarding with multilingual prompts
- Collects `name`, `gender`, `department`, `year`, and `preferred_language`
- Admin broadcast commands with optional filters: gender, department, year, language
- Config-driven: `config.json` centralizes bot options

## Prerequisites
- Python 3.10+
- A Supabase project with a `users` table (columns: `user_id`, `name`, `gender`, `department`, `year`, `preferred_language`)
- A Telegram bot token (`TELEGRAM_BOT_TOKEN`) from BotFather

## Setup
1. Create `.env` and set:
   - `TELEGRAM_BOT_TOKEN`
   - `SUPABASE_URL`
   - `SUPABASE_SERVICE_ROLE_KEY`
2. Add `admin_role` to the Supabase `users` table (enum-like text values: `master`, `1`, `2`, `3`, `4`, `none`).
3. Edit `config.json` to set options (`years`, `genders`, `departments`, `default_language`).
4. Verify `translations.json` contains keys for the languages you want to support.

## Debug Broadcast Mode
- Enable safe broadcast testing using either:
   - `.env` override: `DEBUG=true` (recommended for quick toggling), or
   - `config.json`: `options.debug: true`
- When `DEBUG=true`, the bot uses the `demo_users` table instead of `users` in the same database.
- The bot logs `DEBUG mode enabled: broadcasts will use demo_users table` on startup.

## Install
```bash
python -m venv .venv
# Git Bash / WSL / Linux/macOS
source .venv/Scripts/activate
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Run
```bash
source .venv/Scripts/activate
python bot.py
```

## Admin Broadcasts
- `/all [<GENDER>] [<DEPARTMENT>] <message>` — send to all users.
- `/year <year> [<GENDER>] [<DEPARTMENT>] <message>` — filter by year.
- `/lang <language> [<GENDER>] [<DEPARTMENT>] <message>` — filter by preferred language (multi-word supported).
- `/yearlang <year> <language> [<GENDER>] [<DEPARTMENT>] <message>` — filter by year + language.

Notes:
- Language names support spaces (example: "Afan Oromo").
- Prefix filters (gender, department) are optional and order-insensitive.
- Use `{name}` in the message body to personalize broadcasts.

## Admin Management
- `/adminadd <user_id> master` — add a master admin (or reply to a user and omit `<user_id>`).
- `/adminadd <user_id> year <year>` — add a year admin for a specific year.
- `/adminremove <user_id> master|year <year>|all` — remove a user from admin roles (sets `admin_role` to `none`).
- `/adminlist` — list current admins.

## Permissions & per-chat commands
- Telegram only allows per-chat command registration after the admin has started a chat with the bot. Ask each admin to send `/start` once.

## Development notes
- Config options live in `config.json`, translations in `translations.json`.
- Database helpers are in `app/db.py`, handlers in `app/handlers.py`.

