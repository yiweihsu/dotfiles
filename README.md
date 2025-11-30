````markdown
# 🛠️ My Dotfiles

Minimal, fast, and AI-optimized setup for macOS using **Ghostty** + **Zsh**.

## ⚡️ Quick Setup

### 1. Clone & Install Dependencies

Assumes you have [Homebrew](https://brew.sh) installed.

```bash
# 1. Clone repo
git clone [https://github.com/YOUR_USERNAME/dotfiles.git](https://github.com/YOUR_USERNAME/dotfiles.git) ~/dotfiles
cd ~/dotfiles

# 2. Install EVERYTHING (Tools, Shell, Fonts)
brew install git stow gh starship zoxide zsh-autosuggestions zsh-syntax-highlighting
brew install --cask font-jetbrains-mono-nerd-font
```
````

### 2\. Cleanup & Link (Stow)

Move existing configs aside to avoid conflicts, then link the new ones.

```bash
# 1. Backup old configs (ignore errors if files don't exist)
mv ~/.zshrc ~/.zshrc.bak
mv ~/.config/ghostty/config ~/.config/ghostty/config.bak
# Remove macOS default ghostty config location if it exists
rm "$HOME/Library/Application Support/com.mitchellh.ghostty/config"

# 2. Link files
cd ~/dotfiles
stow zsh
stow ghostty
```

### 3\. Finalize

```bash
# Login to GitHub (for Copilot)
gh auth login

# Refresh Shell
source ~/.zshrc
```

---

## 🤖 AI Cheatsheet

### GitHub Copilot (`??`)

Powered by GitHub CLI. Best for general coding questions.

| Command  | Usage                 | Description                                |
| :------- | :-------------------- | :----------------------------------------- |
| **`??`** | `??`                  | Start interactive AI agent session.        |
| **`??`** | `?? "kill port 3000"` | Ask a specific question (Suggestion mode). |

### Codex CLI (`cx`)

Powered by OpenAI/Codex. Best for complex tasks or file manipulation.

| Command   | Usage                    | Description                                            |
| :-------- | :----------------------- | :----------------------------------------------------- |
| **`cx`**  | `cx`                     | Enter interactive chat mode.                           |
| **`cxe`** | `cxe "list large files"` | **Exec**ute a single command (Non-interactive).        |
| **`cxa`** | `cxa "refactor main.js"` | **Full Auto** mode. Reads/writes files without asking. |

## ⌨️ Shell Shortcuts

| Command     | Description                                               |
| :---------- | :-------------------------------------------------------- |
| `z <dir>`   | Smart jump to directory (e.g., `z dot` -\> `~/dotfiles`). |
| `src`       | Reload `.zshrc`.                                          |
| `zshconfig` | Open `.zshrc` in editor.                                  |
