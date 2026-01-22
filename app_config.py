import os

def get_env(key, default=None):
    """Helper to read from .env loaded by Docker"""
    return os.getenv(key, default)

# --- CREDENTIALS ---
BOT_TOKEN = get_env("BOT_TOKEN", "")
AUTHORIZED_USER_ID = int(get_env("AUTHORIZED_USER_ID", "0"))

# --- SETTINGS ---
# We point directly to the bind-mounted file in Docker
RCLONE_CONFIG_PATH = get_env("RCLONE_CONFIG_PATH", "/data/app/rclone.conf")

# Default remote to use if the user provides only a path (e.g., "gdrive")
DEFAULT_REMOTE = get_env("DEFAULT_REMOTE", "")

# --- GLOBAL STATE ---
# Tracks active transfers for status updates
ACTIVE_JOBS = {}
