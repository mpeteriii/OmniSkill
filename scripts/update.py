#!/usr/bin/env python3
import argparse
import sys
import shutil
import urllib.request
import os
import tempfile
import zipfile
from urllib.parse import urlparse
from pathlib import Path
from utils import get_sources, set_writable, set_readonly, VAULT_DIR

def update_github_dir(repo_url, subpath, vault_path):
    print(f"🔄 Updating '{vault_path.name}' from {repo_url} / {subpath}")
    url_parts = urlparse(repo_url).path.strip("/").split("/")
    owner, repo = url_parts[0], url_parts[1]
    api_url = f"https://api.github.com/repos/{owner}/{repo}/zipball/main"
    
    print(f"⬇️  Fetching {api_url}...")
    
    req = urllib.request.Request(api_url, headers={"User-Agent": "omniskill"})
    try:
        with urllib.request.urlopen(req) as response:
            with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                shutil.copyfileobj(response, tmp_file)
                tmp_file_path = tmp_file.name
    except Exception as e:
        print(f"❌ Failed to fetch updates: {e}")
        return
        
    with tempfile.TemporaryDirectory() as extract_dir:
        with zipfile.ZipFile(tmp_file_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
            
        extracted_root = list(Path(extract_dir).iterdir())[0]
        skill_source = extracted_root / subpath
        
        if not skill_source.exists():
            print(f"❌ Subpath '{subpath}' not found in the downloaded repository. It may have been moved or deleted.")
            os.remove(tmp_file_path)
            return
            
        print("🔓 Temporarily unlocking Vault...")
        set_writable(vault_path)
        shutil.rmtree(vault_path)
        
        print(f"📥 Overwriting with new version...")
        shutil.copytree(skill_source, vault_path)
        
        print("🔒 Re-locking Vault...")
        set_readonly(vault_path)
        
        print(f"✅ '{vault_path.name}' updated successfully! All symlinked environments instantly reflect changes.")
        
    os.remove(tmp_file_path)

def update_skill(skill_name=None):
    if not VAULT_DIR.exists():
        print("❌ Vault is empty.")
        sys.exit(1)
        
    skills_to_update = []
    
    # Simple strategy: search the vault
    if skill_name:
        for path in VAULT_DIR.rglob(f"*{skill_name}"):
            if path.is_dir() and (path / "SKILL.md").exists():
                skills_to_update.append(path)
        if not skills_to_update:
            print(f"❌ Skill '{skill_name}' not found in Vault.")
            sys.exit(1)
    else:
        for root, dirs, files in os.walk(VAULT_DIR):
            if "SKILL.md" in files:
                skills_to_update.append(Path(root))
                
    sources = get_sources().get("sources", {})
    
    for vault_path in skills_to_update:
        # Determine origin by looking at the vault structure
        origin = str(vault_path.relative_to(VAULT_DIR))
        
        if origin.startswith("github.com/"):
            # e.g., github.com/openai/skills/skills/.curated/math
            parts = origin.split("/")
            domain, owner, repo = parts[0], parts[1], parts[2]
            repo_url = f"https://{domain}/{owner}/{repo}"
            subpath = "/".join(parts[3:])
            
            update_github_dir(repo_url, subpath, vault_path)
        else:
            print(f"⏭️  Skipping '{vault_path.name}': Not a GitHub repository (origin: {origin}). Cannot automatically update.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Update skills in the Vault from their remote origins")
    parser.add_argument("skill_name", nargs="?", help="Specific skill to update (updates all if omitted)")
    args = parser.parse_args()

    update_skill(args.skill_name)
