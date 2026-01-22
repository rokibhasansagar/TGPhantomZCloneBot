from telegram import Update
from telegram.ext import ContextTypes
import utils

async def generic_ops(update: Update, context: ContextTypes.DEFAULT_TYPE, rclone_cmd: str):
    """Generic handler to run simple rclone commands"""
    if not context.args:
        await update.message.reply_text(f"⚠️ Usage: `/{rclone_cmd} <path>`")
        return
    
    target = utils.resolve_path(context.args[0])
    msg = await update.message.reply_text(f"⏳ **PhantomZClone:** Running `{rclone_cmd}`...", parse_mode="Markdown")
    
    # Add flags for specific commands for better output
    cmd_args = [rclone_cmd, target]
    if rclone_cmd in ['ls', 'lsd', 'size']:
        cmd_args.append("--human-readable")

    code, out, err = await utils.run_rclone(cmd_args)

    if code == 0:
        # Sanitize output length for Telegram (4096 char limit)
        if len(out) > 3000: out = out[:3000] + "\n...(truncated)"
        if not out: out = "Done (No Output)"
        await msg.edit_text(f"✅ **Result:**\n```{out}```", parse_mode="Markdown")
    else:
        await msg.edit_text(f"❌ **Error:**\n`{err}`", parse_mode="Markdown")

# Wrappers for Bot Commands
async def ls(u, c): await generic_ops(u, c, "ls")
async def lsd(u, c): await generic_ops(u, c, "lsd")
async def mkdir(u, c): await generic_ops(u, c, "mkdir")
async def rmdir(u, c): await generic_ops(u, c, "rmdir")
async def delete(u, c): await generic_ops(u, c, "delete")
async def purge(u, c): await generic_ops(u, c, "purge")
async def cat(u, c): await generic_ops(u, c, "cat")
async def size(u, c): await generic_ops(u, c, "size")
