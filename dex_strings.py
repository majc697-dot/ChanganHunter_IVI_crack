# -*- coding: utf-8 -*-
import zipfile, re, struct, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

APK = r"c:\Users\24920\Documents\trae_projects\MT8666\CA_Launcher.apk"
z = zipfile.ZipFile(APK)

def read_uleb(data, off):
    result = 0; shift = 0
    while True:
        b = data[off]; off += 1
        result |= (b & 0x7f) << shift
        if (b & 0x80) == 0: break
        shift += 7
    return result, off

def dex_strings(data):
    # header: string_ids_size @0x38, string_ids_off @0x3c
    string_ids_size = struct.unpack_from('<I', data, 0x38)[0]
    string_ids_off  = struct.unpack_from('<I', data, 0x3c)[0]
    out = []
    for i in range(string_ids_size):
        so = struct.unpack_from('<I', data, string_ids_off + i*4)[0]
        _, p = read_uleb(data, so)
        end = data.index(b'\x00', p)
        try:
            out.append(data[p:end].decode('utf-8','replace'))
        except Exception:
            pass
    return out

def dex_types(data):
    type_ids_size = struct.unpack_from('<I', data, 0x40)[0]
    type_ids_off  = struct.unpack_from('<I', data, 0x44)[0]
    strs = dex_strings(data)
    types=[]
    for i in range(type_ids_size):
        idx = struct.unpack_from('<I', data, type_ids_off + i*4)[0]
        if idx < len(strs): types.append(strs[idx])
    return strs, types

OUT = open(r"c:\Users\24920\Documents\trae_projects\MT8666\dex_out.txt", "w", encoding="utf-8")
def print(*a):
    OUT.write(' '.join(str(x) for x in a) + '\n')

TARGETS = ['classes3.dex','classes4.dex','classes5.dex','classes2.dex','classes28.dex','classes29.dex']
kw = re.compile(r'(?i)(allapp|applist|white_?list|black_?list|hideapp|hide_app|drawer|queryintent|category\.app|cn\.kuwo|kugou|netease|package_added|addworkspace|workspace|customcategory|appstore|install)')
appcls = re.compile(r'^L(com/(autoai|bon)|cn/)', )

for d in TARGETS:
    data = z.read(d)
    strs, types = dex_types(data)
    print(f"\n########## {d}: {len(strs)} strings, {len(types)} types ##########")
    # interesting class descriptors
    interesting_types = sorted({t for t in types if re.search(r'(?i)(allapp|applist|workspace|drawer|launcher|shortcut|widget)', t) and 'androidx' not in t and 'android/support' not in t and '/com/android/' not in t})
    print("---- interesting classes ----")
    for t in interesting_types[:60]:
        print(" ", t)
    print("---- interesting strings ----")
    seen=set()
    for s in strs:
        if len(s) < 4 or len(s) > 200: continue
        if kw.search(s) and s not in seen:
            seen.add(s)
    for s in sorted(seen)[:120]:
        print("  ", s)

print("\n########## assets/command_media.json ##########")
print(z.read('assets/command_media.json').decode('utf-8','replace'))
