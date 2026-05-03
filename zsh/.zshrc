# =====================================================
# 1. Environment & PATH (Early, deterministic)
# =====================================================

# Homebrew (Apple Silicon)
if [[ -x /opt/homebrew/bin/brew ]]; then
  eval "$(/opt/homebrew/bin/brew shellenv)"
fi

typeset -U path PATH
path=(
  "$HOME/bin"
  "$HOME/.local/bin"
  "$HOME/.cargo/bin"
  "$HOME/.foundry/bin"
  "$HOME/.antigravity/antigravity/bin"
  $path
)

# Editor
export EDITOR="micro"
export _ZO_DOCTOR=0


# =====================================================
# 2. Zsh Core Behavior & Completion
# =====================================================

[[ -d "$HOME/.docker/completions" ]] && fpath=("$HOME/.docker/completions" $fpath)

autoload -Uz compinit

# Menu selection with arrows
zstyle ':completion:*' menu select

# Case-insensitive + fuzzy-ish matching
zstyle ':completion:*' matcher-list \
  'm:{a-zA-Z}={A-Za-z}' \
  'r:|[._-]=* r:|=*' \
  'l:|=* r:|=*'

# Colored completion (respect LS_COLORS)
zstyle ':completion:*' list-colors "${(s.:.)LS_COLORS}"
zstyle ':completion:*' use-cache on
zstyle ':completion:*' cache-path "$HOME/.cache/zsh"

mkdir -p "$HOME/.cache/zsh"
if [[ -s "$HOME/.zcompdump" ]]; then
  compinit -C
else
  compinit
fi

# History
HISTFILE="$HOME/.zsh_history"
HISTSIZE=50000
SAVEHIST=50000
setopt HIST_IGNORE_DUPS
setopt APPEND_HISTORY
setopt SHARE_HISTORY
setopt HIST_IGNORE_SPACE
setopt HIST_REDUCE_BLANKS


# =====================================================
# 3. Runtime / Language Managers
# =====================================================

# ---- nvm (Homebrew install) ----
export NVM_DIR="$HOME/.nvm"
mkdir -p "$NVM_DIR"

__load_nvm() {
  unfunction nvm node npm npx corepack 2>/dev/null
  [[ -s /opt/homebrew/opt/nvm/nvm.sh ]] && source /opt/homebrew/opt/nvm/nvm.sh
  [[ -s /opt/homebrew/opt/nvm/etc/bash_completion.d/nvm ]] && source /opt/homebrew/opt/nvm/etc/bash_completion.d/nvm
}
nvm() { __load_nvm; nvm "$@"; }
node() { __load_nvm; command node "$@"; }
npm() { __load_nvm; command npm "$@"; }
npx() { __load_nvm; command npx "$@"; }
corepack() { __load_nvm; command corepack "$@"; }

# ---- pyenv ----
if command -v pyenv >/dev/null 2>&1; then
  eval "$(pyenv init -)"
fi

# ---- conda (lazy load; avoids paying the startup cost on every shell) ----
__load_conda() {
  unfunction conda 2>/dev/null
  local conda_bin="/opt/homebrew/Caskroom/miniconda/base/bin/conda"
  local conda_sh="/opt/homebrew/Caskroom/miniconda/base/etc/profile.d/conda.sh"
  local __conda_setup

  if [[ -x "$conda_bin" ]]; then
    __conda_setup="$("$conda_bin" shell.zsh hook 2>/dev/null)"
    if [[ $? -eq 0 ]]; then
      eval "$__conda_setup"
    elif [[ -f "$conda_sh" ]]; then
      source "$conda_sh"
    else
      path=("/opt/homebrew/Caskroom/miniconda/base/bin" $path)
    fi
    unset __conda_setup
  fi
}
conda() { __load_conda; conda "$@"; }


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
  if command -v fd >/dev/null 2>&1; then
    export FZF_DEFAULT_COMMAND='fd --hidden --strip-cwd-prefix --exclude .git'
    export FZF_CTRL_T_COMMAND="$FZF_DEFAULT_COMMAND"
    export FZF_ALT_C_COMMAND='fd --type=d --hidden --strip-cwd-prefix --exclude .git'
  fi
  source <(fzf --zsh)
  export FZF_DEFAULT_OPTS=" \
    --color=bg+:#1b2b34,bg:#0f111a,spinner:#89ddff,hl:#82aaff \
    --color=fg:#c5d3e0,header:#89ddff,info:#c792ea,pointer:#89ddff \
    --color=marker:#c792ea,fg+:#ffffff,prompt:#82aaff,hl+:#ffcb6b \
    --color=selected-bg:#263238 \
    --border='rounded' --prompt=' ' --pointer='' \
    --separator='─' --scrollbar='│' --info='right'"
  if command -v bat >/dev/null 2>&1; then
    export FZF_CTRL_T_OPTS="--preview 'bat --color=always --style=numbers --line-range=:200 {} 2>/dev/null || ls -la {}'"
  fi
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

