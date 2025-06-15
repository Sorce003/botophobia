from pyrogram import Client, filters
import os
import random
import asyncio
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from utils.audio_tools import process_audio
from config import API_ID, API_HASH, VC_CHAT_ID, STRING_SESSION, SECONDARY_OWNER_ID, SUDO_IDS

# --- Auto-compatible imports for PyTgCalls 1.x and 2.x+ ---
try:
    from pytgcalls import PyTgCalls
    from pytgcalls.types.input_stream import AudioPiped
    from pytgcalls.types import StreamType
except ImportError:
    # Fallback for pytgcalls 1.x
    from pytgcalls import PyTgCalls, StreamType
    from pytgcalls.types import AudioPiped

# ---- Session Setup (String Session or API ID/HASH) ----
if STRING_SESSION and STRING_SESSION.strip():
    app = Client(
        name="userbot",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=STRING_SESSION
    )
else:
    app = Client(
        name="userbot",
        api_id=API_ID,
        api_hash=API_HASH
    )

pytg = PyTgCalls(app)

loop_enabled = False
autoloop_enabled = False
dominance_mode = False
compression_enabled = False
current_audio = None
chat_id = VC_CHAT_ID

def is_owner(user_id, client=None):
    try:
        main_owner_id = str(client.me.id) if client and hasattr(client, "me") else None
    except:
        main_owner_id = None
    return str(user_id) == str(SECONDARY_OWNER_ID) or (main_owner_id and str(user_id) == main_owner_id)

def is_sudo(user_id, client=None):
    return is_owner(user_id, client) or str(user_id) in [str(i) for i in SUDO_IDS]

# ----------- Command Handlers ------------

@app.on_message(filters.private & filters.command("setvc", prefixes="."))
async def set_vc(client, message: Message):
    if not is_owner(message.from_user.id, client):
        return await message.reply("❌ Unauthorized")
    global chat_id
    parts = message.text.split(maxsplit=1)
    if len(parts) != 2:
        return await message.reply("Usage: `.setvc <chat_id or @username>`")
    chat_id = parts[1]
    await message.reply(f"✅ VC chat set to: `{chat_id}`")

@app.on_message(filters.private & filters.command("play", prefixes="."))
async def play_audio(client, message: Message):
    global current_audio
    if not message.reply_to_message or not message.reply_to_message.audio:
        return await message.reply("Reply to an audio with `.play <multiplier>` (e.g. `.play 2`, `.play 25`)")
    try:
        multiplier = float(message.text.split()[1])
        if multiplier <= 0:
            return await message.reply("Multiplier must be positive, e.g. `.play 2`")
    except:
        return await message.reply("Usage: `.play <multiplier>`, e.g. `.play 2`, `.play 10`")

    file_path = await message.reply_to_message.download()
    boosted_path = process_audio(file_path, multiplier, compression_enabled, dominance_mode)
    current_audio = boosted_path

    await pytg.join_group_call(
        chat_id,
        AudioPiped(boosted_path),
        stream_type=StreamType().local_stream
    )
    await message.reply(f"▶️ Playing at {multiplier}x amplification (max clarity, auto-normalized).")

@app.on_message(filters.private & filters.command("stop", prefixes="."))
async def stop_audio(_, message: Message):
    await pytg.leave_group_call(chat_id)
    await message.reply("⏹️ Stopped playback and left VC.")

@app.on_message(filters.private & filters.command("loop", prefixes="."))
async def toggle_loop(_, message: Message):
    global loop_enabled
    cmd = message.text.split()
    if len(cmd) > 1 and cmd[1].lower() == "on":
        loop_enabled = True
        await message.reply("🔁 Looping enabled.")
    elif len(cmd) > 1 and cmd[1].lower() == "off":
        loop_enabled = False
        await message.reply("🔂 Looping disabled.")
    else:
        await message.reply("Usage: `.loop on` / `.loop off`")

