# -*- coding: utf-8 -*-
import io, re
from loguru import logger as _l
_l.remove()
from androguard.misc import AnalyzeAPK
a, d_list, dx = AnalyzeAPK(r"c:\Users\24920\Documents\trae_projects\MT8666\CA_Launcher.apk")
c = dx.classes.get('Lcom/kugou/auto/proxy/KgAutoProxy;')
src = c.get_vm_class().get_source()
open(r"c:\Users\24920\Documents\trae_projects\MT8666\decomp_kgproxy_full.txt",'w',encoding='utf-8').write(src)
print(len(src))
