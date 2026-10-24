#!/usr/bin/env python3
"""Terminal themes: one palette drives Ghostty, Claude Code and Codex.

  term-theme list                   themes and which one is active
  term-theme check [slug]           WCAG contrast report (all text >= 4.5:1)
  term-theme apply <slug> [--dry-run]
  term-theme preview <slug>...       side-by-side palette cards (PNG), no terminal windows
"""
import argparse, datetime, difflib, json, re, shutil, subprocess, sys, tomllib
from pathlib import Path
def lum(h):
    h=h.lstrip('#'); c=[int(h[i:i+2],16)/255 for i in (0,2,4)]
    c=[x/12.92 if x<=0.03928 else ((x+0.055)/1.055)**2.4 for x in c]
    return 0.2126*c[0]+0.7152*c[1]+0.0722*c[2]
def cr(a,b):
    la,lb=sorted([lum(a),lum(b)],reverse=True); return (la+0.05)/(lb+0.05)

T = {
 # A: warm oat paper; colour lives in accents, not the surface.
 "oat-matcha": dict(name="Oat Matcha", base="light",
   bg="#f5f0e6", surface="#ebe4d6", surface2="#e2dac9", selection="#d6e5c4",
   text="#2e2a24", muted="#665f53", faint="#8a8273", border="#c9bfac",
   matcha="#336a22", sky="#195f9a", hojicha="#93461f", red="#a5302a",
   amber="#735200", plum="#6e4590", teal="#16645f",
   addbg="#dcebcc", rmbg="#f6dcd5", addw="#bfdca5", rmw="#eebcb0",
   cursor="#336a22"),
 # B: deep ink-green night; vivid matcha + sky on a quiet base.
 "night-matcha": dict(name="Night Matcha", base="dark",
   bg="#161d18", surface="#202a22", surface2="#2a362c", selection="#2c4228",
   text="#e7e3d7", muted="#a3ad9c", faint="#7b8777", border="#3e4c3f",
   matcha="#a6d672", sky="#7cc0f2", hojicha="#eba06a", red="#f48c82",
   amber="#e8c46b", plum="#c9a8e8", teal="#72d1c1",
   addbg="#24402a", rmbg="#46262a", addw="#35603a", rmw="#6c3439",
   cursor="#a6d672"),
 # B1: cool deep forest; matcha is the brand accent everywhere.
 "forest-matcha": dict(name="Forest Matcha", base="dark",
   bg="#13241a", surface="#1b3223", surface2="#25412e", selection="#274630",
   text="#e4ecd8", muted="#a5b89d", faint="#83977d", border="#3d5c45",
   matcha="#aedd74", sky="#82c6f0", hojicha="#eca56e", red="#f89c92",
   amber="#e8c96e", plum="#cab0e8", teal="#78d8c2",
   addbg="#21432a", rmbg="#4a2a2c", addw="#356a3c", rmw="#70383b",
   cursor="#aedd74", brand="#aedd74", pborder="#5d8a5c"),
 # B2: koicha, warm yellow-green like matcha powder in a dark tea bowl.
 "koicha": dict(name="Koicha", base="dark",
   bg="#1f2613", surface="#2a331a", surface2="#353f20", selection="#3a4620",
   text="#f2eedb", muted="#c2c19d", faint="#9e9c7a", border="#57612f",
   matcha="#cddc76", sky="#8cc6e2", hojicha="#f4b47e", red="#fba49a",
   amber="#f0d27a", plum="#dab6dc", teal="#95d6b0",
   addbg="#2f4419", rmbg="#4f2e20", addw="#47642a", rmw="#78402f",
   cursor="#cddc76", brand="#cddc76", pborder="#7a8a44"),
 # Wa-iro: 柳煤竹 base, 裏柳 hero.
 "urayanagi": dict(name="Urayanagi 裏柳", base="dark",
   bg="#1e2418", surface="#283022", surface2="#323d29", selection="#303b29",
   text="#f0eedf", muted="#bcc1a8", faint="#979c84", border="#55644a",
   sky="#93b8cc", hojicha="#d8ab74", red="#ea9e90",
   amber="#d8cf7c", plum="#c9adcb", teal="#9fcbb2",
   addbg="#2b3f23", rmbg="#472d24", addw="#3e5a32", rmw="#6a3d31",
   pborder="#6c7a52", matcha="#b5caa0", cursor="#b5caa0", brand="#b5caa0"),
 # Wa-iro: 柳煤竹 base, 柳染 hero.
 "yanagizome": dict(name="Yanagizome 柳染", base="dark",
   bg="#1e2418", surface="#283022", surface2="#323d29", selection="#303b29",
   text="#f0eedf", muted="#bcc1a8", faint="#979c84", border="#55644a",
   sky="#93b8cc", hojicha="#d8ab74", red="#ea9e90",
   amber="#d8cf7c", plum="#c9adcb", teal="#9fcbb2",
   addbg="#2b3f23", rmbg="#472d24", addw="#3e5a32", rmw="#6a3d31",
   pborder="#6c7a52", matcha="#91ad70", cursor="#91ad70", brand="#91ad70"),
 # Ube night: ube-ink base, ube hero, 裏柳 matcha as the complementary accent.
 "ube": dict(name="Ube", base="dark",
   bg="#1d1828", surface="#272035", surface2="#312843", selection="#2f2741",
   text="#eee4ff", muted="#c2b6da", faint="#9b90b3", border="#504470",
   matcha="#b5caa0", sky="#8fc0ec", hojicha="#f0b07a", red="#f59aa8",
   amber="#ecd08a", plum="#c9a6ff", teal="#8fd4c8",
   addbg="#243a2a", rmbg="#46243a", addw="#36573e", rmw="#6c3352",
   cursor="#ccadff", brand="#bb92ff", pborder="#7a62a8"),
 # Ube milk: light ube surface; ube #aa77ff for non-text accents only.
 "ube-milk": dict(name="Ube Milk", base="light",
   bg="#f3ecff", surface="#e9defc", surface2="#dfd1f9", selection="#ddcdfb",
   text="#2a2238", muted="#5c5272", faint="#7d7294", border="#c3b2e4",
   matcha="#3a6526", sky="#1d5c92", hojicha="#8e421d", red="#a42d3c",
   amber="#6e4c00", plum="#7e2c7c", teal="#145f5a",
   addbg="#dcecd3", rmbg="#f9dde5", addw="#c2dcb2", rmw="#f0c0cf",
   cursor="#aa77ff", brand="#6b3fc4", pborder="#aa77ff",
   ansi8="#685e80", ansi15="#3e3550", ansi_magenta="#6b3fc4"),
 # Matcha latte: Ube Milk's recipe in a warm matcha hue. 苔 brand, 松葉 success,
 # 柳染 #91ad70 for non-text accents only, ube purple as the complementary accent.
 "matcha-latte": dict(name="Matcha Latte", base="light",
   bg="#f1f2e1", surface="#e6e9cf", surface2="#dce2c2", selection="#dbe2bc",
   text="#272c1b", muted="#555c43", faint="#757c61", border="#bcc79f",
   matcha="#33622a", sky="#1d5c92", hojicha="#8a421d", red="#a42d3c",
   amber="#6a4c00", plum="#6b3fc4", teal="#145f5a",
   addbg="#dae9c6", rmbg="#f6ddd2", addw="#bfd9a3", rmw="#efc1b4",
   cursor="#91ad70", brand="#576313", pborder="#91ad70",
   ansi8="#5f6750", ansi15="#363d2a", ansi_magenta="#576313"),
}

