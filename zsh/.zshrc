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
ZSH_THEME=""

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

# ==============================================
# GitHub Copilot CLI (Suggestion Mode)
# ==============================================
if command -v copilot &> /dev/null; then

    function ask_copilot() {
        if [ -z "$1" ]; then
            # No arguments: Start interactive session
            copilot
        else
            # Arguments provided:
            # We append instructions to force it to ONLY show the command.
            # This mimics the old 'gh copilot suggest' behavior.
            copilot -p "Show me the shell command to: $* . Do not execute it, just display the command and a brief explanation."
        fi
    }

    alias '??'='ask_copilot'
fi

# Common Git aliases (Muscle memory, even though OMZ has some)
alias gs="git status"
alias gc="git commit -m"
alias gp="git push"

# Enable colors in ls (macOS default ls is monochrome)
alias ls="ls -G"
alias ll="ls -Glh"


# ==============================================
# Codex CLI Configuration
# ==============================================

# Check if 'codex' is installed
if command -v codex &> /dev/null; then

    # 1. Standard Interactive Mode
    # Usage: cx "how do I center a div"
    # This enters the interactive session with your prompt.
    alias cx='codex'

    # 2. Non-Interactive Execution Mode (The "One-Shot" mode)
    # Usage: cxe "list all files larger than 100mb"
    # This uses the 'exec' subcommand to run non-interactively.
    # It will likely ask for confirmation before running dangerous commands
    # unless configured otherwise.
    function cxe() {
        if [ -z "$1" ]; then
            echo "Usage: cxe <prompt>"
        else
            codex exec "$*"
        fi
    }

    # 3. Full Auto Mode (Danger Zone)
    # Usage: cxa "fix the bug in main.rs"
    # This uses --full-auto (low-friction, workspace-write access).
    # Use this when you trust the agent to read/write files without asking every time.
    function cxa() {
        if [ -z "$1" ]; then
            echo "Usage: cxa <prompt>"
        else
            echo "⚠️  Running Codex in FULL AUTO mode..."
            codex --full-auto "$*"
        fi
    }
fi