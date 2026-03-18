from typing import Any, Dict, Optional

from supabase import Client

from . import config


def fetch_users(supabase: Client, filters: Optional[Dict[str, Any]] = None) -> list[dict[str, Any]]:
    query = supabase.table(config.USERS_TABLE).select('user_id,name')
    if filters:
        for key, value in filters.items():
            query = query.eq(key, value)
    response = query.execute()
    return response.data if getattr(response, 'data', None) else []


def save_user_to_db(
    supabase: Client,
    user_id: int,
    name: str | None,
    gender: str | None,
    dept: str | None,
    year: int | None,
    preferred_language: str | None,
) -> None:
    try:
        response = supabase.table(config.USERS_TABLE).upsert({
            'user_id': user_id,
            'name': name,
            'gender': gender,
            'department': dept,
            'year': year,
            'preferred_language': preferred_language,
        }).execute()
        if getattr(response, 'error', None):
            print(f"Supabase upsert error: {response.error}")
    except Exception as e:  # noqa: BLE001
        print(f"Supabase save error: {e}")


def get_admin_role(supabase: Client, user_id: int) -> str:
    try:
        response = (
            supabase.table(config.USERS_TABLE)
            .select('admin_role')
            .eq('user_id', user_id)
            .limit(1)
            .execute()
        )
        if getattr(response, 'data', None):
            role = response.data[0].get('admin_role')
            return str(role).strip().lower() if role else 'none'
    except Exception as e:  # noqa: BLE001
        print(f"Supabase admin role fetch error: {e}")
    return 'none'


def set_admin_role(supabase: Client, user_id: int, role: str) -> bool:
    try:
        response = supabase.table(config.USERS_TABLE).upsert({
            'user_id': user_id,
            'admin_role': role,
        }).execute()
        if getattr(response, 'error', None):
            print(f"Supabase admin role update error: {response.error}")
            return False
        return True
    except Exception as e:  # noqa: BLE001
        print(f"Supabase admin role update error: {e}")
        return False


def fetch_admins(supabase: Client) -> tuple[set[int], dict[int, set[int]]]:
    master_ids: set[int] = set()
    year_admins: dict[int, set[int]] = {}

    try:
        response = supabase.table(config.USERS_TABLE).select('user_id,admin_role').execute()
    except Exception as e:  # noqa: BLE001
        print(f"Supabase admin list error: {e}")
        return master_ids, year_admins

    rows = response.data if getattr(response, 'data', None) else []
    for row in rows:
        user_id = row.get('user_id')
        role = (row.get('admin_role') or 'none')
        role_text = str(role).strip().lower()
        if not user_id or role_text == 'none':
            continue
        if role_text == 'master':
            master_ids.add(int(user_id))
        elif role_text.isdigit():
            year = int(role_text)
            year_admins.setdefault(year, set()).add(int(user_id))

    return master_ids, year_admins
