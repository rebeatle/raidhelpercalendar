import os

# --- Access Token ---
with open('api.txt', 'r', encoding='utf-8') as f:
    ACCESS_TOKEN = f.read().strip()

# --- User API Key (opcional) ---
USER_API_KEY = None
if os.path.exists('api_key.txt'):
    with open('api_key.txt', 'r', encoding='utf-8') as f:
        USER_API_KEY = f.read().strip()

# --- Endpoints ---
ENDPOINT_AUTH    = "https://raid-helper.xyz/api/auth/{access_token}"
ENDPOINT_EVENTS  = "https://raid-helper.xyz/api/events/"
ENDPOINT_AGENDA  = "https://raid-helper.xyz/api/v4/users/{api_key}/events"
ENDPOINT_DETALLE = "https://raid-helper.xyz/api/event/{raid_id}"
