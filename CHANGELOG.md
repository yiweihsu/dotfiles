# Changelog

## 2026-03-06 — Terminal & Shell 全面升級

### 新增工具

| 工具 | 用途 | 指令 |
|------|------|------|
| **Ghostty** | GPU-accelerated terminal（取代 iTerm2 為主力） | 開啟 app，`Option+Space` toggle Quick Terminal |
| **atuin** | Shell 歷史搜尋（取代 fzf 的 Ctrl+R） | `Ctrl+R` 觸發 atuin 搜尋介面 |
| **direnv** | 進目錄自動載入 `.envrc` 環境變數 | 在目錄放 `.envrc`，進入時自動生效 |
| **lazygit** | TUI git client | `lg` |
| **zellij** | Terminal multiplexer（類似 tmux） | `zellij` |

### 移除

- **Oh My Zsh** — 原本只用 `git` plugin，功能已被 Section 6 自訂 alias 完全覆蓋，移除省去框架載入開銷

### 改動檔案

#### `Brewfile`
- 新增 `cask "ghostty"` + `brew "atuin"` / `"direnv"` / `"lazygit"` / `"zellij"`

#### `zsh/.zshrc`
- 刪除 Section 0（Oh My Zsh 整段，共 7 行）
- Section 4 新增 atuin init、direnv hook
- Section 6 新增 `lg` alias（lazygit）

#### `ghostty/.config/ghostty/config`
- Line 62：`keybind = global:alt+escape=toggle_quick_terminal` → `keybind = global:alt+space=toggle_quick_terminal`
- 效果：Quick Terminal hotkey 改為 Option+Space（與 iTerm2 原本一致）

#### `README.md`
- 標題改為 Ghostty / iTerm2
- Quick Setup 新增 Ghostty config symlink 步驟
- What's Included 新增 Ghostty、atuin、direnv、lazygit、zellij

### Symlinks

```
~/dotfiles/ghostty/.config/ghostty/config  →  ~/.config/ghostty/config   (新建)
~/dotfiles/zsh/.zshrc                      →  ~/.zshrc                   (既有)
~/dotfiles/git/.gitconfig                  →  ~/.gitconfig               (既有)
~/dotfiles/starship/starship.toml          →  ~/.config/starship.toml    (既有)
```

### 跨裝置同步

在其他裝置執行：

```bash
cd ~/dotfiles
git pull
brew bundle install        # 安裝新工具
mkdir -p ~/.config/ghostty
ln -sf ~/dotfiles/ghostty/.config/ghostty/config ~/.config/ghostty/config
source ~/.zshrc
```

### 驗證清單

- [ ] `source ~/.zshrc` — 無錯誤
- [ ] `Ctrl+R` — 出現 atuin 搜尋介面
- [ ] `lg` — 在 git repo 開啟 lazygit TUI
- [ ] `zellij` — 啟動 terminal multiplexer
- [ ] 開啟 Ghostty app → `Option+Space` toggle Quick Terminal
- [ ] `direnv` — 在有 `.envrc` 的目錄驗證自動載入

### 注意事項

- iTerm2 不用刪，兩者並存。試用期間先關掉 iTerm2 的 Option+Space hotkey 避免衝突
- 如果確定不再用 OMZ，可以 `rm -rf ~/.oh-my-zsh` 清除殘留檔案
- Shell 啟動時間 ~1.1s 持平（主要瓶頸是 nvm/conda/pyenv init，不是 OMZ）
