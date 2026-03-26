#!/usr/bin/env python3
import argparse
import sys
import urllib.request
import json
import os
from pathlib import Path
from utils import get_sources, VAULT_DIR

def list_remote():
    sources = get_sources().get("sources", {})
    print("🌍 AVAILABLE REMOTE SKILLS:")
    print("-" * 50)
    
    for alias, source in sources.items():
        url = source["url"]
        path = source.get("path", "")
        
        # Simple parsing for github repos
        if "github.com" in url:
            parts = url.replace("https://github.com/", "").split("/")
            if len(parts) >= 2:
                owner, repo = parts[0], parts[1]
                api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
                
                try:
                    req = urllib.request.Request(api_url, headers={"Accept": "application/vnd.github.v3+json", "User-Agent": "omniskill"})
                    with urllib.request.urlopen(req) as response:
                        contents = json.loads(response.read().decode())
                        
                        skills = [item["name"] for item in contents if item["type"] == "dir" and not item["name"].startswith(".")]
                        if skills:
                            print(f"\n📦 From '{alias}' ({url}):")
                            for skill in skills:
                                print(f"  - {alias}/{skill}")
                except Exception as e:
                    print(f"  [!] Failed to fetch from {alias}: {e}")

def list_status():
    print("🏦 VAULT STATUS:")
    print("-" * 50)
    
    if not VAULT_DIR.exists():
        print("Vault is empty.")
        return
        
    installed = []
    for root, dirs, files in os.walk(VAULT_DIR):
        if "SKILL.md" in files:
            rel_path = Path(root).relative_to(VAULT_DIR)
            installed.append(rel_path)
            
    if not installed:
        print("No skills currently in Vault.")
    else:
        for skill_path in installed:
            skill_name = skill_path.name
            origin = str(skill_path.parent)
            print(f"✅ {skill_name} (Origin: {origin})")

    # We could extend this to search local envs for symlinks
    print("\nUse `install.py` to add skills or `enable.py` to activate them.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="List available or installed skills")
    parser.add_argument("--remote", action="store_true", help="List remote skills from configured sources")
    parser.add_argument("--status", action="store_true", help="List installed skills in the Vault")
    args = parser.parse_args()

    if args.remote:
        list_remote()
    elif args.status:
        list_status()
    else:
        parser.print_help()
