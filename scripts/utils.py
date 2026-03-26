import json
import os
import stat
from pathlib import Path

VAULT_DIR = Path(os.path.expanduser("~/.config/opencode/skill-vault"))
SOURCES_FILE = VAULT_DIR / "sources.json"

def get_sources():
    if not SOURCES_FILE.exists():
        return {"sources": {}}
    with open(SOURCES_FILE, "r") as f:
        return json.load(f)

def save_sources(data):
    VAULT_DIR.mkdir(parents=True, exist_ok=True)
    with open(SOURCES_FILE, "w") as f:
        json.dump(data, f, indent=2)

def set_readonly(path):
    """Recursively set files and directories to read-only."""
    path = Path(path)
    for root, dirs, files in os.walk(path):
        for file in files:
            file_path = Path(root) / file
            # Make read-only by removing write permissions for everyone
            os.chmod(file_path, stat.S_IREAD | stat.S_IRGRP | stat.S_IROTH)
        for d in dirs:
            dir_path = Path(root) / d
            # Make read-only by removing write permissions for everyone
            os.chmod(dir_path, stat.S_IREAD | stat.S_IRGRP | stat.S_IROTH | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    # Also set the root path itself to read-only
    os.chmod(path, stat.S_IREAD | stat.S_IRGRP | stat.S_IROTH | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

def set_writable(path):
    """Recursively set files and directories to writable."""
    path = Path(path)
    for root, dirs, files in os.walk(path):
        for file in files:
            file_path = Path(root) / file
            # Make writable by owner
            os.chmod(file_path, stat.S_IREAD | stat.S_IRGRP | stat.S_IROTH | stat.S_IWRITE)
        for d in dirs:
            dir_path = Path(root) / d
            # Make writable and executable (to enter directory) by owner
            os.chmod(dir_path, stat.S_IREAD | stat.S_IRGRP | stat.S_IROTH | stat.S_IWRITE | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    # Also set the root path itself to writable
    os.chmod(path, stat.S_IREAD | stat.S_IRGRP | stat.S_IROTH | stat.S_IWRITE | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

def get_env_dir(env, scope):
    """Get the target directory based on environment and scope."""
    if env == "opencode":
        if scope == "global":
            return Path.home() / ".config" / "opencode" / "skills"
        else:
            return Path.cwd() / ".opencode" / "skills"
    elif env == "agents":
        base = Path.cwd() if scope == "local" else Path.home()
        return base / ".agents" / "skills"
    else:
        raise ValueError(f"Unknown environment: {env}")