@app.on_message(filters.private & filters.command("autoloop", prefixes="."))
async def toggle_autoloop(_, message: Message):
    global autoloop_enabled
    autoloop_enabled = not autoloop_enabled
    status = "enabled" if autoloop_enabled else "disabled"
    await message.reply(f"🔁 Auto-loop is now {status}.")

@app.on_message(filters.private & filters.command("compress", prefixes="."))
async def toggle_compress(_, message: Message):
    global compression_enabled
    compression_enabled = not compression_enabled
    status = "enabled" if compression_enabled else "disabled"
    await message.reply(f"🎚️ Compression {status}.")

@app.on_message(filters.private & filters.command("dominance", prefixes="."))
async def toggle_dominance(_, message: Message):
    global dominance_mode
    dominance_mode = not dominance_mode
    status = "enabled" if dominance_mode else "disabled"
    await message.reply(f"👑 Dominance mode {status}.")

@app.on_message(filters.private & filters.command("ping", prefixes="."))
async def ping(_, message: Message):
    await message.reply("🏓 Pong! Bot is alive.")

@app.on_message(filters.private & filters.command("help", prefixes="."))
async def help_command(client, message):
    help_text = """
🤖 **Userbot Command List**

🎵 **Audio Control**
.play <multiplier> – Play & boost replied audio (`.play 1` = normal, `.play 10` = 10x louder, etc.)
.stop – Stop playback and leave VC
.loop on / .loop off – Enable/Disable repeat of current audio
.autoloop – Toggle infinite auto-replay

🎚️ **Audio Enhancer**
.compress – Toggle voice compression (radio-style boost)

👑 **Control & Dominance**
.dominance – Toggle dominance mode (VC priority audio)
.ping – Check if bot is alive
.setvc <chat_id or @username> – Set group VC to join (private/public)

🛡️ **Group Moderation**
.banall – Ban all non-admins in the group (sudo/owner only)
.unbanall – Unban all banned users in the group (sudo/owner only)

📘 **This Help**
.help – Show this command list
"""
    await message.reply_text(help_text.strip())

# ----------- Sexy Welcome Message ------------

welcome_messages = [
    "😏 Well, hello there.",
    "✨ You made it. This just got interesting.",
    "👀 Someone cool just showed up.",
    "🔥 New vibe detected. Ready when you are.",
    "😉 Didn’t expect you, but I’m glad you’re here."
]

@app.on_message(filters.private & ~filters.me)
async def sexy_welcome(client, message: Message):
    if message.from_user.is_self:
        return
    await message.reply(random.choice(welcome_messages))

# ----------- Banall & Unbanall (SUDO/Owner) ------------

@app.on_message(filters.command("banall", prefixes=".") & filters.group)
async def banall_handler(client, message: Message):
    if not is_sudo(message.from_user.id, client):
        return await message.reply("❌ Unauthorized")

    kicked = 0
    async for member in client.get_chat_members(message.chat.id):
        if member.user.is_self or member.status in ("administrator", "creator") or member.user.is_bot:
            continue
        try:
            await client.ban_chat_member(message.chat.id, member.user.id)
            kicked += 1
            await asyncio.sleep(0.5)
        except FloodWait as e:
            await asyncio.sleep(e.value)
        except Exception:
            continue
    await message.reply(f"🚫 Banned {kicked} members from this group.")

@app.on_message(filters.command("unbanall", prefixes=".") & filters.group)
async def unbanall_handler(client, message: Message):
    if not is_sudo(message.from_user.id, client):
        return await message.reply("❌ Unauthorized")

    unbanned = 0
    async for banned in client.get_chat_members(message.chat.id, filter="kicked"):
        try:
            await client.unban_chat_member(message.chat.id, banned.user.id)
            unbanned += 1
            await asyncio.sleep(0.5)
        except FloodWait as e:
            await asyncio.sleep(e.value)
        except Exception:
            continue
    await message.reply(f"✅ Unbanned {unbanned} users in this group.")

# ----------- Start the Bot -----------
app.start()
pytg.start()
print("Bot is running...")
app.idle()
