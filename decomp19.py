# -*- coding: utf-8 -*-
import io
from loguru import logger as _l
_l.remove()
from androguard.misc import AnalyzeAPK
a, d_list, dx = AnalyzeAPK(r"c:\Users\24920\Documents\trae_projects\MT8666\CA_Launcher.apk")
buf = io.StringIO()
for cn in ['Lcom/autoai/project/home/util/HomeUtils;']:
    c = dx.classes.get(cn)
    src = c.get_vm_class().get_source()
    # only startCommonApp / startInstalledApp methods
    import re
    for m in re.finditer(r'    public static [^\n]*start(?:Common|Installed)App\([^\{]*\{.*?\n    \}', src, re.S):
        buf.write(m.group(0)+"\n\n")
open(r"c:\Users\24920\Documents\trae_projects\MT8666\decomp_homeutils.txt",'w',encoding='utf-8').write(buf.getvalue())
print(len(buf.getvalue()))
