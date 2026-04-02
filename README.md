# Spanish Version 

> 🌐 [Versión en español](README.es.md)

# ⚔ Raid Helper Viewer (RHV)



A desktop dashboard to visualize all your Raid Helper events
across multiple Discord servers from a single screen.

> Built by [rebeatle](https://github.com/rebeatle) — because jumping between
> 14 Discord channels just to check the calendar is a raid by itself.

---

## What is this?

If you use Raid Helper across multiple Discord servers, you know the pain of
having to check channel by channel to see what raids are scheduled.

RHV solves that: a single screen with all your upcoming events, filters,
color coding by date proximity, and a mark showing which ones you're already signed up for.

![Main view](screenshots/main_view.png)
![launcher](screenshots/intro_2.png)

---

## Features

- 📅 **Unified view** of events from multiple servers
- 🔴🟡🟢 **Color by proximity** — today, tomorrow, this week
- ✅ **Mark your events** — instantly see where you're already signed up
- 🔍 **Filters** by period, server, and free text
- 📋 **Full event details** with role signups (Tanks, Healers, Melee, Ranged)
- ⌨️ **100% keyboard and mouse** — fast navigation

---

## Requirements

- Windows 10 or higher
- Python 3.10+ → [download here](https://www.python.org/downloads/)
  - ⚠️ During installation, check **"Add Python to PATH"**
- Discord account with access to servers using Raid Helper

---

## Installation

1. Download the repository as a ZIP and extract it to your desktop
2. Open the folder and double-click **`launcher.bat`**
3. The launcher installs dependencies automatically and guides you through setup

![launcher](screenshots/rhv_intro.png)

---

If you are an advanced user, it is recommended to create a `.env` and install these dependencies:
    pip install -r requirements.txt

    textual>=0.8.0
    requests>=2.28.0

Otherwise, just download the files and place them on your desktop. Don’t forget to install Python. The launcher will handle everything automatically.

---

## Initial Setup

The launcher will ask you for 3 things the first time:

### 1. Access Token
This is your session token from raid-helper.xyz. To obtain it:

1. Go to [raid-helper.xyz](https://raid-helper.xyz) and log in with Discord
2. Once inside, open the calendar of any server
3. Press `F12` to open DevTools
4. Go to the **Network** tab and filter by **Fetch/XHR**
5. Reload the page with `F5`
6. Look for a call named **`events/`**
7. Click it and go to the **Payload** tab
8. You will see something like:
```json
{"serverid":"...","accessToken":"YOUR_TOKEN_HERE"}
```
![f12](screenshots/f12.png)
9. Copy only the value of `accessToken` (the long string)

> ⚠️ This token is personal — do not share it with anyone.
> It expires over time. If the app stops showing events, repeat this process
> and update your `api.txt` with the new token (option C → Settings).

### 2. User API Key *(optional)*
Allows marking events with ✅ where you're already signed up.

1. In Discord, find the **Raid-Helper** bot in any server
2. Send it a direct message with: `/usersettings apikey show`
3. Copy the key it returns

If you don’t configure it, the app still works but without signup marks.

### 3. Discord Server IDs
The servers where you have Raid Helper active.

**How to get a server ID?**
1. In Discord, enable Developer Mode:
   `Settings → Advanced → Developer Mode ✅`
2. Right-click the server
3. Select **Copy Server ID**

You can enter them one by one or from a `.txt` file with one ID per line.

![dev mode](screenshots/dev_mode.png)
![Ids server](screenshots/id_server.png)

---

## Controls

| Key | Action |
|-----|--------|
| `↑` `↓` | Navigate events |
| `Enter` | View full event details |
| `R` | Reload data from API |
| `C` | Open settings menu |
| `V` | Add more servers |
| `Esc` | Close detail window |
| `Q` | Exit |

---

## Colors

| Color | Meaning |
|-------|---------|
| 🔴 Red | Event is today |
| 🟡 Yellow | Event is tomorrow |
| 🟢 Green | Event is this week |
| ⚪ White | Event is later |

---

## FAQ

**Why isn’t the app showing events?**
Most likely your Access Token has expired. Go to Settings (`C`) → option 1, and follow the steps to get a new token.

**Why don’t I see the ✅ on my events?**
You need to configure the User API Key. Go to Settings (`C`) → option 2.

**Does it work on Mac or Linux?**
`launcher.bat` is Windows-only. On Mac/Linux you can run
`python app.py` directly from the terminal, but setup must be done manually for now.

**Is it official? Does it have Raid Helper permission?**
This is not an official Raid Helper product. It uses the same API as the
raid-helper.xyz frontend with your personal session. Each user authenticates
with their own credentials. If Raid Helper changes its API, it may stop working until updated.

---

## Technical Notes

RHV replicates the calls made by the raid-helper.xyz frontend using
the Discord OAuth session `accessToken`. There is no publicly documented API —
this was discovered by observing the network traffic of the official website.

---

## Contributions

Pull requests are welcome. If something breaks due to changes in the Raid Helper API, open an issue.

---

## License

This project is licensed under **GNU GPL v3**.

You are free to use, study, and modify the code, but any distributed modified version must:
- Also be open source under GPL v3
- Give credit to the original author
- **Not be sold or used commercially** without explicit permission from the author

© 2026 [rebeatle](https://github.com/rebeatle) — All rights reserved under GPL v3.

For commercial use or special agreements, contact the author directly.
