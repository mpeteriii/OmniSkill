#!/usr/bin/env python3
import argparse
import sys
import os
from utils import get_sources, save_sources

def add_source(alias, url, path=""):
    sources = get_sources()
    
    if alias in sources["sources"]:
        print(f"⚠️  Source '{alias}' already exists. Overwriting...")
        
    type_ = "github" if "github.com" in url else "git"
    
    sources["sources"][alias] = {
        "type": type_,
        "url": url.rstrip("/"),
        "path": path.strip("/")
    }
    
    save_sources(sources)
    print(f"✅ Source '{alias}' added successfully! ({url}/{path})")

def remove_source(alias):
    sources = get_sources()
    
    if alias not in sources["sources"]:
        print(f"❌ Source '{alias}' not found.")
        sys.exit(1)
        
    del sources["sources"][alias]
    save_sources(sources)
    print(f"✅ Source '{alias}' removed successfully!")

def list_sources():
    sources = get_sources().get("sources", {})
    
    print("📚 CONFIGURED SOURCES:")
    print("-" * 50)
    
    if not sources:
        print("No sources configured.")
        sys.exit(0)
        
    for alias, source in sources.items():
        url = source["url"]
        path = source.get("path", "")
        print(f"[{alias}] -> {url} (path: {path})")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Manage skill sources")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    parser_add = subparsers.add_parser("add", help="Add a new source")
    parser_add.add_argument("alias", help="Alias for the source (e.g. 'community')")
    parser_add.add_argument("url", help="Repository URL (e.g. 'https://github.com/user/repo')")
    parser_add.add_argument("--path", default="", help="Subpath within the repository")
    
    parser_remove = subparsers.add_parser("remove", help="Remove a source")
    parser_remove.add_argument("alias", help="Alias of the source to remove")
    
    parser_list = subparsers.add_parser("list", help="List all configured sources")
    
    args = parser.parse_args()

    if args.command == "add":
        add_source(args.alias, args.url, args.path)
    elif args.command == "remove":
        remove_source(args.alias)
    elif args.command == "list":
        list_sources()
