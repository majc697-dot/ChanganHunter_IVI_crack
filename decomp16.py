# -*- coding: utf-8 -*-
import io
from loguru import logger as _l
_l.remove()
from androguard.misc import AnalyzeAPK

APK_PATH = r"c:\Users\24920\Documents\trae_projects\MT8666\CA_Launcher.apk"
OUT = r"c:\Users\24920\Documents\trae_projects\MT8666\decomp_scanner.txt"
WANT = [
    'Lcom/autoai/project/home/LauncherApplication;',
    'Lcom/autoai/project/home/util/ImageUtils;',
]
print("loading...")
a, d_list, dx = AnalyzeAPK(APK_PATH)
buf = io.StringIO()
for cn in WANT:
    c = dx.classes.get(cn)
    buf.write(f"\n===== {cn} =====\n")
    if not c:
        buf.write("NOT FOUND\n"); continue
    buf.write(c.get_vm_class().get_source()[:24000])
open(OUT,'w',encoding='utf-8').write(buf.getvalue())
print("written", len(buf.getvalue()))