def ghostty(t):
    light = t["base"]=="light"
    pal = [t["surface2"] if not light else t["text"], t["red"], t["matcha"], t["amber"], t["sky"], t.get("ansi_magenta",t["plum"]), t["teal"],
           t["muted"] if light else "#cdc8bb",
           t.get("ansi8", t["faint"] if not light else "#6b6457"), t["red"], t["matcha"], t["amber"], t["sky"], t.get("ansi_magenta",t["plum"]), t["teal"],
           t.get("ansi15", "#48423a" if light else "#f6f3ea")]
    L=[f"# {t['name']}",f"background = {t['bg']}",f"foreground = {t['text']}",
       f"selection-background = {t['selection']}",f"selection-foreground = {t['text']}",
       f"cursor-color = {t['cursor']}",f"cursor-text = {t['bg']}",f"split-divider-color = {t['border']}"]
    L+= [f"palette = {i}={c}" for i,c in enumerate(pal)]
    return "\n".join(L)+"\n", pal

def claude(t):
    o = dict(text=t["text"], inverseText=t["bg"], inactive=t["muted"], subtle=t["border"],
      claude=t.get("brand",t["hojicha"]), claudeShimmer=t["amber"], success=t["matcha"], error=t["red"],
      warning=t["amber"], warningShimmer=t["hojicha"], merged=t["plum"], permission=t["sky"],
      permissionShimmer=t["teal"], remember=t["plum"], suggestion=t["sky"],
      promptBorder=t.get("pborder",t["border"]), promptBorderShimmer=t["matcha"], planMode=t["teal"],
      autoAccept=t["matcha"], bashBorder=t["hojicha"], ide=t["sky"], fastMode=t["hojicha"],
      fastModeShimmer=t["amber"], inactiveShimmer=t["faint"],
      diffAdded=t["addbg"], diffRemoved=t["rmbg"], diffAddedDimmed=t["surface"], diffRemovedDimmed=t["surface"],
      diffAddedWord=t["addw"], diffRemovedWord=t["rmw"],
      userMessageBackground=t["surface"], userMessageBackgroundHover=t["surface2"],
      bashMessageBackgroundColor=t["surface"], memoryBackgroundColor=t["surface"],
      selectionBg=t["selection"], composerSidebarBackground=t["surface"],
      rate_limit_fill=t["matcha"], rate_limit_empty=t["border"],
      briefLabelYou=t["sky"], briefLabelClaude=t.get("brand",t["hojicha"]))
    return {"name":t["name"],"base":t["base"],"overrides":o}


