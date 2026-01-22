from telegram import Update
from telegram.ext import ContextTypes, filters
import app_config as cfg
import utils

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Check if config exists
    remotes = utils.get_remotes()
    remote_status = f"✅ Loaded ({len(remotes)} remotes)" if remotes else "❌ Not Found (Upload rclone.conf)"
    default_remote = cfg.DEFAULT_REMOTE if cfg.DEFAULT_REMOTE else "None (Set in .env)"

    help_text = (
        f"👻 **PhantomZCloneBot Online**\n"
        f"──────────────────\n"
        f"**System Status:**\n"
        f"📄 Config: `{remote_status}`\n"
        f"☁️ Default Remote: `{default_remote}`\n"
        f"──────────────────\n"
        f"**📥 Transfer Commands:**\n"
        f"`/copyurl <link> [path]` - Download direct link\n"
        f"*(Use -p flag or just separate args)*\n\n"
        
        f"**📂 File Operations:**\n"
        f"`/ls <path>` - List files\n"
        f"`/lsd <path>` - List directories\n"
        f"`/mkdir <path>` - Create directory\n"
        f"`/rmdir <path>` - Remove empty directory\n"
        f"`/delete <path>` - Delete a file\n"
        f"`/purge <path>` - Delete folder & contents\n"
        f"`/cat <path>` - View file content\n"
        f"`/size <path>` - Check size\n\n"

        f"**⚙️ System:**\n"
        f"`/status` - View active transfer progress\n"
        f"`/version` - Rclone version\n"
        f"`/config` - (Attach file) Upload new config\n"
        f"──────────────────\n"
        f"**Tip:** If no remote is specified in path, `{default_remote}` is used."
    )
    
    await update.message.reply_text(help_text, parse_mode="Markdown")

async def upload_config(update: Update, context: ContextTypes.DEFAULT_TYPE):
    document = update.message.document
    if not document or not document.file_name.endswith(".conf"):
        await update.message.reply_text("❌ Please send a valid `.conf` file.")
        return

    # Download config to the bind-mounted path
    new_file = await document.get_file()
    await new_file.download_to_drive(cfg.RCLONE_CONFIG_PATH)
    
    remotes = utils.get_remotes()
    await update.message.reply_text(f"✅ **Config Updated!**\nDetected remotes: `{', '.join(remotes)}`", parse_mode="Markdown")

# Filter used in main.py to detect config uploads
config_filter = filters.CaptionRegex(r"^/config") & filters.Document.ALL
