# -*- coding: utf-8 -*-
import zipfile, re, struct, sys

APK = r"c:\Users\24920\Documents\trae_projects\MT8666\P201_COMMON_APP.apk"
OUT = open(r"c:\Users\24920\Documents\trae_projects\MT8666\common_out.txt", "w", encoding="utf-8")
def w(*a): OUT.write(' '.join(str(x) for x in a) + '\n')
z = zipfile.ZipFile(APK)

def read_uleb(data, off):
    result = 0; shift = 0
    while True:
        b = data[off]; off += 1
        result |= (b & 0x7f) << shift
        if (b & 0x80) == 0: break
        shift += 7
    return result, off

def parse_dex(data):
    ssize = struct.unpack_from('<I', data, 0x38)[0]
    soff  = struct.unpack_from('<I', data, 0x3c)[0]
    strs=[]
    for i in range(ssize):
        so = struct.unpack_from('<I', data, soff + i*4)[0]
        _, p = read_uleb(data, so)
        end = data.index(b'\x00', p)
        strs.append(data[p:end].decode('utf-8','replace'))
    tsize = struct.unpack_from('<I', data, 0x40)[0]
    toff  = struct.unpack_from('<I', data, 0x44)[0]
    types=[]
    for i in range(tsize):
        idx = struct.unpack_from('<I', data, toff + i*4)[0]
        if idx < len(strs): types.append(strs[idx])
    return strs, types

names = z.namelist()
dex = sorted([n for n in names if re.fullmatch(r'classes\d*\.dex', n)])
w("DEX:", dex)

cls_re = re.compile(r'(?i)(adapter|music|hardkey|keyevent|media|steer|can|mcu)')
str_re = re.compile(r'(?i)(hardkey|hard_key|keycode|media_button|next|previous|playpause|kgauto|netease|kuwo|kugou|steer|sendbroadcast|android\.intent\.action\.MEDIA|adapter\.sdk|bindService|AutoSdkAIDL|MODULE_)')

for d in dex:
    data = z.read(d)
    strs, types = parse_dex(data)
    itypes = sorted({t for t in types if cls_re.search(t) and 'androidx' not in t and 'android/support' not in t and '/google/' not in t})
    istrs = sorted({s for s in strs if 4 < len(s) < 160 and str_re.search(s)})
    if not itypes and not istrs: continue
    w(f"\n########## {d} ##########")
    w("---- classes ----")
    for t in itypes[:120]: w(" ", t)
    w("---- strings ----")
    for s in istrs[:200]: w("  ", s)
OUT.close()
print("done")