# Exploration drafts from 2026-10-24: readable, but not yet at Ube Milk quality.
DRAFTS = {"oat-matcha","night-matcha","forest-matcha","koicha","urayanagi","yanagizome","ube"}

HOME = Path.home()
GHOSTTY_BIN = "/Applications/Ghostty.app/Contents/MacOS/ghostty"
GHOSTTY_CFG = (HOME/".config/ghostty/config").resolve()
CLAUDE_SETTINGS = HOME/".claude/settings.json"
CLAUDE_THEMES = HOME/".claude/themes"
CODEX_CFG = HOME/".codex/config.toml"
CODEX_THEME = "base16-256"  # Codex syntax colors follow the Ghostty ANSI palette.
BACKUPS = HOME/".local/state/ghostty-themes"
BEGIN = "# >>> theme (managed by design-system/palettes.py; switch with `term-theme apply <slug>`) >>>"
END = "# <<< theme (managed by design-system/palettes.py) <<<"

def contrast_report(slug, t, verbose=True):
    _, pal = ghostty(t); low = []
    for fg in ["text","muted","matcha","sky","hojicha","red","amber","plum","teal"]:
        for bgk in ["bg","surface","addbg","rmbg","selection"]:
            r = cr(t[fg], t[bgk])
            if r < 4.5: low.append(f"{fg} on {bgk} {r:.2f}")
    if verbose:
        print(f"== {slug} ({t['name']}, {t['base']})")
        print(f"  text {cr(t['text'],t['bg']):.2f}  muted {cr(t['muted'],t['bg']):.2f}  ansi8 {cr(pal[8],t['bg']):.2f}  faint {cr(t['faint'],t['bg']):.2f}")
        for x in low: print(f"  LOW  {x}")
        print("  ok" if not low else f"  {len(low)} pair(s) below 4.5:1")
    return not low

def ghostty_block(t):
    light = t["base"] == "light"
    lines = [BEGIN, f"# {t['name']}: generated palette, text contrast >= 4.5:1.", ghostty(t)[0].rstrip("\n")]
    if light:
        lines += ["# Light theme: no native glass; Ghostty 1.3.1 glass + minimum-contrast turns dark text white.",
                  "background-opacity = 1", "background-blur = false"]
    else:
        lines += ["background-opacity = 0.97", "background-blur = macos-glass-regular"]
    lines += ["minimum-contrast = 1", "faint-opacity = 1", END]
    return "\n".join(lines)

def new_ghostty_cfg(text, t):
    if text.count(BEGIN) != 1 or text.count(END) != 1:
        sys.exit(f"Ghostty config has no managed theme block: {GHOSTTY_CFG}")
    a = text.index(BEGIN); b = text.index(END) + len(END)
    return text[:a] + ghostty_block(t) + text[b:]

