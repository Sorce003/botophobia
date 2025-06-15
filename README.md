
# VC Dominator Userbot

[![Deploy to Heroku](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/Sorce003/botophobia)

A modern, feature-packed Pyrogram userbot for Telegram — manage voice chats, boost audio, moderate groups, and more with ease!

---

## ✨ Features

- Unlimited, crystal-clear audio amplification for Telegram Voice Chats (VC)
- Owner + Secondary Owner + SUDO system (edit `config.py` or Heroku vars anytime)
- Mass moderation: `.banall` and `.unbanall` (owner/sudo only)
- Modern, “sexy” DM welcome messages
- Toggle loop, autoloop, compression, dominance mode
- Heroku, local, or VPS deployment
- Easy, in-file config management

---

## 🚀 Quick Start

### 1. Fork/Clone This Repo

```bash
git clone https://github.com/Sorce003/botophobia.git
cd VC_Dominator_Userbot_Heroku
```

---

## 🛠 Configuration

Edit `config.py` or set environment variables (recommended for Heroku):

```python
API_ID = 1234567                    # Your Telegram API ID (int)
API_HASH = "your_api_hash_here"     # Your API hash (string)
STRING_SESSION = ""                 # (Recommended) Pyrogram session string
VC_CHAT_ID = ""                     # Optional: VC/group ID to join by default
SECONDARY_OWNER_ID = "111111111"    # Your secondary owner Telegram user ID (string)
SUDO_IDS = ["222222222", "333333333"]  # SUDO users (as strings/ints)
```

- **STRING_SESSION is safest for Heroku (see below for generation).**
- SUDO_IDS can be changed in `config.py` anytime.

---

## 🟣 Deploy to Heroku (Recommended, Easiest)

1. **[Generate your Pyrogram STRING_SESSION](#generate-string-session)**
2. **Click this button**:<br>
   [![Deploy to Heroku](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/Sorce003/botophobia)
3. **Fill in your API_ID, API_HASH, STRING_SESSION, etc. as config vars**
4. After deploy, go to Resources and enable the `worker` dyno
5. (Optional but recommended) Add the **Heroku apt buildpack** for FFmpeg:
    - Go to *Settings > Buildpacks*, add:  
      ```
      heroku-community/apt
      ```
    - Make sure your repo root has an `Aptfile` containing:
      ```
      ffmpeg
      ```

---

## 💻 Run Locally (PC/Linux/Mac)

1. Install requirements:
    ```bash
    pip install -r requirements.txt
    ```
2. Make sure you have **ffmpeg** installed (`sudo apt install ffmpeg`)
3. Edit `config.py` with your credentials
4. Run the bot:
    ```bash
    python userbot.py
    ```

---

## 🌐 Run on VPS (Ubuntu/Debian)

1. Install dependencies:
    ```bash
    sudo apt update && sudo apt install python3-pip ffmpeg git -y
    git clone https://github.com/Sorce003/botophobia.git
    cd VC_Dominator_Userbot_Heroku
    pip3 install -r requirements.txt
    ```
2. Edit `config.py`
3. Run:
    ```bash
    python3 userbot.py
    ```

---

## 🔐 Generate String Session

Run this on your local machine to generate a session string (recommended for Heroku):

soon will give the string session script
- Paste the result into your `config.py` or Heroku config var as `STRING_SESSION`.

---



## 🛡️ Security Notice

**Never use your personal/main Telegram account for userbot activities.**  
Use a dedicated or “throwaway” account. Both Telethon and Pyrogram userbots can be banned by Telegram if abused.

---

## 🤝 Credits

- [Pyrogram](https://github.com/pyrogram/pyrogram)
- [PyTgCalls](https://github.com/pytgcalls/pytgcalls)
- [pydub](https://github.com/jiaaro/pydub)
- Inspired by many open-source Telegram userbot projects
THE MAGICIAN 
---

## 💬 Support

Have questions, need help, or want to chat?  
Join our [Support Group](https://t.me/YourSupportGroup) on Telegram.

Open an issue or pull request for improvements, or contact the maintainer any time.

---

**Happy dominating VCs! 🎵🚀**
