# OmniSkill

> The universal package manager for OpenCode and subagents. Fetch, isolate, and update AI skills from any Git repository into a secure, read-only vault for safe multi-agent execution.

OmniSkill is an advanced, ASDF-like package manager built specifically for AI agents like OpenCode and Claude. It solves the critical problems of discovering, installing, isolating, and updating skills across different AI tools and projects.

## Why OmniSkill?

*   **The Ecosystem Problem:** Skills are scattered across different repositories (OpenAI, Anthropic, community repos). OmniSkill bridges these gaps by fetching skills from any GitHub URL or registered source.
*   **The Parallel Execution Problem:** If multiple agents execute the same skill simultaneously, they can corrupt each other's temporary files or `node_modules` folders. OmniSkill solves this using an **Immutable Vault Architecture**. Skills are downloaded to a central, strictly read-only Vault, and then isolated.
*   **The Multi-Agent Problem:** OmniSkill seamlessly enables skills globally or locally for OpenCode (`.opencode/skills/`) and generic agents (`.agents/skills/`).

## Quick Install

Run this single command to install OmniSkill globally for OpenCode and your subagents:

```bash
curl -sL https://raw.githubusercontent.com/mpeteriii/OmniSkill/main/install.sh | bash
```

## Usage

Once installed, simply ask your agent (e.g., OpenCode) to manage your skills!

*   **Discovery:** *"Use OmniSkill to list available skills from Anthropic and OpenAI."*
*   **Installation:** *"Install the `openai/playwright` skill!"* or *"Install `https://github.com/user/repo/tree/main/skills/custom`"*
*   **Activation:** The agent will automatically ask you if you want the skill enabled globally or locally, and for which ecosystem (OpenCode or Agents).
*   **Updating:** *"Update my skills."* (OmniSkill will securely pull the latest changes from GitHub for all installed skills).
*   **Safe Local Editing:** *"I want to edit the `math` skill."* (OmniSkill will automatically `eject` it from the read-only vault so you can safely edit a local copy).

## Architecture

1.  **The Vault (`~/.config/opencode/skill-vault/`)**: All skills are downloaded here, mapped by their origin URL to prevent naming collisions. Core files are locked down via `chmod -w` to guarantee immutability.
2.  **The Environments**: Skills are activated via symlinks from the Vault into specific tool environments (`~/.config/opencode/skills/` or `~/.agents/skills/`).
3.  **The Scopes**: Symlinks can be placed globally or locally for a specific project (`$PWD/.agents/skills/`).

## 🤝 Contributing is Very Welcome!

The AI agent ecosystem is moving incredibly fast, and OmniSkill is designed to evolve with it. **Contributions are highly encouraged and very welcome!**

Whether you want to:
*   Add native support for new AI ecosystems (like Cursor, OpenClaw, etc.)
*   Improve the `sources.json` registry with new community-curated skill lists
*   Enhance the security and isolation of the Immutable Vault
*   Fix bugs or improve documentation

...we would love your help! Please feel free to open an issue to discuss ideas, or submit a Pull Request directly. No contribution is too small. Let's build the standard package manager for AI agents together!

## License
MIT License. See [LICENSE](LICENSE) for more details.