def new_claude_settings(text, slug):
    pat = r'("theme"\s*:\s*)"[^"]*"'
    if len(re.findall(pat, text)) != 1: sys.exit('Expected exactly one "theme" key in Claude settings.json')
    out = re.sub(pat, lambda m: f'{m.group(1)}"custom:{slug}"', text)
    json.loads(out); return out

def new_codex_cfg(text):
    m = re.search(r'(?m)^\[tui\]\s*$', text)
    if not m: sys.exit("No [tui] table in Codex config.toml")
    nxt = re.search(r'(?m)^\[', text[m.end():])
    end = m.end() + (nxt.start() if nxt else len(text[m.end():]))
    sec = text[m.end():end]
    if re.search(r'(?m)^theme\s*=', sec):
        sec = re.sub(r'(?m)^theme\s*=.*$', f'theme = "{CODEX_THEME}"', sec, count=1)
    else:
        sec = f'\ntheme = "{CODEX_THEME}"' + sec
    out = text[:m.end()] + sec + text[end:]
    if tomllib.loads(out)["tui"]["theme"] != CODEX_THEME: sys.exit("Codex config readback failed")
    return out

def active():
    try: return json.loads(CLAUDE_SETTINGS.read_text()).get("theme","").removeprefix("custom:")
    except Exception: return ""

def apply(slug, dry):
    if slug not in T: sys.exit(f"Unknown theme '{slug}'. Try: term-theme list")
    t = T[slug]
    if not contrast_report(slug, t, verbose=False):
        contrast_report(slug, t); sys.exit("Refusing to apply: contrast check failed.")
    files = {GHOSTTY_CFG: new_ghostty_cfg, CLAUDE_SETTINGS: None, CODEX_CFG: None}
    old = {f: f.read_text() for f in files}
    new = {GHOSTTY_CFG: new_ghostty_cfg(old[GHOSTTY_CFG], t),
           CLAUDE_SETTINGS: new_claude_settings(old[CLAUDE_SETTINGS], slug),
           CODEX_CFG: new_codex_cfg(old[CODEX_CFG])}
    theme_json = json.dumps(claude(t), indent=2, ensure_ascii=False) + "\n"
    if dry:
        for f in files:
            d = list(difflib.unified_diff(old[f].splitlines(), new[f].splitlines(), str(f), str(f), lineterm="", n=1))
            print("\n".join(d) if d else f"(unchanged) {f}")
        print(f"(would write) {CLAUDE_THEMES/(slug+'.json')}")
        return
    backup = BACKUPS/datetime.datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    backup.mkdir(parents=True)
    for f in files: shutil.copy2(f, backup/f.name)
    CLAUDE_THEMES.mkdir(exist_ok=True)
    (CLAUDE_THEMES/f"{slug}.json").write_text(theme_json)
    for f in files: f.write_text(new[f])
    v = subprocess.run([GHOSTTY_BIN, "+validate-config"], capture_output=True, text=True)
    if v.returncode != 0:
        for f in files: shutil.copy2(backup/f.name, f)
        sys.exit(f"Ghostty rejected the config, restored from {backup}:\n{v.stdout}{v.stderr}")
    r = subprocess.run(["osascript", "-e", 'tell application "Ghostty"\nif (count of terminals) is 0 then return "NO_TERMINALS"\nreturn perform action "reload_config" on first terminal\nend tell'], capture_output=True, text=True)
    shown = subprocess.run([GHOSTTY_BIN, "+show-config"], capture_output=True, text=True).stdout
    bg = re.search(r'(?m)^background = (\S+)', shown)
    receipt = {"theme": slug, "ghosttyBackground": bg.group(1) if bg else None,
               "claudeTheme": json.loads(CLAUDE_SETTINGS.read_text())["theme"],
               "codexTheme": tomllib.loads(CODEX_CFG.read_text())["tui"]["theme"],
               "ghosttyReload": (r.stdout or r.stderr).strip(), "backup": str(backup)}
    (backup/"receipt.json").write_text(json.dumps(receipt, indent=2, ensure_ascii=False) + "\n")
    ok = receipt["ghosttyBackground"] == t["bg"] and receipt["claudeTheme"] == f"custom:{slug}" and receipt["codexTheme"] == CODEX_THEME
    print(json.dumps(receipt, indent=2, ensure_ascii=False))
    print(f"\n{'Applied' if ok else 'Applied with readback mismatch'}: {t['name']}. "
          "Running sessions: Claude Code /theme -> pick it; restart Codex (it detects the background at startup).")
    if not ok: sys.exit(1)

