---
name: omniskill
description: Install, update, and manage skills from external sources (like GitHub or local paths) into a centralized read-only Vault, and securely enable them globally or locally via symlinks for OpenCode, Claude, or Agents. Use this when the user asks to find new skills, install skills, update skills, or manage their skill environments.
---

# OmniSkill

OmniSkill is an advanced, ASDF-like package manager for AI skills. It solves the problem of discovering, installing, isolating, and updating skills across different AI tools and projects.

## Architecture Overview

1.  **The Vault (`~/.config/opencode/skill-vault/`)**: All skills are downloaded here. They are organized by their origin (e.g., `github.com/openai/...` or `local/...`). Because multiple agents might use a skill simultaneously, the Vault makes downloaded skills read-only to prevent agents from corrupting the master copy with temporary files or dependency installations.
2.  **The Environments**: Activate skills by creating symlinks from the Vault into specific tool environments:
    *   `~/.config/opencode/skills/` (OpenCode Global) or `.opencode/skills/` (OpenCode Local)
    *   `.agents/skills/` (Generic Agents)
3.  **The Scopes**: Place symlinks globally (for all projects) or locally (for a specific project workspace).

## Usage & Workflows

Always use the bundled Python scripts in `scripts/` to perform these actions. Do not manually copy files or create symlinks yourself.

### 1. Discovery (`scripts/list.py`)
To discover new skills or review installed ones:
*   `python scripts/list.py --remote`: Fetch and list all available skills from configured remote sources (e.g., OpenAI, Anthropic).
*   `python scripts/list.py --status`: Display all skills currently sitting in the Vault and identify where they are actively symlinked.

### 2. Installation (`scripts/install.py`)
To install a skill into the Vault:
*   `python scripts/install.py <source>`
*   This downloads the skill (e.g., "openai/math" or a GitHub URL) into the read-only Vault.
*   Because OmniSkill supports multiple AI tools, after installing a skill into the Vault, you must ask the user where to link it so that it becomes available to their preferred environment (`opencode` vs `agents`) and scope (`global` vs `local`). Do not proceed to activation until they answer.

### 3. Activation (`scripts/enable.py` & `scripts/disable.py`)
To activate or deactivate a skill based on the user's preferences:
*   Enable: `python scripts/enable.py <skill_name> --env <opencode|agents> --scope <global|local>`
*   Disable: `python scripts/disable.py <skill_name> --env <env> --scope <scope>`

### 4. Updating (`scripts/update.py`)
To keep the Vault fresh:
*   `python scripts/update.py [skill_name]` (Updates a specific skill, or all skills if no name is provided).
*   This temporarily unlocks the Vault, fetches the latest files from the original remote source, and relocks it. Because environments use symlinks, all active environments update instantly.

### 5. Safe Editing (`scripts/eject.py`)
To modify an installed skill:
*   Because skills in the Vault are immutable and shared across projects, directly editing a symlinked skill will fail. Therefore, whenever the user asks to modify, edit, or update the code/prompts of an installed skill, first check if it is a symlink. 
*   If it is a symlink, run: `python scripts/eject.py <skill_name> --env <env> --scope local`
*   This replaces the local symlink with a writable, disconnected copy of the skill from the Vault. You may then safely edit this local copy using tools like `skill-creator`.

### 6. Managing Sources (`scripts/source.py`)
To add a new GitHub repository to search for skills:
*   `python scripts/source.py add <alias> <url> [--path <subfolder>]` 
*   `python scripts/source.py remove <alias>`
*   `python scripts/source.py list`

## Examples

**Example 1: Installing a new skill**
Input: "Install the OpenAI playwright skill globally for OpenCode."
Action: 
1. Run `python scripts/install.py openai/playwright`
2. Run `python scripts/enable.py playwright --env opencode --scope global`

**Example 2: Safe local editing**
Input: "I want to edit the math skill for this project."
Action:
1. Verify it's a symlink in the current project directory.
2. Run `python scripts/eject.py math --env agents --scope local`
3. Edit the newly created local files.
