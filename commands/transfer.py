import asyncio
import json
from telegram import Update
from telegram.ext import ContextTypes
import app_config as cfg
import utils

async def copyurl(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Usage: /copyurl <link> [path]
    """
    args = context.args
    if not args:
        await update.message.reply_text("⚠️ Usage: `/copyurl <http_link> [remote_path]`", parse_mode="Markdown")
        return
    
    url = args[0]
    
    # Determine destination
    if len(args) > 1:
        destination = utils.resolve_path(args[1])
    else:
        # Default to root of default remote
        if not cfg.DEFAULT_REMOTE:
            await update.message.reply_text("❌ No default remote set. Please specify path: `/copyurl <url> <remote:path>`")
            return
        destination = f"{cfg.DEFAULT_REMOTE}:/"

    # Start Job
    chat_id = update.effective_chat.id
    status_msg = await update.message.reply_text(f"🚀 **PhantomZClone Starting...**\nSource: `{url}`\nDest: `{destination}`", parse_mode="Markdown")
    
    cfg.ACTIVE_JOBS[chat_id] = {"type": "copyurl", "percent": "0", "status": "Starting"}

    # Build Command
    cmd = [
        "rclone", "copyurl", url, destination,
        "--config", cfg.RCLONE_CONFIG_PATH,
        "--auto-filename", 
        "--no-clobber",
        "--use-json-log",   # JSON logging for parsing
        "--stats", "2s",    # Update stats every 2s
        "--verbose"
    ]

    process = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    # Monitor Progress via stderr (Rclone writes logs to stderr)
    while True:
        line = await process.stderr.readline()
        if not line:
            break
        
        try:
            decoded_line = line.decode().strip()
            if decoded_line.startswith("{"):
                data = json.loads(decoded_line)
                if "stats" in data:
                    stats = data["stats"]
                    job_data = cfg.ACTIVE_JOBS.get(chat_id, {})
                    
                    # Update global state
                    job_data["speed"] = stats.get("speed", "0")
                    job_data["eta"] = f"{stats.get('elapsed', 0)}s elapsed"
                    
                    if "transferring" in stats and stats["transferring"]:
                        trans = stats["transferring"][0]
                        job_data["percent"] = trans.get("percentage", 0)
                        job_data["file"] = trans.get("name", "Unknown")
                    
                    cfg.ACTIVE_JOBS[chat_id] = job_data
        except:
            continue

    await process.wait()
    
    # Cleanup
    if chat_id in cfg.ACTIVE_JOBS:
        del cfg.ACTIVE_JOBS[chat_id]

    if process.returncode == 0:
        await status_msg.edit_text(f"✅ **Transfer Complete!**\nSaved to `{destination}`", parse_mode="Markdown")
    else:
        await status_msg.edit_text(f"❌ **Transfer Failed.**", parse_mode="Markdown")
