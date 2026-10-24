"""Build coordinated light terminal themes from OKLCH semantic tokens.

No application settings are changed by this builder.
"""
from pathlib import Path
import math
import json

ROOT = Path(__file__).resolve().parent
THEMES = ROOT.parent / '.config/ghostty/themes'

def rgb(l, c, h):
    a, b = c*math.cos(math.radians(h)), c*math.sin(math.radians(h))
    ll=(l+.3963377774*a+.2158037573*b)**3
    mm=(l-.1055613458*a-.0638541728*b)**3
    ss=(l-.0894841775*a-1.291485548*b)**3
    return (4.0767416621*ll-3.3077115913*mm+.2309699292*ss,
            -1.2684380046*ll+2.6097574011*mm-.3413193965*ss,
            -.0041960863*ll-.7034186147*mm+1.707614701*ss)

def color(l,c,h):
    # Reduce chroma while preserving hue/lightness to stay in sRGB gamut.
    while True:
        v=rgb(l,c,h)
        if min(v)>=0 and max(v)<=1:break
        c*=.95
    def srgb(x):return 12.92*x if x<=.0031308 else 1.055*x**(1/2.4)-.055
    return '#'+''.join(f'{round(srgb(x)*255):02x}' for x in v)

def luminance(s):
    v=[int(s[i:i+2],16)/255 for i in (1,3,5)]
    v=[x/12.92 if x<=.04045 else ((x+.055)/1.055)**2.4 for x in v]
    return sum(a*b for a,b in zip(v,(.2126,.7152,.0722)))

def contrast(a,b):
    x,y=sorted((luminance(a),luminance(b)))
    return (y+.05)/(x+.05)

def make(name,hue,chroma):
    t={
      'canvas':color(.962,chroma,hue),
      'surface':color(.925,chroma*1.2,hue),
      'selection':color(.87,chroma*1.6,hue),
      'text':color(.30,.025,hue),
      'secondary':color(.43,.027,hue),
      'muted':color(.46,.025,hue),
      'border':color(.62,.03,hue),
      'blue':color(.44,.09,235),
      'green':color(.44,.085,145),
      'amber':color(.44,.085,75),
      'red':color(.44,.12,30),
      'purple':color(.44,.08,320),
      'teal':color(.44,.07,185),
      'accent':color(.44,.09,55),
      'addedBg':color(.925,.035,145),
      'removedBg':color(.925,.035,30),
      'addedWord':color(.86,.05,145),
      'removedWord':color(.86,.05,30),
    }
    # Validate actual rounded sRGB values, not just OKLCH inputs.
    checks=[]
    ink=['text','secondary','muted','blue','green','amber','red','purple','teal','accent']
    for fg in ink:
      for bg in ['canvas','surface','selection','addedBg','removedBg','addedWord','removedWord']:
        cr=contrast(t[fg],t[bg]);checks.append(dict(fg=fg,bg=bg,ratio=round(cr,3)))
        assert cr>=4.5,(name,fg,bg,cr)
    assert contrast(t['border'],t['canvas'])>=3
    palette=[t[k] for k in ['text','red','green','amber','blue','purple','teal','surface','muted','red','green','amber','blue','purple','teal','canvas']]
    lines=[f'# {name} / generated from design-system/build.py',
      '# Background L=.962; ink L=.30/.43/.46; accents L=.44.',
      f'background = {t["canvas"]}',f'foreground = {t["text"]}',
      f'selection-background = {t["selection"]}',f'selection-foreground = {t["text"]}',
      f'cursor-color = {t["accent"]}',f'cursor-text = {t["canvas"]}',
      f'split-divider-color = {t["border"]}',
      '# Contrast is checked offline; avoid glass/min-contrast interaction in 1.3.1.',
      'minimum-contrast = 1','faint-opacity = 1']
    lines += [f'palette = {i}={v}' for i,v in enumerate(palette)]
    (THEMES/name).write_text('\n'.join(lines)+'\n')
    o={
      'text':t['text'],'inverseText':t['canvas'],'inactive':t['muted'],'subtle':t['muted'],
      'claude':t['accent'],'claudeShimmer':t['amber'],
      'success':t['green'],'error':t['red'],'warning':t['amber'],'warningShimmer':t['amber'],
      'merged':t['purple'],'permission':t['blue'],'permissionShimmer':t['blue'],
      'remember':t['purple'],'suggestion':t['blue'],
      'promptBorder':t['border'],'promptBorderShimmer':t['blue'],
      'planMode':t['blue'],'autoAccept':t['green'],'bashBorder':t['teal'],
      'ide':t['blue'],'fastMode':t['accent'],'fastModeShimmer':t['amber'],
      'inactiveShimmer':t['secondary'],
      'diffAdded':t['addedBg'],'diffRemoved':t['removedBg'],
      'diffAddedDimmed':t['addedBg'],'diffRemovedDimmed':t['removedBg'],
      'diffAddedWord':t['addedWord'],'diffRemovedWord':t['removedWord'],
      'userMessageBackground':t['surface'],'userMessageBackgroundHover':t['selection'],
      'bashMessageBackgroundColor':t['surface'],'memoryBackgroundColor':t['surface'],
      'selectionBg':t['selection'],'composerSidebarBackground':t['surface'],
      'rate_limit_fill':t['blue'],'rate_limit_empty':t['border'],
      'briefLabelYou':t['blue'],'briefLabelClaude':t['accent'],
    }
    slug=name.lower().replace(' ','-')
    (ROOT/(slug+'.claude.json')).write_text(json.dumps(dict(name=name,base='light',overrides=o),indent=2)+'\n')
    return dict(name=name,tokens=t,checks=checks,minContrast=min(x['ratio'] for x in checks),borderContrast=round(contrast(t['border'],t['canvas']),3))

if __name__=='__main__':
    results=[make('Slow Sky',230,.021),make('Matcha Milk',125,.032)]
    (ROOT/'tokens-and-contrast.json').write_text(json.dumps(results,indent=2)+'\n')
    for r in results:print(r['name'], 'min text contrast',r['minContrast'],'border',r['borderContrast'])
