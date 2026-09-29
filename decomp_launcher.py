# -*- coding: utf-8 -*-
import sys, io
from androguard.misc import AnalyzeAPK

APK_PATH = r"c:\Users\24920\Documents\trae_projects\MT8666\CA_Launcher.apk"
OUT = r"c:\Users\24920\Documents\trae_projects\MT8666\decomp_launcher.txt"

print("loading apk...")
a, d_list, dx = AnalyzeAPK(APK_PATH)
print("analyzing...")

WANT = [
    'Lcom/autoai/project/home/LauncherModel;',
    'Lcom/autoai/project/home/LauncherActivity;',
]

buf = io.StringIO()
for cn in WANT:
    c = dx.classes.get(cn)
    if not c:
        buf.write(f"\n##### NOT FOUND {cn}\n")
        continue
    vm = c.get_vm_class()
    buf.write(f"\n{'='*100}\nCLASS {cn}\n{'='*100}\n")
    try:
        src = vm.get_source()
        buf.write(src)
    except Exception as e:
        buf.write(f"[source error: {e}]\n")

with open(OUT, 'w', encoding='utf-8') as f:
    f.write(buf.getvalue())
print("written", OUT, len(buf.getvalue()))
