# -*- coding: utf-8 -*-
import io
from loguru import logger as _l
_l.remove()
from androguard.misc import AnalyzeAPK

APK_PATH = r"c:\Users\24920\Documents\trae_projects\MT8666\CA_Launcher.apk"
OUT = r"c:\Users\24920\Documents\trae_projects\MT8666\decomp_more.txt"

WANT = [
    'Lcom/autoai/project/common/CommonService$3;',
    'Lcom/autoai/project/common/hk/HKManager;',
    'Lcom/autoai/project/common/adapter/CommonManager;',
    'Lcom/autoai/project/home/util/XMLParse;',
    'Lcom/autoai/project/home/db/DatabaseHelper;',
    'Lcom/autoai/project/common/rpc/RpcContext;',
]

print("loading...")
a, d_list, dx = AnalyzeAPK(APK_PATH)
buf = io.StringIO()
for cn in WANT:
    c = dx.classes.get(cn)
    buf.write(f"\n{'='*100}\nCLASS {cn}\n{'='*100}\n")
    if not c:
        buf.write("NOT FOUND\n"); continue
    try:
        buf.write(c.get_vm_class().get_source())
    except Exception as e:
        buf.write(f"[err {e}]\n")
open(OUT,'w',encoding='utf-8').write(buf.getvalue())
print("written", len(buf.getvalue()))

# search any class referencing engineer_appStore / getShortcutInfo(Context) callers
print("\n== xrefs getShortcutInfo ==")
for m in dx.find_methods(methodname='getShortcutInfo'):
    for ref in m.get_xref_from():
        print(m.name, '<-', ref[0].name, ref[1].name)
