import json, sys
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

ok=True
for slug,t in T.items():
    g,pal=ghostty(t); open(f"{slug}.ghostty","w").write(g)
    json.dump(claude(t),open(f"{slug}.json","w"),indent=2)
    print(f"== {t['name']}")
    for fg in ["text","muted","matcha","sky","hojicha","red","amber","plum","teal"]:
        for bgk in ["bg","surface","addbg","rmbg","selection"]:
            r=cr(t[fg],t[bgk]); need=4.5
            flag="" if r>=need else "  <-- LOW"
            if flag: ok=False
            if bgk=="bg" or flag: print(f"  {fg:8} on {bgk:9} {r:5.2f}{flag}")
    print(f"  faint    on bg        {cr(t['faint'],t['bg']):5.2f} (hints, >=3 target)")
    print(f"  ansi8    on bg        {cr(pal[8],t['bg']):5.2f}")
    print(f"  ansi7    on bg        {cr(pal[7],t['bg']):5.2f}")
    print(f"  border   on bg        {cr(t['border'],t['bg']):5.2f} (non-text)")
print("ALL TEXT >=4.5" if ok else "SOME LOW")
