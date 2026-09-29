# -*- coding: utf-8 -*-
import io
from loguru import logger as _l
_l.remove()
from androguard.misc import AnalyzeAPK
JAR = r"c:\Users\24920\Documents\trae_projects\MT8666\RpcManager.jar"
a, d_list, dx = AnalyzeAPK(JAR)
names = sorted(c.name for c in dx.get_classes())
print("=== key-related classes ===")
for n in names:
    if 'Key' in n or 'HK' in n or 'Hard' in n:
        print(n)
for cn in ['Lcom/xauto/rpc/NativeRpcComm;']:
    c = dx.classes.get(cn)
    print("\n===== "+cn+" =====")
    print(c.get_vm_class().get_source()[:12000] if c else "NOT FOUND")
