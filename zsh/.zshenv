# Loaded by every zsh process, including non-interactive scripts.
# Keep this file tiny and side-effect free.
typeset -U path PATH
[[ -d "$HOME/.cargo/bin" ]] && path=("$HOME/.cargo/bin" $path)
[[ -d "$HOME/.foundry/bin" ]] && path=("$HOME/.foundry/bin" $path)
