#!/usr/bin/env python3
import argparse
import sys
import os
from pathlib import Path
from utils import get_env_dir

def disable_skill(skill_name, env, scope):
    print(f"🚫 Disabling '{skill_name}' for {env} ({scope})")
    
    target_dir = get_env_dir(env, scope)
    symlink_path = target_dir / skill_name
    
    if not symlink_path.exists() and not symlink_path.is_symlink():
        print(f"⚠️  Skill '{skill_name}' is not enabled at {symlink_path}.")
        sys.exit(0)
        
    if not symlink_path.is_symlink():
        print(f"❌ '{symlink_path}' is a physical directory, not a symlink to the Vault.")
        print("   If you wish to delete it permanently, run `rm -rf {symlink_path}` manually.")
        sys.exit(1)
        
    try:
        symlink_path.unlink()
        print(f"✅ Successfully removed symlink {symlink_path}")
    except OSError as e:
        print(f"❌ Failed to remove symlink: {e}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Disable a skill by removing its symlink")
    parser.add_argument("skill_name", help="Name of the symlinked skill to remove")
    parser.add_argument("--env", choices=["opencode", "agents"], required=True, help="Target ecosystem")
    parser.add_argument("--scope", choices=["global", "local"], required=True, help="Scope where it was enabled")
    args = parser.parse_args()

    disable_skill(args.skill_name, args.env, args.scope)
