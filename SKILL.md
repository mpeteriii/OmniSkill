---
name: omniskill
description: Install, update, and manage skills from external sources (like GitHub or local paths) into a centralized read-only Vault, and securely enable them globally or locally via symlinks for OpenCode, Claude, or Agents. Use this when the user asks to find new skills, install skills, update skills, or manage their skill environments.
---

# OmniSkill

The `omniskill` is an advanced, ASDF-like package manager for AI skills. It solves the problem of discovering, installing, isolating, and updating skills across different AI tools and projects.

## Architecture Overview

1.  **The Vault (`~/.config/opencode/skill-vault/`)**: All skills are downloaded here. They are organized by their origin (e.g., `github.com/openai/...` or `local/...`). **CRITICAL:** Skills in the Vault are made read-only to prevent agents from corrupting global copies with temporary files.
2.  **The Environments**: Skills are activated by creating symlinks from the Vault into specific tool environments:
    *   `~/.config/opencode/skills/` (OpenCode Global) or `.opencode/skills/` (OpenCode Local)
    *   `.agents/skills/` (Claude)
    *   `.agents/skills/` (Generic Agents)
3.  **The Scopes**: Symlinks can be placed globally (e.g., `~/.agents/skills/`) or locally for a specific project (`$PWD/.agents/skills/`).

## Usage & Workflows

You must use the bundled Python scripts in `scripts/` to perform these actions. NEVER attempt to manually copy files or create symlinks yourself.

### 1. Discovery (`scripts/list.py`)
When the user asks what skills are available, or what they have installed:
*   `python scripts/list.py --remote`: Fetches and lists all available skills from configured remote sources (e.g., OpenAI, Anthropic).
*   `python scripts/list.py --status`: Shows all skills currently in the Vault and where they are actively symlinked.

### 2. Installation (`scripts/install.py`)
When the user asks to install a skill (e.g., "Install openai/math" or "Install https://github.com/.../math" or "Import ./my-local-skill"):
*   `python scripts/install.py <source>`
*   This downloads the skill into the read-only Vault.
*   **MANDATORY AFTER INSTALL:** You MUST ask the user:
    1.  *"Which environment should I enable this for? (opencode or agents)"*
    2.  *"Should I enable it Globally (for all projects) or Locally (just for this workspace)?"*
    Do NOT proceed to step 3 until they answer.

### 3. Activation (`scripts/enable.py` & `scripts/disable.py`)
Once you have the user's answers from Step 2:
*   `python scripts/enable.py <skill_name> --env <opencode|agents> --scope <global|local>`
*   If they want to remove a skill: `python scripts/disable.py <skill_name> --env <env> --scope <scope>`

### 4. Updating (`scripts/update.py`)
When the user asks to update their skills:
*   `python scripts/update.py [skill_name]` (Updates a specific skill, or all skills if no name provided).
*   This temporarily unlocks the Vault, fetches the latest files from the original source, and relocks it. All symlinked environments update instantly.

### 5. Safe Editing (`scripts/eject.py`)
**CRITICAL PROTECTION:** If the user asks you to modify, edit, or update the code/prompts of an *already installed skill*, you must FIRST check if it is a symlink.
*   If it is a symlink, you MUST run: `python scripts/eject.py <skill_name> --env <env> --scope local`
*   This replaces the local symlink with a writable, disconnected copy of the skill from the Vault. You may then edit this local copy freely using tools like `skill-creator`.

### 6. Managing Sources (`scripts/source.py`)
When the user wants to add a new GitHub repository to search for skills:
*   `python scripts/source.py add <alias> <url> [--path <subfolder>]` (e.g., `python scripts/source.py add community https://github.com/awesome/skills --path dist/`)
*   `python scripts/source.py remove <alias>`
*   `python scripts/source.py list`
