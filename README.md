````markdown
# My Dotfiles

Configuration files for macOS, managed via [GNU Stow](https://www.gnu.org/software/stow/).
Optimized for Web3 development with **Ghostty** and **Zsh**.

## 📂 Structure

```text
~/dotfiles
├── ghostty/
│   └── .config/ghostty/config  # Terminal configuration
├── zsh/
│   └── .zshrc                  # Shell configuration
└── README.md
```
````

## 🚀 Quick Start (New Device)

### 1\. Install Prerequisites (Homebrew & Git)

If you haven't installed Homebrew yet:

```bash
/bin/bash -c "$(curl -fsSL [https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh](https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh))"
```

Add Homebrew to PATH (if on Apple Silicon):

```bash
(echo; echo 'eval "$(/opt/homebrew/bin/brew shellenv)"') >> /Users/$USER/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"
```

### 2\. Install Core Tools

Install `stow` for management and essential cli tools:

```bash
brew install git stow gh
```

### 3\. Clone Repository

Clone this repo to your home directory:

```bash
git clone [https://github.com/YOUR_USERNAME/dotfiles.git](https://github.com/YOUR_USERNAME/dotfiles.git) ~/dotfiles
cd ~/dotfiles
```

### 4\. Apply Configurations (Stow)

This creates symlinks from `~/dotfiles` to your home directory.
**Note:** Ensure you don't have existing `.zshrc` or ghostty config files, or stow will fail (conflict).

```bash
# Backup existing zshrc if needed
# mv ~/.zshrc ~/.zshrc.bak

# Apply configs
stow zsh
stow ghostty
```

### 5\. Install Shell Dependencies

These tools are required for the `.zshrc` to work correctly:

```bash
# 1. Install Modern Shell Tools
brew install starship zoxide

# 2. Install Zsh Plugins (Autosuggestions & Syntax Highlighting)
brew install zsh-autosuggestions zsh-syntax-highlighting

# 3. Install Fonts (Required for Ghostty/Starship)
brew install --cask font-jetbrains-mono-nerd-font
```

### 6\. Finalize

Reload your shell to see changes:

```bash
source ~/.zshrc
```

## 🛠 Manual Fixes

### Ghostty

If Ghostty config isn't loading, check if the default macOS config file is overriding the Stow link:

```bash
# Remove the default conflict file if it exists
rm "$HOME/Library/Application Support/com.mitchellh.ghostty/config"
```

### GitHub Copilot CLI

To enable the `??` alias, login to GitHub:

```bash
gh auth login
gh extension install github/gh-copilot
```
