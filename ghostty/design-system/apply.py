"""Apply sky/matcha across Ghostty and agent theme preferences."""
from pathlib import Path
from datetime import datetime
import argparse, json, re, shutil, subprocess, tomllib

root=Path(__file__).resolve().parent
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('style',choices=['sky','matcha'])
args=parser.parse_args()
name={'sky':'Slow Sky','matcha':'Matcha Milk'}[args.style]
slug=name.lower().replace(' ','-')
home=Path.home()
ghost=(home/'.config/ghostty/config').resolve(strict=True)
codex=home/'.codex/config.toml'
claude=home/'.claude/settings.json'
g=ghost.read_text(); c=codex.read_text(); a=claude.read_text()
theme=root.parent/'.config/ghostty/themes'/name
palette_text=theme.read_text()
start=g.index('# --- Theme & Appearance ---')
end=g.index('# --- Fonts ---',start)
newg=g[:start]+f'''# --- Theme & Appearance ---

# Semantic OKLCH palette, contrast checked by design-system/build.py.
# Inline colors so a reload explicitly sets the active surface colors.
{palette_text}

# Stable light surface: no native glass or runtime contrast recoloring.
# Existing macOS windows may retain their previous opacity until app restart.
background-opacity = 1
background-blur = false

'''+g[end:]
# Only change the TUI theme; desktop preferences and other settings stay intact.
old_tui=tomllib.loads(c).get('tui',{}).get('theme')
m=re.search(r'(?ms)^\[tui\]\n(.*?)(?=^\[|\Z)',c)
if not m:raise SystemExit('Missing [tui]; no settings changed')
section=m.group(1)
section,count=re.subn(r'^theme\s*=.*$', 'theme = "catppuccin-latte"',section,flags=re.M)
if count!=1:raise SystemExit('Expected exactly one tui.theme; no settings changed')
newc=c[:m.start(1)]+section+c[m.end(1):]
olda=json.loads(a).get('theme')
newa,count=re.subn(r'("theme"\s*:\s*)"[^"\n]*"',lambda m:m.group(1)+json.dumps('custom:'+slug),a)
if count!=1:raise SystemExit('Expected exactly one Claude theme; no settings changed')
tomllib.loads(newc); json.loads(newa)
backup=home/'.local/state/ghostty-themes'/datetime.now().strftime('%Y%m%d-%H%M%S-%f')
backup.mkdir(parents=True)
shutil.copy2(ghost,backup/'ghostty-before.config')
(backup/'previous-theme-preferences.json').write_text(json.dumps({'codex':old_tui,'claude':olda},indent=2)+'\n')
candidate=backup/'ghostty-candidate.config';candidate.write_text(newg)
binary='/Applications/Ghostty.app/Contents/MacOS/ghostty'
subprocess.run([binary,'+validate-config','--config-file='+str(candidate)],check=True)
target=home/'.claude/themes'/(slug+'.json');target.parent.mkdir(parents=True,exist_ok=True)
shutil.copy2(root/(slug+'.claude.json'),target)
ghost.write_text(newg);codex.write_text(newc);claude.write_text(newa)
assert ghost.read_text()==newg
assert tomllib.loads(codex.read_text())['tui']['theme']=='catppuccin-latte'
assert json.loads(claude.read_text())['theme']=='custom:'+slug
assert json.loads(target.read_text())['base']=='light'
subprocess.run([binary,'+validate-config'],check=True)
result=subprocess.run(['osascript','-e','''tell application "Ghostty"
if (count of terminals) is 0 then return "NO_TERMINALS"
return perform action "reload_config" on first terminal
end tell'''],capture_output=True,text=True)
receipt={'style':name,'ghosttyTheme':str(theme),'claudeTheme':str(target),'codexTheme':'catppuccin-latte','backup':str(backup),'reloadActionResult':result.stdout.strip(),'reloadError':result.stderr.strip(),'note':'Config readback verified. Running agent sessions may require /theme or restart to adopt their theme preference.'}
(backup/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
