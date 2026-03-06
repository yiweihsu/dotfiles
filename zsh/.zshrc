# =====================================================
# 1. Environment & PATH (Early, deterministic)
# =====================================================

# Homebrew (Apple Silicon)
if [[ -x /opt/homebrew/bin/brew ]]; then
  eval "$(/opt/homebrew/bin/brew shellenv)"
fi

# Editor
export EDITOR="vim"

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

# fzf (fuzzy finder)
if command -v fzf >/dev/null 2>&1; then
  source <(fzf --zsh)
  export FZF_DEFAULT_OPTS=" \
    --color=bg+:#313244,bg:#1e1e2e,spinner:#f5e0dc,hl:#f38ba8 \
    --color=fg:#cdd6f4,header:#f38ba8,info:#cba6f7,pointer:#f5e0dc \
    --color=marker:#b4befe,fg+:#cdd6f4,prompt:#cba6f7,hl+:#f38ba8 \
    --color=selected-bg:#45475a \
    --border='rounded' --prompt=' ' --pointer='' \
    --separator='─' --scrollbar='│' --info='right'"
fi

# Autosuggestions
if [[ -f /opt/homebrew/share/zsh-autosuggestions/zsh-autosuggestions.zsh ]]; then
  source /opt/homebrew/share/zsh-autosuggestions/zsh-autosuggestions.zsh
fi

# Atuin (shell history — replaces fzf Ctrl+R)
if command -v atuin >/dev/null 2>&1; then
  eval "$(atuin init zsh)"
fi

# direnv (per-directory env)
if command -v direnv >/dev/null 2>&1; then
  eval "$(direnv hook zsh)"
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

# lazygit
if command -v lazygit >/dev/null 2>&1; then
  alias lg='lazygit'
fi

# Git
alias g='git'
alias gs='git status'
alias ga='git add'
alias gc='git commit -m'
alias gp='git push'
alias gl='git pull'
alias gd='git diff'
alias gds='git diff --staged'
alias glog='git log --oneline --graph --decorate'

# ls (eza)
if command -v eza >/dev/null 2>&1; then
  alias ls='eza --icons --group-directories-first'
  alias ll='eza -l --icons --group-directories-first --git --time-style=relative'
  alias la='eza -la --icons --group-directories-first --git --time-style=relative'
  alias lt='eza --tree --level=2 --icons --group-directories-first'
else
  alias ls='ls -G'
  alias ll='ls -Glh'
fi

# bat (syntax-highlighted cat)
if command -v bat >/dev/null 2>&1; then
  alias cat='bat --paging=never'
  alias catp='bat'
  export BAT_THEME="Catppuccin Mocha"
  export MANPAGER="sh -c 'col -bx | bat -l man -p'"
fi

# delta (git diff pager)
if command -v delta >/dev/null 2>&1; then
  export GIT_PAGER="delta"
fi

# Added by Antigravity
export PATH="/Users/yiweihsu/.antigravity/antigravity/bin:$PATH"

# >>> conda initialize >>>
# !! Contents within this block are managed by 'conda init' !!
__conda_setup="$('/opt/homebrew/Caskroom/miniconda/base/bin/conda' 'shell.zsh' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
    eval "$__conda_setup"
else
    if [ -f "/opt/homebrew/Caskroom/miniconda/base/etc/profile.d/conda.sh" ]; then
        . "/opt/homebrew/Caskroom/miniconda/base/etc/profile.d/conda.sh"
    else
        export PATH="/opt/homebrew/Caskroom/miniconda/base/bin:$PATH"
    fi
fi
unset __conda_setup
# <<< conda initialize <<<

# The following lines have been added by Docker Desktop to enable Docker CLI completions.
fpath=(/Users/yiweihsu/.docker/completions $fpath)
autoload -Uz compinit
compinit
# End of Docker CLI completions
export PATH="$HOME/.local/bin:$PATH"

# pnpm
export PNPM_HOME="/Users/yiweihsu/Library/pnpm"
case ":$PATH:" in
  *":$PNPM_HOME:"*) ;;
  *) export PATH="$PNPM_HOME:$PATH" ;;
esac
# pnpm end
