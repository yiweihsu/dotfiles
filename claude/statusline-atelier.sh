#!/bin/bash
# Claude Code stdin JSON -> a single, restrained ANSI status line.
set -euo pipefail
input=$(cat)
fields=$(printf '%s' "$input" | /usr/bin/jq -r '
  def clean: tostring | explode | map(select(. >= 32 and (. < 127 or . > 159))) | implode;
  [(.model.display_name // "Claude" | clean),
   (.workspace.current_dir // .cwd // "" | clean),
   (.context_window.used_percentage // -1 | tonumber | floor),
   ((.context_window.total_input_tokens // 0) + (.context_window.total_output_tokens // 0))]
  | .[]')
model=$(printf '%s\n' "$fields" | sed -n '1p')
cwd=$(printf '%s\n' "$fields" | sed -n '2p')
used=$(printf '%s\n' "$fields" | sed -n '3p')
total=$(printf '%s\n' "$fields" | sed -n '4p')
case "$cwd" in
  "$HOME") cwd='~' ;;
  "$HOME"/*) cwd="~/${cwd#"$HOME"/}" ;;
esac
if [ "${#cwd}" -gt 36 ]; then cwd="…/${cwd##*/}"; fi
reset=$'\033[0m'
ink=$'\033[38;2;222;219;211m'
muted=$'\033[38;2;146;157;155m'
accent=$'\033[38;2;165;185;161m'
if [ "$used" -ge 85 ]; then accent=$'\033[38;2;207;139;131m'
elif [ "$used" -ge 65 ]; then accent=$'\033[38;2;200;179;138m'; fi
printf '%s%s%s  ·  %s%s' "$ink" "$model" "$muted" "$cwd" "$reset"
if [ "$used" -ge 0 ]; then
  [ "$used" -le 100 ] || used=100
  filled=$((used / 10))
  printf '  %s' "$accent"
  for ((i=0; i<10; i++)); do
    if [ "$i" -lt "$filled" ]; then printf '━'; else printf '%s─' "$muted"; fi
  done
  printf ' %s%s%% ctx%s' "$accent" "$used" "$reset"
else
  printf '  %sctx --%s' "$muted" "$reset"
fi
if [ "$total" -gt 0 ]; then
  tokens=$(awk -v n="$total" 'BEGIN {if(n>=1000000) printf "%.1fM",n/1000000; else if(n>=1000) printf "%.0fk",n/1000; else printf "%d",n}')
  printf '  %s·  %s tok%s' "$muted" "$tokens" "$reset"
fi
printf '\n'
