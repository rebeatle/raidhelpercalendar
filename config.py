import os

# --- Access Token (sesión de raid-helper) ---
with open('api.txt', 'r', encoding='utf-8') as f:
    ACCESS_TOKEN = f.read().strip()

# --- User API Key (agenda personal, opcional) ---
USER_API_KEY = None
if os.path.exists('api_key.txt'):
    with open('api_key.txt', 'r', encoding='utf-8') as f:
        USER_API_KEY = f.read().strip()

# --- Servidores ---
MIS_SERVIDORES = [
  "1374406840179232838"
]
""" ,"1041361547991208048", "703326394234568785",
    "883885047604711475",  "1459468417923813451", "1282514878262804621", "833645497473433610",
    "1465636323611119649", "1374406840179232838", "1313151590206803998", "918730780467941376",
    "936312188484874310",  "1436625771870294088" """

# --- Endpoints ---
ENDPOINT_EVENTS  = "https://raid-helper.xyz/api/events/"
ENDPOINT_AGENDA  = "https://raid-helper.xyz/api/v4/users/{api_key}/events"