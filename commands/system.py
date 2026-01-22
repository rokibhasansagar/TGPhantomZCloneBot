from telegram import Update
from telegram.ext import ContextTypes
import app_config as cfg
import utils

async def version(update: Update, context: ContextTypes.DEFAULT_TYPE):
    code, out, err = await utils.run_rclone(["version"])
    await update.message.reply_text(f"ℹ️ **PhantomZClone Version:**\n`{out}`", parse_mode="Markdown")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    job = cfg.ACTIVE_JOBS.get(chat_id)

    if not job:
        await update.message.reply_text("💤 No active transfers running.")
        return

    msg = (
        f"🔄 **Active Transfer:**\n"
        f"📄 File: `{job.get('file', 'Initializing...')}`\n"
        f"📊 Progress: {job.get('percent', '0')}% \n"
        f"🚀 Speed: {job.get('speed', '0')}\n"
        f"⏱ Time: {job.get('eta', '0')}"
    )
    await update.message.reply_text(msg, parse_mode="Markdown")