croot() {
  local root
  root="$(git rev-parse --show-toplevel 2>/dev/null)" || return 1
  cd "$root"
}

take() {
  if [[ -z "$1" ]]; then
    echo "Usage: take <dir>"
    return 1
  fi
  mkdir -p "$1" && cd "$1"
}

ff() {
  if command -v fd >/dev/null 2>&1 && command -v fzf >/dev/null 2>&1; then
    fd --hidden --strip-cwd-prefix --exclude .git "${1:-}" |
      fzf --preview 'bat --color=always --style=numbers --line-range=:200 {} 2>/dev/null || ls -la {}'
  else
    echo "ff requires fd and fzf"
    return 1
  fi
}

fcd() {
  if command -v fd >/dev/null 2>&1 && command -v fzf >/dev/null 2>&1; then
    local dir
    dir="$(fd --type=d --hidden --strip-cwd-prefix --exclude .git | fzf)"
    [[ -n "$dir" ]] && cd "$dir"
  else
    echo "fcd requires fd and fzf"
    return 1
  fi
}

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

alias ..='cd ..'
alias ...='cd ../..'
alias c='clear'

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

if command -v yazi >/dev/null 2>&1; then
  y() {
    local tmp
    tmp="$(mktemp -t yazi-cwd.XXXXXX)"
    yazi "$@" --cwd-file="$tmp"
    if [[ -s "$tmp" ]]; then
      local cwd
      cwd="$(cat "$tmp")"
      [[ -n "$cwd" && "$cwd" != "$PWD" ]] && cd "$cwd"
    fi
    rm -f "$tmp"
  }
fi

if command -v uv >/dev/null 2>&1; then
  alias uvr='uv run'
  alias uvs='uv sync'
fi

if command -v mise >/dev/null 2>&1; then
  eval "$(mise activate zsh)"
  alias mr='mise run'
fi

# pnpm
export PNPM_HOME="$HOME/Library/pnpm"
[[ -d "$PNPM_HOME" ]] && path=("$PNPM_HOME" $path)
# pnpm end

# =====================================================
# 7. Welcome / System Snapshot
# =====================================================

splash() {
  if command -v figlet >/dev/null 2>&1 && command -v lolcat >/dev/null 2>&1; then
    figlet -f slant "YW" | lolcat -f
  fi
  command -v fastfetch >/dev/null 2>&1 && fastfetch
}

[[ -n "$YW_SPLASH_ON_START" ]] && splash

# =====================================================
# 8. Google Cloud SA auth (永不過期)
# =====================================================
# SA keys: ~/.config/gcloud/keys/<project>.json (Editor role per project).
# Default ADC + gcloud account = pokai-ai。用 gcp-* alias 切其他 project。
# gcp-user 切回 yiwei.hsu@ablauf.io 做 IAM/billing/org-level 操作。
export GOOGLE_APPLICATION_CREDENTIALS="$HOME/.config/gcloud/keys/pokai-ai.json"

alias gcp-pokai='gcloud config set account local-dev@pokai-ai.iam.gserviceaccount.com && gcloud config set project pokai-ai && export GOOGLE_APPLICATION_CREDENTIALS=$HOME/.config/gcloud/keys/pokai-ai.json'
alias gcp-mokuhjem='gcloud config set account local-dev@mokuhjem.iam.gserviceaccount.com && gcloud config set project mokuhjem && export GOOGLE_APPLICATION_CREDENTIALS=$HOME/.config/gcloud/keys/mokuhjem.json'
alias gcp-tools='gcloud config set account local-dev@ablauf-tools.iam.gserviceaccount.com && gcloud config set project ablauf-tools && export GOOGLE_APPLICATION_CREDENTIALS=$HOME/.config/gcloud/keys/ablauf-tools.json'
alias gcp-user='gcloud config set account yiwei.hsu@ablauf.io'
export PATH="$HOME/bin:$PATH"
