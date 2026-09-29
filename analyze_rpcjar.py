# -*- coding: utf-8 -*-
import io
from loguru import logger as _l
_l.remove()
from androguard.misc import AnalyzeAPK
JAR = r"c:\Users\24920\Documents\trae_projects\MT8666\RpcManager.jar"
a, d_list, dx = AnalyzeAPK(JAR)
names = sorted(c.name for c in dx.get_classes())
print(len(names), "classes")
for n in names:
    print(n)
