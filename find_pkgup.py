# -*- coding: utf-8 -*-
from loguru import logger as _l
_l.remove()
from androguard.misc import AnalyzeAPK
a, d_list, dx = AnalyzeAPK(r"c:\Users\24920\Documents\trae_projects\MT8666\CA_Launcher.apk")
for cn in ['Lcom/autoai/project/home/LauncherModel$PackageUpdatedTask;']:
    c = dx.classes.get(cn)
    print("class:", cn, "found:", bool(c))
    if c:
        vm = c.get_vm_class()
        for m in vm.get_methods():
            if m.name == '<init>':
                ana = dx.get_method(m)
                print("init xref_from:", ana.get_xref_from())
# search any string ref to package broadcasts
for s in dx.get_strings():
    v = s.get_value()
    if 'PACKAGE' in v and ('ADDED' in v or 'REPLACED' in v or 'REMOVED' in v or 'package' in v):
        print("STR:", v)
