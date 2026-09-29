# -*- coding: utf-8 -*-
import io
from loguru import logger as _l
_l.remove()
from androguard.misc import AnalyzeAPK
a, d_list, dx = AnalyzeAPK(r"c:\Users\24920\Documents\trae_projects\MT8666\CA_Launcher.apk")
names = [n for n in dx.classes.keys() if 'kugou' in n.lower() and ('Proxy' in n or 'Result' in n)]
print(names)
buf = io.StringIO()
for cn in names:
    if 'KgAutoProxy' in cn or 'VoidResult' in cn or 'BoolResult' in cn or 'BooleanResult' in cn:
        c = dx.classes.get(cn)
        if c:
            buf.write("===== %s =====\n" % cn)
            buf.write(c.get_vm_class().get_source()[:9000])
            buf.write("\n\n")
open(r"c:\Users\24920\Documents\trae_projects\MT8666\decomp_kgproxy.txt",'w',encoding='utf-8').write(buf.getvalue())
print(len(buf.getvalue()))
