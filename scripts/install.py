#!/usr/bin/env python3
import argparse
import sys
import shutil
import tempfile
import zipfile
import urllib.request
import os
from urllib.parse import urlparse
from pathlib import Path
from utils import get_sources, VAULT_DIR, set_readonly, set_writable

def download_github_dir(repo_url, subpath, dest_dir):
    """Download a specific subfolder from a GitHub repo as a zip using the GitHub API."""
    url_parts = urlparse(repo_url).path.strip("/").split("/")
    if len(url_parts) < 2:
        print("Invalid GitHub URL format.")
        sys.exit(1)
        
    owner, repo = url_parts[0], url_parts[1]
    api_url = f"https://api.github.com/repos/{owner}/{repo}/zipball/main"
    
    print(f"⬇️  Downloading from {api_url}...")
    
    req = urllib.request.Request(api_url, headers={"User-Agent": "omniskill"})
    with urllib.request.urlopen(req) as response:
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            shutil.copyfileobj(response, tmp_file)
            tmp_file_path = tmp_file.name
            
    with tempfile.TemporaryDirectory() as extract_dir:
        with zipfile.ZipFile(tmp_file_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
            
        # GitHub zips put everything in a root folder like 'openai-skills-abcdef1/'
        extracted_root = list(Path(extract_dir).iterdir())[0]
        skill_source = extracted_root / subpath
        
        if not skill_source.exists():
            print(f"❌ Subpath '{subpath}' not found in the downloaded repository.")
            sys.exit(1)
            
        if dest_dir.exists():
            print(f"⚠️  Skill already exists in Vault. Overwriting...")
            set_writable(dest_dir)
            shutil.rmtree(dest_dir)
            
        shutil.copytree(skill_source, dest_dir)
        
    os.remove(tmp_file_path)

def install_source(source_arg):
    # Parse source type (URL, local path, or alias/name)
    sources = get_sources().get("sources", {})
    
    dest_path = None
    skill_name = None
    
    # 1. Alias format: e.g., 'openai/math'
    if "/" in source_arg and not source_arg.startswith("http") and not os.path.exists(source_arg):
        alias, skill = source_arg.split("/", 1)
        if alias in sources:
            source = sources[alias]
            repo_url = source["url"]
            subpath = f"{source.get('path', '')}/{skill}".strip("/")
            
            domain = urlparse(repo_url).netloc
            repo_path = urlparse(repo_url).path.strip("/")
            
            dest_path = VAULT_DIR / domain / repo_path / subpath
            skill_name = skill
            
            print(f"📦 Installing '{skill}' from curated source '{alias}'...")
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            download_github_dir(repo_url, subpath, dest_path)
            
        else:
            print(f"❌ Source alias '{alias}' not found in registry.")
            sys.exit(1)

    # 2. Local Directory or .skill file
    elif Path(source_arg).exists():
        src_path = Path(source_arg).absolute()
        skill_name = src_path.stem.replace(".skill", "")
        dest_path = VAULT_DIR / "local" / src_path.parent.relative_to(Path("/")).joinpath(skill_name)
        
        if src_path.is_file() and src_path.suffix == ".skill":
            print(f"📦 Extracting local .skill archive '{skill_name}'...")
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            if dest_path.exists():
                set_writable(dest_path)
                shutil.rmtree(dest_path)
            
            with zipfile.ZipFile(src_path, 'r') as zip_ref:
                zip_ref.extractall(dest_path)
                
        elif src_path.is_dir():
            print(f"📦 Importing local directory '{skill_name}'...")
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            if dest_path.exists():
                set_writable(dest_path)
                shutil.rmtree(dest_path)
            shutil.copytree(src_path, dest_path)
            
        else:
            print(f"❌ Unsupported local file type: {src_path}")
            sys.exit(1)

    # 3. Direct GitHub URL (fallback)
    elif source_arg.startswith("https://github.com/"):
        print("📦 Installing from direct GitHub URL...")
        parsed = urlparse(source_arg)
        parts = parsed.path.strip("/").split("/")
        
        if len(parts) >= 5 and parts[2] == "tree":
            # e.g., https://github.com/user/repo/tree/main/skills/math
            owner, repo = parts[0], parts[1]
            subpath = "/".join(parts[4:])
            skill_name = parts[-1]
            repo_url = f"https://github.com/{owner}/{repo}"
            
            dest_path = VAULT_DIR / parsed.netloc / owner / repo / subpath
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            download_github_dir(repo_url, subpath, dest_path)
        else:
            print("❌ Invalid GitHub tree URL. Must point to a specific skill directory.")
            sys.exit(1)
            
    else:
        print(f"❌ Unsupported source format: {source_arg}")
        sys.exit(1)

    # Final Validation & Lockdown
    if dest_path and dest_path.exists():
        skill_md = dest_path / "SKILL.md"
        if not skill_md.exists():
            print(f"⚠️  WARNING: No SKILL.md found in {dest_path}. This may not be a valid skill.")
        
        print("🔒 Locking source files in the Vault (read-only)...")
        set_readonly(dest_path)
        
        print(f"\n✅ Skill '{skill_name}' successfully installed to the Vault!")
        print(f"Vault Path: {dest_path}")
        print("\n👉 Next Step: Enable this skill globally or locally using:")
        print(f"   python enable.py {skill_name} --env [opencode|claude|agents] --scope [global|local]")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Install a skill into the Vault")
    parser.add_argument("source", help="Source alias (e.g., openai/math), local path, or GitHub tree URL")
    args = parser.parse_args()

    install_source(args.source)
