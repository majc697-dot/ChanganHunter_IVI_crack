# -*- coding: utf-8 -*-
import io
from loguru import logger as _l
_l.remove()
from androguard.misc import AnalyzeAPK

APK_PATH = r"c:\Users\24920\Documents\trae_projects\MT8666\P201_COMMON_APP.apk"
OUT = r"c:\Users\24920\Documents\trae_projects\MT8666\decomp_models.txt"

WANT = [
    'Lcom/autoai/common/adapter/MainService$1;',
    'Lcom/autoai/common/adapter/model/ModelManager;',
    'Lcom/autoai/common/adapter/model/media/EasyMediaModel;',
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
