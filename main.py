import logging
import app_config as cfg
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

# Import modules
from commands import core, file_ops, system, transfer

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

if __name__ == '__main__':
    # Verify Tokens
    if not cfg.BOT_TOKEN:
        print("CRITICAL: BOT_TOKEN not found in environment variables.")
        exit(1)

    app = ApplicationBuilder().token(cfg.BOT_TOKEN).build()
    
    # Security: Allow only Authorized User
    if cfg.AUTHORIZED_USER_ID == 0:
        print("WARNING: AUTHORIZED_USER_ID is 0. Bot might reject commands.")
    
    user_filter = filters.User(user_id=cfg.AUTHORIZED_USER_ID)

    # --- Register Core Commands ---
    app.add_handler(CommandHandler("start", core.start, filters=user_filter))
    app.add_handler(CommandHandler("help", core.start, filters=user_filter))
    # Detect config file upload
    app.add_handler(MessageHandler(user_filter & core.config_filter, core.upload_config))

    # --- Register Transfer Commands ---
    app.add_handler(CommandHandler("copyurl", transfer.copyurl, filters=user_filter))

    # --- Register File Ops Commands ---
    app.add_handler(CommandHandler("ls", file_ops.ls, filters=user_filter))
    app.add_handler(CommandHandler("lsd", file_ops.lsd, filters=user_filter))
    app.add_handler(CommandHandler("mkdir", file_ops.mkdir, filters=user_filter))
    app.add_handler(CommandHandler("rmdir", file_ops.rmdir, filters=user_filter))
    app.add_handler(CommandHandler("delete", file_ops.delete, filters=user_filter))
    app.add_handler(CommandHandler("purge", file_ops.purge, filters=user_filter))
    app.add_handler(CommandHandler("cat", file_ops.cat, filters=user_filter))
    app.add_handler(CommandHandler("size", file_ops.size, filters=user_filter))

    # --- Register System Commands ---
    app.add_handler(CommandHandler("status", system.status, filters=user_filter))
    app.add_handler(CommandHandler("version", system.version, filters=user_filter))

    print(f"PhantomZCloneBot is polling... (Authorized User: {cfg.AUTHORIZED_USER_ID})")
    app.run_polling()
