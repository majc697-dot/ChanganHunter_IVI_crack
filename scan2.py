# -*- coding: utf-8 -*-
import zipfile, re, struct
APK = r"c:\Users\24920\Documents\trae_projects\MT8666\P201_COMMON_APP.apk"
z = zipfile.ZipFile(APK)
def read_uleb(data, off):
    result=0; shift=0
    while True:
        b=data[off]; off+=1; result|=(b&0x7f)<<shift
        if not b&0x80: break
        shift+=7
    return result,off
def dex_strings(data):
    n=struct.unpack_from('<I',data,0x38)[0]; o=struct.unpack_from('<I',data,0x3c)[0]
    out=[]
    for i in range(n):
        so=struct.unpack_from('<I',data,o+i*4)[0]
        _,p=read_uleb(data,so); e=data.index(b'\x00',p)
        out.append(data[p:e].decode('utf-8','replace'))
    return out
pat=re.compile(r'(?i)(netease|kwmusic|kugou|AutoSdk|music.*\.action|\.action\..*music|xauto.*music|MODULE_|source_|currentSource|switchSource|setSource)')
for d in ['classes.dex','classes2.dex','classes3.dex']:
    strs=dex_strings(z.read(d))
    hits=sorted({s for s in strs if 3<len(s)<160 and pat.search(s)})
    print(f"===== {d} =====")
    for s in hits: print(s)
