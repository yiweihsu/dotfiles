if [[ -x /opt/homebrew/bin/brew ]]; then
  eval "$(/opt/homebrew/bin/brew shellenv)"
fi

export _ZO_DOCTOR=0
# Added by Antigravity CLI installer
export PATH="$HOME/.local/bin:$PATH"
