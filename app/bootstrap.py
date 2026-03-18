import os

import telebot
from telebot import types
from dotenv import load_dotenv
from supabase import Client, create_client

from app import config
from app import db
from app.handlers import register_handlers


def create_bot() -> telebot.TeleBot:
    load_dotenv()

    token = (os.getenv('TELEGRAM_BOT_TOKEN') or '').strip()
    supabase_url = (os.getenv('SUPABASE_URL') or '').strip()
    supabase_service_role_key = (os.getenv('SUPABASE_SERVICE_ROLE_KEY') or '').strip()

    if not token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN missing in .env")

    if not supabase_url or not supabase_service_role_key:
        raise RuntimeError("Supabase credentials missing (SUPABASE_URL / SUPABASE_SERVICE_ROLE_KEY)")

    supabase: Client = create_client(supabase_url, supabase_service_role_key)

    if config.DEBUG:
        print(f"DEBUG mode enabled: broadcasts will use {config.USERS_TABLE} table")

    try:
        supabase.table(config.USERS_TABLE).select('user_id').limit(1).execute()
        print(f"Supabase connection established ({config.USERS_TABLE})")
    except Exception as e:  # noqa: BLE001
        print(f"Warning: Unable to query '{config.USERS_TABLE}' table. Ensure it exists before running the bot.")
        print(f"Supabase error: {e}")

    bot = telebot.TeleBot(token)
    try:
        bot.set_my_commands([
            types.BotCommand("start", "Start registration"),
        ])
    except Exception as exc:  # noqa: BLE001
        print(f"Warning: Unable to set default commands: {exc}")

    admin_commands = [
        types.BotCommand("all", "Send to all users"),
        types.BotCommand("year", "Send to a specific year"),
        types.BotCommand("lang", "Send to a specific language"),
        types.BotCommand("yearlang", "Send to year + language"),
        types.BotCommand("adminadd", "Add a master or year admin"),
        types.BotCommand("adminremove", "Remove a master or year admin"),
        types.BotCommand("adminlist", "List current admins"),
    ]

    year_admin_commands = [
        types.BotCommand("year", "Send to a specific year"),
        types.BotCommand("yearlang", "Send to year + language"),
    ]

    master_admins, year_admins = db.fetch_admins(supabase)
    year_admin_ids = set()
    for ids in year_admins.values():
        year_admin_ids.update(ids)

    for admin_id in master_admins:
        try:
            bot.set_my_commands(admin_commands, scope=types.BotCommandScopeChat(admin_id))
        except Exception as exc:  # noqa: BLE001
            print(f"Warning: Unable to set admin commands for {admin_id}: {exc}")

    for admin_id in year_admin_ids.difference(master_admins):
        try:
            bot.set_my_commands(year_admin_commands, scope=types.BotCommandScopeChat(admin_id))
        except Exception as exc:  # noqa: BLE001
            print(f"Warning: Unable to set year admin commands for {admin_id}: {exc}")
    register_handlers(bot, supabase)
    return bot
