# -*- coding: utf-8 -*-
import zipfile, re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

APK = r"c:\Users\24920\Documents\trae_projects\MT8666\CA_Launcher.apk"
z = zipfile.ZipFile(APK)

names = z.namelist()
dex = [n for n in names if n.endswith('.dex')]
print("DEX FILES:", dex)

# interesting non-code entries
print("\n==== assets / config-like files ====")
for n in names:
    low = n.lower()
    if (low.startswith('assets/') or low.startswith('res/raw') or
        re.search(r'(app|white|black|config|launcher|list).*\.(xml|json|txt|db|properties)$', low)):
        if low.endswith(('.png','.jpg','.webp','.ttf','.otf','.so')):
            continue
        print(n, z.getinfo(n).file_size)

# strings to locate inside dex
needles = [
    b'android.intent.category.LAUNCHER',
    b'queryIntentActivities',
    b'PACKAGE_ADDED',
    b'PACKAGE_REPLACED',
    b'allapp', b'AllApp', b'applist', b'AppList', b'app_list',
    b'whitelist', b'whiteList', b'blacklist', b'hideApp', b'hidden',
    b'getInstalledPackages',
    b'getInstalledApplications',
    b'com.autoai',
    b'LAUNCHER_APP', b'category.APP',
    b'appDrawer', b'AppDrawer', b'drawer',
    b'addWorkspace', b'addShortcut',
    b'cn.kuwo', b'kugou', b'netease',
]

def scan(data, tag):
    found = {}
    for nd in needles:
        idxs = [m.start() for m in re.finditer(re.escape(nd), data)]
        if idxs:
            found[nd.decode('utf-8','replace')] = len(idxs)
    if found:
        print(f"\n==== hits in {tag} ====")
        for k,v in found.items():
            print(f"  {k}: {v}")

for d in dex:
    data = z.read(d)
    scan(data, d)

# dump readable strings context around interesting keys in classes.dex
print("\n==== contextual strings (first dex with LAUNCHER) ====")
for d in dex:
    data = z.read(d)
    if b'android.intent.category.LAUNCHER' in data or b'queryIntentActivities' in data:
        # extract printable ascii strings >=6 chars, filter relevant
        strs = re.findall(rb'[\x20-\x7e]{6,}', data)
        kws = re.compile(r'(?i)(launcher|queryintent|package_added|allapp|applist|whitelist|blacklist|hide|drawer|getinstalled|category|workspace|shortcut)')
        seen=set()
        out=[]
        for s in strs:
            t=s.decode()
            if kws.search(t) and t not in seen:
                seen.add(t); out.append(t)
        for t in out[:150]:
            print(t)
        break
