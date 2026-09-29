# -*- coding: utf-8 -*-
import io
from loguru import logger as _l
_l.remove()
from androguard.misc import AnalyzeAPK
a, d_list, dx = AnalyzeAPK(r"c:\Users\24920\Documents\trae_projects\MT8666\CA_Launcher.apk")
names = [n for n in dx.classes.keys() if 'MapManager' in n]
print(names)
buf = io.StringIO()
for cn in ['Lcom/autoai/project/common/map/MapManager;']:
    c = dx.classes.get(cn)
    if c:
        buf.write(c.get_vm_class().get_source()[:16000])
open(r"c:\Users\24920\Documents\trae_projects\MT8666\decomp_map.txt",'w',encoding='utf-8').write(buf.getvalue())
print(len(buf.getvalue()))
