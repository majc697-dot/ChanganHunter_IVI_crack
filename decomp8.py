# -*- coding: utf-8 -*-
import io
from loguru import logger as _l
_l.remove()
from androguard.misc import AnalyzeAPK

APK_PATH = r"c:\Users\24920\Documents\trae_projects\MT8666\P201_COMMON_APP.apk"
OUT = r"c:\Users\24920\Documents\trae_projects\MT8666\decomp_mainservice.txt"

WANT = [
    'Lcom/autoai/common/adapter/MainService;',
    'Lcom/autoai/common/adapter/IAdapterService;',
]
print("loading...")
a, d_list, dx = AnalyzeAPK(APK_PATH)
buf = io.StringIO()
# also dump service decl from manifest
import androguard.core.apk as _apk
buf.write(str(a.get_android_manifest_axml().get_xml().decode('utf-8','replace'))[:200000])
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
