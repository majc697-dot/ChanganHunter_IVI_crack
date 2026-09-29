# -*- coding: utf-8 -*-
import io
from loguru import logger as _l
_l.remove()
from androguard.misc import AnalyzeAPK
a, d_list, dx = AnalyzeAPK(r"c:\Users\24920\Documents\trae_projects\MT8666\P201_COMMON_APP.apk")
buf = io.StringIO()
for cn in ['Lcom/autoai/common/center/manager/FocusManager$1;','Lcom/autoai/common/center/manager/SystemStateManager;']:
    c = dx.classes.get(cn)
    if not c:
        buf.write("NF %s\n" % cn); continue
    buf.write("===== %s =====\n" % cn)
    buf.write(c.get_vm_class().get_source()[:18000])
    buf.write("\n\n")
open(r"c:\Users\24920\Documents\trae_projects\MT8666\decomp_focus.txt",'w',encoding='utf-8').write(buf.getvalue())
print(len(buf.getvalue()))