def card(t, W=1100, H=760):
    from PIL import Image, ImageDraw, ImageFont
    font = lambda n: ImageFont.truetype(str(HOME/"Library/Fonts/Sarasa-SuperTTC.ttc"), n, index=0)
    brand = t.get("brand", t["hojicha"]); f = font(26); im = Image.new("RGB", (W, H), t["bg"]); d = ImageDraw.Draw(im)
    d.text((30, 18), t["name"], fill=brand, font=font(34)); y = 80
    d.rectangle([20, y-10, W-20, y+44], fill=t["surface"]); d.text((40, y), "› 幫我把 greet() 加上 name 參數", fill=t["text"], font=f); y += 80
    d.text((30, y), "●", fill=brand, font=f); d.text((60, y), "現在修改 ", fill=t["text"], font=f)
    d.text((60+f.getlength("現在修改 "), y), "greet()", fill=t["sky"], font=f); y += 52
    d.text((30, y), "● Update(demo.py)", fill=t["matcha"], font=f); y += 48
    d.rectangle([60, y-6, W-40, y+36], fill=t["rmbg"]); d.text((80, y), "- def greet():", fill=t["text"], font=f); y += 42
    d.rectangle([60, y-6, W-40, y+36], fill=t["addbg"]); d.text((80, y), '+ def greet(name: str = "世界") -> None:', fill=t["text"], font=f); y += 62
    for k, lab in [("muted", "次要文字 Read 1 file"), ("hojicha", "焙茶 · 強調"), ("amber", "警告 · auto mode"),
                   ("red", "錯誤 · failed"), ("plum", "紫 · merged"), ("teal", "青磁 · plan mode")]:
        d.text((40, y), lab, fill=t[k], font=f); y += 42
    d.line([20, y+6, W-20, y+6], fill=t.get("pborder", t["border"]), width=3)
    d.text((40, y+18), "›", fill=brand, font=f); d.rectangle([66, y+20, 80, y+50], fill=t["cursor"])
    d.text((100, y+18), "~/Workspace", fill=t["text"], font=font(26)); x = 30
    for k in ["bg", "surface", "text", "muted", "matcha", "sky", "hojicha", "amber", "red", "plum", "teal"]:
        d.rectangle([x, H-62, x+52, H-14], fill=t[k], outline=t["border"]); x += 58
    d.rectangle([x, H-62, x+52, H-14], fill=brand, outline=t["border"]); x += 58
    d.rectangle([x, H-62, x+52, H-14], fill=t["cursor"], outline=t["border"])
    return im

def preview(slugs, out):
    from PIL import Image
    cards = [card(T[s]) for s in slugs]; pad = 24
    sheet = Image.new("RGB", (sum(c.width for c in cards) + pad*(len(cards)+1), cards[0].height + 2*pad), "#d9d6cf")
    x = pad
    for c in cards: sheet.paste(c, (x, pad)); x += c.width + pad
    sheet.save(out); subprocess.run(["open", str(out)]); print(out)

def main():
    ap = argparse.ArgumentParser(prog="term-theme", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list")
    c = sub.add_parser("check"); c.add_argument("slug", nargs="?")
    a = sub.add_parser("apply"); a.add_argument("slug"); a.add_argument("--dry-run", action="store_true")
    pv = sub.add_parser("preview"); pv.add_argument("slugs", nargs="+"); pv.add_argument("-o", "--out", default=str(BACKUPS.parent/"term-theme-preview.png"))
    args = ap.parse_args()
    if args.cmd == "list":
        cur = active()
        for slug, t in T.items():
            print(f"{'*' if slug == cur else ' '} {slug:14} {t['name']:18} {t['base']:5} bg {t['bg']}{'  (draft)' if slug in DRAFTS else ''}")
    elif args.cmd == "check":
        slugs = [args.slug] if args.slug else list(T)
        good = all([contrast_report(s, T[s]) for s in slugs])
        sys.exit(0 if good else 1)
    elif args.cmd == "preview":
        unknown = [x for x in args.slugs if x not in T]
        if unknown: sys.exit(f"Unknown theme(s): {', '.join(unknown)}")
        preview(args.slugs, Path(args.out))
    else:
        apply(args.slug, args.dry_run)

if __name__ == "__main__":
    main()
