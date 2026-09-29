# -*- coding: utf-8 -*-
import io
from loguru import logger as _l
_l.remove()
from androguard.misc import AnalyzeAPK
a, d_list, dx = AnalyzeAPK(r"c:\Users\24920\Documents\trae_projects\MT8666\CA_Launcher.apk")
buf = io.StringIO()
# find Repository class and startKWApp/startXMApp callers
for cname in list(dx.classes.keys()):
    if 'Repository' in cname:
        print("REPO?", cname)
for cn in ['Lcom/autoai/project/home/repository/LauncherRepository;','Lcom/autoai/project/home/LauncherActivity$Repository;']:
    c = dx.classes.get(cn)
    if c:
        src = c.get_vm_class().get_source()
        import re
        for m in re.finditer(r'    public [^\n]*start(KW|XM)App\([^\{]*\{.*?\n    \}', src, re.S):
            buf.write(m.group(0)+"\n\n")
open(r"c:\Users\24920\Documents\trae_projects\MT8666\decomp_repo.txt",'w',encoding='utf-8').write(buf.getvalue())
print(len(buf.getvalue()))
