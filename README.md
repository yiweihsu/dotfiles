# 🛠️ My Dotfiles

Minimal, fast setup for macOS using **iTerm2** + **Zsh** + **Starship**.

## ⚡️ Quick Setup

### 1. Clone & Install Dependencies

Assumes you have [Homebrew](https://brew.sh) installed.

```bash
# 1. Clone repo
git clone https://github.com/YOUR_USERNAME/dotfiles.git ~/dotfiles
cd ~/dotfiles

# 2. Install all dependencies using Brewfile
brew bundle install
```

### 2. Link Dotfiles

```bash
# Backup old configs (ignore errors if files don't exist)
mv ~/.zshrc ~/.zshrc.bak
mv ~/.zshenv ~/.zshenv.bak
mv ~/.zprofile ~/.zprofile.bak
mv ~/.config/starship.toml ~/.config/starship.toml.bak

# Link zsh configs
ln -s ~/dotfiles/zsh/.zshrc ~/.zshrc
ln -s ~/dotfiles/zsh/.zshenv ~/.zshenv
ln -s ~/dotfiles/zsh/.zprofile ~/.zprofile

# Link starship config
mkdir -p ~/.config
ln -s ~/dotfiles/starship/starship.toml ~/.config/starship.toml

# Link iTerm2 preferences
ln -s ~/dotfiles/iterm2/com.googlecode.iterm2.plist ~/Library/Preferences/com.googlecode.iterm2.plist
```

### 3. Finalize

```bash
# Refresh Shell
source ~/.zshrc
```

---

## 📦 What's Included

### Shell & Prompt

- **Zsh** - Shell configuration with .zshrc, .zshenv, and .zprofile
- **Starship** - Fast, customizable prompt
- **Zoxide** - Smarter cd command

### Terminal

- **iTerm2** - Feature-rich terminal emulator for macOS

### Development Tools

- **nvm** - Node.js version manager
- **pyenv** - Python version manager

### Shell Enhancement

- **zsh-autosuggestions** - Fish-like autosuggestions
- **zsh-syntax-highlighting** - Real-time syntax highlighting

---

## ⌨️ Shell Shortcuts

| Command   | Description                                              |
| :-------- | :------------------------------------------------------- |
| `z <dir>` | Smart jump to directory (e.g., `z dot` -> `~/dotfiles`). |
| `src`     | Reload `.zshrc`.                                         |
