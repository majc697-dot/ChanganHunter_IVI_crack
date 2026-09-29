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
data=z.read('classes.dex')
strs=dex_strings(data)
pat=re.compile(r'(?i)(netease|kuwo|kugou|autoai.*(music|action|service)|action\.(music|play|next|hard)|com\.autoai|xauto|\.service\.|AIDLRemote|bind|MODULE)')
seen=set()
for s in strs:
    if 4<len(s)<180 and pat.search(s) and s not in seen:
        seen.add(s); print(s)
