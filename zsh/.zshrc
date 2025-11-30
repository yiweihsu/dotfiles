# --- 1. Path & Environment Variables (Load first) ---
# Homebrew Setup (Standard for Apple Silicon)
if [[ -f /opt/homebrew/bin/brew ]]; then
    eval "$(/opt/homebrew/bin/brew shellenv)"
fi

# Java Home
export PATH="/opt/homebrew/opt/openjdk/bin:$PATH"
export JAVA_HOME="/opt/homebrew/opt/openjdk"

# Antigravity
export PATH="/Users/yiwei/.antigravity/antigravity/bin:$PATH"

# Editor (Default editor, change to 'code' or 'vim' if you prefer)
export EDITOR='vim'

# --- 2. Oh My Zsh Setup ---
export ZSH="$HOME/.oh-my-zsh"

# Disable default OMZ theme (We are using Starship instead for speed)
ZSH_THEME=""files

# Plugins (Load git only here; manage others via Brew for performance)
plugins=(git)

source $ZSH/oh-my-zsh.sh

# --- 3. Modern Tools ---

# Starship: Blazing fast, beautiful prompt
if command -v starship &> /dev/null; then
    eval "$(starship init zsh)"
fi

# Zoxide: Smarter directory jumping (Replaces 'cd')
if command -v zoxide &> /dev/null; then
    eval "$(zoxide init zsh)"
    alias cd="z"
fi

# Zsh Autosuggestions (Gray text suggestions based on history)
if [ -f /opt/homebrew/share/zsh-autosuggestions/zsh-autosuggestions.zsh ]; then
    source /opt/homebrew/share/zsh-autosuggestions/zsh-autosuggestions.zsh
fi

# Zsh Syntax Highlighting (Green for valid commands, red for invalid)
# Note: This must be loaded LAST
if [ -f /opt/homebrew/share/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh ]; then
    source /opt/homebrew/share/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh
fi

# --- 4. NVM (Node Version Manager) ---
# NVM initialization is slow, load it late to prevent terminal startup lag
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"

# --- 5. Aliases (Shortcuts) ---

# Quickly reload Zsh config
alias src="source ~/.zshrc && echo 'Zsh config reloaded!'"

# Quickly edit Zsh config (Uses VS Code if available)
alias zshconfig="code ~/.zshrc"

# GitHub Copilot CLI shortcut (The '??' command)
# Usage: ?? "how to kill process on port 3000"
if command -v gh &> /dev/null; then
    eval "$(gh copilot alias -- zsh)"
    alias '??'='gh copilot suggest'
fi

# Common Git aliases (Muscle memory, even though OMZ has some)
alias gs="git status"
alias gc="git commit -m"
alias gp="git push"

# Enable colors in ls (macOS default ls is monochrome)
alias ls="ls -G"
alias ll="ls -Glh"