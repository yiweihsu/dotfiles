# =====================================================
# 0. Oh My Zsh (Framework)
# =====================================================
export ZSH="$HOME/.oh-my-zsh"
DISABLE_AUTO_UPDATE="true"
plugins=(git)
source "$ZSH/oh-my-zsh.sh"


# =====================================================
# 1. Environment & PATH (Early, deterministic)
# =====================================================

# Homebrew (Apple Silicon)
if [[ -x /opt/homebrew/bin/brew ]]; then
  eval "$(/opt/homebrew/bin/brew shellenv)"
fi

# Editor
export EDITOR="vim"

# Java (Homebrew)
export JAVA_HOME="/opt/homebrew/opt/openjdk"
export PATH="$JAVA_HOME/bin:$PATH"

# Antigravity
export PATH="$HOME/.antigravity/antigravity/bin:$PATH"


# =====================================================
# 2. Zsh Core Behavior & Completion
# =====================================================

autoload -Uz compinit
compinit

# Menu selection with arrows
zstyle ':completion:*' menu select

# Case-insensitive + fuzzy-ish matching
zstyle ':completion:*' matcher-list \
  'm:{a-zA-Z}={A-Za-z}' \
  'r:|[._-]=* r:|=*' \
  'l:|=* r:|=*'

# Colored completion (respect LS_COLORS)
zstyle ':completion:*' list-colors "${(s.:.)LS_COLORS}"

# History
HISTFILE="$HOME/.zsh_history"
HISTSIZE=50000
SAVEHIST=50000
setopt HIST_IGNORE_DUPS
setopt APPEND_HISTORY
setopt SHARE_HISTORY


# =====================================================
# 3. Runtime / Language Managers
# =====================================================

# ---- nvm (Homebrew install) ----
export NVM_DIR="$HOME/.nvm"
mkdir -p "$NVM_DIR"

if [[ -s /opt/homebrew/opt/nvm/nvm.sh ]]; then
  source /opt/homebrew/opt/nvm/nvm.sh
fi
if [[ -s /opt/homebrew/opt/nvm/etc/bash_completion.d/nvm ]]; then
  source /opt/homebrew/opt/nvm/etc/bash_completion.d/nvm
fi

# ---- pyenv ----
if command -v pyenv >/dev/null 2>&1; then
  eval "$(pyenv init -)"
fi


# =====================================================
# 4. Modern CLI Enhancements
# =====================================================

# Starship prompt
if command -v starship >/dev/null 2>&1; then
  eval "$(starship init zsh)"
fi

# Zoxide (smart cd)
if command -v zoxide >/dev/null 2>&1; then
  eval "$(zoxide init zsh)"
  alias cd="z"
fi

# Autosuggestions
if [[ -f /opt/homebrew/share/zsh-autosuggestions/zsh-autosuggestions.zsh ]]; then
  source /opt/homebrew/share/zsh-autosuggestions/zsh-autosuggestions.zsh
fi

# Syntax highlighting (must be last among plugins)
if [[ -f /opt/homebrew/share/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh ]]; then
  source /opt/homebrew/share/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh
fi


# =====================================================
# 5. AI / Dev Tools
# =====================================================

# GitHub Copilot CLI
if command -v copilot >/dev/null 2>&1; then
  ask_copilot() {
    if [[ -z "$1" ]]; then
      copilot
    else
      copilot -p "Show me the shell command to: $* . Do not execute it, just display the command and a brief explanation."
    fi
  }
  alias '??'='ask_copilot'
fi

# Codex CLI
if command -v codex >/dev/null 2>&1; then
  alias cx='codex'
  cxe() { [[ -z "$1" ]] && echo "Usage: cxe <prompt>" || codex exec "$*"; }
  cxa() { [[ -z "$1" ]] && echo "Usage: cxa <prompt>" || (echo "⚠️  FULL AUTO"; codex --full-auto "$*"); }
fi


# =====================================================
# 6. Aliases
# =====================================================

# Reload
alias src='source ~/.zshrc && echo "Zsh config reloaded!"'
alias zshconfig='code ~/.zshrc'

# History
alias history='history 1'

# Git
alias g='git'
alias gs='git status'
alias ga='git add'
alias gc='git commit -m'
alias gp='git push'
alias gl='git pull'
alias gd='git diff'
alias glog='git log --oneline --graph --decorate'

# ls
alias ls='ls -G'
alias ll='ls -Glh'
