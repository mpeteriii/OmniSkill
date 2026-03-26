#!/usr/bin/env python3
import argparse
import sys
import os
from pathlib import Path
from utils import get_sources, get_env_dir, set_writable, set_readonly, VAULT_DIR

def find_in_vault(skill_name):
    # Find the skill by name recursively
    for path in VAULT_DIR.rglob(f"*{skill_name}"):
        if path.is_dir() and (path / "SKILL.md").exists():
            return path
    return None

def enable_skill(skill_name, env, scope, alias=None):
    print(f"🔧 Enabling '{skill_name}' for {env} ({scope})")
    
    vault_path = find_in_vault(skill_name)
    if not vault_path:
        print(f"❌ Skill '{skill_name}' not found in the Vault.")
        print("Run `list.py --status` to see installed skills or `install.py` to fetch it first.")
        sys.exit(1)
        
    print(f"📍 Found in Vault: {vault_path}")
    
    target_dir = get_env_dir(env, scope)
    target_dir.mkdir(parents=True, exist_ok=True)
    
    link_name = alias if alias else skill_name
    symlink_path = target_dir / link_name
    
    if symlink_path.exists() or symlink_path.is_symlink():
        if symlink_path.is_symlink() and symlink_path.readlink() == vault_path:
            print(f"⚠️  Skill '{skill_name}' is already enabled here as '{link_name}'.")
            sys.exit(0)
            
        print(f"❌ A skill or directory named '{link_name}' already exists at {symlink_path}.")
        print(f"   Please run this command again with the --alias flag. (e.g. --alias {link_name}-custom)")
        sys.exit(1)
        
    try:
        symlink_path.symlink_to(vault_path)
        print(f"✅ Successfully symlinked {symlink_path} -> {vault_path}")
    except OSError as e:
        print(f"❌ Failed to create symlink: {e}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Enable a skill via symlink")
    parser.add_argument("skill_name", help="Name of the skill in the Vault")
    parser.add_argument("--env", choices=["opencode", "agents"], required=True, help="Target ecosystem")
    parser.add_argument("--scope", choices=["global", "local"], required=True, help="Enable globally or just for this project")
    parser.add_argument("--alias", help="Alias to use for the symlink if the name is already taken", default=None)
    args = parser.parse_args()

    enable_skill(args.skill_name, args.env, args.scope, args.alias)
