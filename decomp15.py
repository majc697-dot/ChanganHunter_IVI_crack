# -*- coding: utf-8 -*-
import io
from loguru import logger as _l
_l.remove()
from androguard.misc import AnalyzeAPK

APK_PATH = r"c:\Users\24920\Documents\trae_projects\MT8666\CA_Launcher.apk"
OUT = r"c:\Users\24920\Documents\trae_projects\MT8666\decomp_native.txt"
WANT = [
    'Lcom/xauto/rpc/NativeRpcComm;',
    'Lcom/autoai/project/rpc/manager/key/RpcKeyConstants;',
]
print("loading...")
a, d_list, dx = AnalyzeAPK(APK_PATH)
buf = io.StringIO()
for cn in WANT:
    c = dx.classes.get(cn)
    buf.write(f"\n===== {cn} =====\n")
    if not c:
        buf.write("NOT FOUND\n"); continue
    buf.write(c.get_vm_class().get_source()[:20000])
open(OUT,'w',encoding='utf-8').write(buf.getvalue())
print("written", len(buf.getvalue()))
import zipfile
z=zipfile.ZipFile(APK)
libs=[n for n in z.namelist() if n.endswith('.so') and ('rpc' in n.lower() or 'xauto' in n.lower())]
print("LIBS:", libs)
