# -*- coding: utf-8 -*-
import io, re
from loguru import logger as _l
_l.remove()
from androguard.misc import AnalyzeAPK
a, d_list, dx = AnalyzeAPK(r"c:\Users\24920\Documents\trae_projects\MT8666\CA_Launcher.apk")
buf = io.StringIO()
c = dx.classes.get('Lcom/autoai/project/home/model/CommonRepository;')
src = c.get_vm_class().get_source()
for m in re.finditer(r'    public [^\n]*start\w*App\([^\{]*\{.*?\n    \}', src, re.S):
    buf.write(m.group(0)+"\n\n")
open(r"c:\Users\24920\Documents\trae_projects\MT8666\decomp_repo.txt",'w',encoding='utf-8').write(buf.getvalue() or src[:8000])
print(len(buf.getvalue()))
