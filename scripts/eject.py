#!/usr/bin/env python3
import argparse
import sys
import shutil
import os
from pathlib import Path
from utils import get_env_dir, set_writable, VAULT_DIR

def eject_skill(skill_name, env, scope):
    print(f"🔓 Ejecting '{skill_name}' for {env} ({scope})")
    
    target_dir = get_env_dir(env, scope)
    symlink_path = target_dir / skill_name
    
    if not symlink_path.exists() and not symlink_path.is_symlink():
        print(f"❌ Skill '{skill_name}' is not enabled at {symlink_path}.")
        sys.exit(1)
        
    if not symlink_path.is_symlink():
        print(f"⚠️  '{symlink_path}' is already a physical directory, not a symlink to the Vault.")
        print("   It is already disconnected and safe to edit.")
        sys.exit(0)
        
    vault_path = symlink_path.readlink()
    
    try:
        # 1. Remove the symlink
        print(f"🗑️ Removing symlink...")
        symlink_path.unlink()
        
        # 2. Copy the actual contents from the Vault
        print(f"📥 Copying from Vault: {vault_path}...")
        shutil.copytree(vault_path, symlink_path)
        
        # 3. Restore write permissions so the user can edit it
        print("🔓 Restoring write permissions on the local copy...")
        set_writable(symlink_path)
        
        print(f"\n✅ Skill '{skill_name}' successfully ejected to {symlink_path}!")
        print("   You may now safely modify this local copy without affecting the global Vault.")
    except Exception as e:
        print(f"❌ Failed to eject skill: {e}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Eject a skill from the Vault into a local, editable directory")
    parser.add_argument("skill_name", help="Name of the symlinked skill to eject")
    parser.add_argument("--env", choices=["opencode", "agents"], required=True, help="Target ecosystem")
    parser.add_argument("--scope", choices=["global", "local"], default="local", help="Scope where it was enabled")
    args = parser.parse_args()

    eject_skill(args.skill_name, args.env, args.scope)
