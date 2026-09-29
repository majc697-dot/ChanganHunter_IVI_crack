# -*- coding: utf-8 -*-
import io
from loguru import logger as _l
_l.remove()
from androguard.misc import AnalyzeAPK

APK_PATH = r"c:\Users\24920\Documents\trae_projects\MT8666\CA_Launcher.apk"
OUT = r"c:\Users\24920\Documents\trae_projects\MT8666\decomp_rpcbase.txt"
WANT = ['Lcom/autoai/project/rpc/RpcManager;']
print("loading...")
a, d_list, dx = AnalyzeAPK(APK_PATH)
buf = io.StringIO()
for cn in WANT:
    c = dx.classes.get(cn)
    if not c:
        print("NOT FOUND"); continue
    buf.write(c.get_vm_class().get_source()[:30000])
open(OUT,'w',encoding='utf-8').write(buf.getvalue())
print("written", len(buf.getvalue()))
