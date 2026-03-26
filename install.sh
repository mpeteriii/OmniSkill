#!/bin/bash
set -e

echo "📦 Installing OmniSkill - The Universal Package Manager for AI Agents"

VAULT_DIR="$HOME/.config/opencode/skill-vault"
GLOBAL_OPENCODE_DIR="$HOME/.config/opencode/skills"
GLOBAL_AGENTS_DIR="$HOME/.agents/skills"

# 1. Create Vault & Sources
mkdir -p "$VAULT_DIR"
if [ ! -f "$VAULT_DIR/sources.json" ]; then
  cat << 'JSON' > "$VAULT_DIR/sources.json"
{
  "sources": {
    "openai": {
      "type": "github",
      "url": "https://github.com/openai/skills",
      "path": "skills/.curated"
    },
    "anthropic": {
      "type": "github",
      "url": "https://github.com/anthropics/skills",
      "path": "skills"
    }
  }
}
JSON
  echo "✅ Initialized sources.json registry."
fi

# 2. Download OmniSkill code
TMP_DIR=$(mktemp -d)
echo "⬇️ Downloading OmniSkill..."
curl -sL https://github.com/mpeteriii/OmniSkill/archive/refs/heads/main.zip -o "$TMP_DIR/omniskill.zip"
unzip -q "$TMP_DIR/omniskill.zip" -d "$TMP_DIR"

# 3. Move to Vault as a local install
TARGET_VAULT="$VAULT_DIR/github.com/mpeteriii/OmniSkill"
rm -rf "$TARGET_VAULT"
mkdir -p "$(dirname "$TARGET_VAULT")"
mv "$TMP_DIR/OmniSkill-main" "$TARGET_VAULT"

# 4. Lock the Vault files (Read-Only)
find "$TARGET_VAULT" -type f -exec chmod a-w {} +
find "$TARGET_VAULT" -type d -exec chmod a-w {} +

# 5. Create Symlinks for OpenCode and Agents
mkdir -p "$GLOBAL_OPENCODE_DIR"
mkdir -p "$GLOBAL_AGENTS_DIR"

ln -sfn "$TARGET_VAULT" "$GLOBAL_OPENCODE_DIR/omniskill"
ln -sfn "$TARGET_VAULT" "$GLOBAL_AGENTS_DIR/omniskill"

echo "✅ OmniSkill successfully installed!"
echo "   Symlinked to: $GLOBAL_OPENCODE_DIR/omniskill"
echo "   Symlinked to: $GLOBAL_AGENTS_DIR/omniskill"
echo "   Vault Path: $TARGET_VAULT"
echo ""
echo "🚀 Next Step: Just ask your AI agent to \"list available skills from openai\" or \"install openai/playwright\"!"

rm -rf "$TMP_DIR"
