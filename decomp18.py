# -*- coding: utf-8 -*-
import io
from loguru import logger as _l
_l.remove()
from androguard.misc import AnalyzeAPK

APK_PATH = r"c:\Users\24920\Documents\trae_projects\MT8666\CA_Launcher.apk"
OUT = r"c:\Users\24920\Documents\trae_projects\MT8666\decomp_exec.txt"
WANT = [
 'Lcom/autoai/project/common/hk/cmd/LocalCmdExecutor;',
 'Lcom/autoai/project/common/hk/cmd/MediaCmdExecutor;',
 'Lcom/autoai/project/common/hk/cmd/BroadCastCmdExecutor;',
 'Lcom/autoai/project/common/hk/cmd/CmdBaseExecutor;',
 'Lcom/autoai/project/common/hk/cmd/PhoneCmdExecutor;',
]
print("loading...")
a, d_list, dx = AnalyzeAPK(APK_PATH)
buf = io.StringIO()
for cn in WANT:
    c = dx.classes.get(cn)
    if not c:
        buf.write("\nNOT FOUND %s\n" % cn)
        continue
    buf.write("\n=== %s ===\n" % cn)
    buf.write(c.get_vm_class().get_source()[:14000])
open(OUT,'w',encoding='utf-8').write(buf.getvalue())
print("written", len(buf.getvalue()))
