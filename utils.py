import os
import asyncio
import logging
import configparser
import app_config as cfg

logger = logging.getLogger(__name__)

def get_remotes():
    """Reads rclone.conf to find available remotes."""
    if not os.path.exists(cfg.RCLONE_CONFIG_PATH):
        return []
    config = configparser.ConfigParser()
    config.read(cfg.RCLONE_CONFIG_PATH)
    return config.sections()

def resolve_path(path_arg: str) -> str:
    """
    Intelligently resolves the path.
    If 'folder/file' is given -> prepends DEFAULT_REMOTE.
    If 'remote:folder/file' is given -> uses it as is.
    """
    if ":" in path_arg:
        return path_arg
    
    if cfg.DEFAULT_REMOTE:
        clean_path = path_arg.lstrip("/")
        return f"{cfg.DEFAULT_REMOTE}:{clean_path}"
    
    return path_arg

async def run_rclone(cmd_list):
    """
    Executes a standard rclone command.
    """
    # Ensure config path is injected into every command
    full_cmd = ["rclone"] + cmd_list + ["--config", cfg.RCLONE_CONFIG_PATH]
    
    process = await asyncio.create_subprocess_exec(
        *full_cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    return process.returncode, stdout.decode().strip(), stderr.decode().strip()
