# -*- coding: utf-8 -*-
import io, re
from loguru import logger as _l
_l.remove()
from androguard.misc import AnalyzeAPK
a, d_list, dx = AnalyzeAPK(r"c:\Users\24920\Documents\trae_projects\MT8666\CA_Launcher.apk")
buf = io.StringIO()
targets = {
 'Lcom/autoai/project/common/hk/HKStateControl;': None,
 'Lcom/autoai/project/common/adapter/CommonManager;': ['next','pre','play','pause','playPause','getCurrentSource','isRealPlaying'],
}
for cn, methods in targets.items():
    c = dx.classes.get(cn)
    if not c:
        buf.write("NF %s\n" % cn); continue
    src = c.get_vm_class().get_source()
    if methods is None:
        buf.write("===== %s =====\n%s\n" % (cn, src[:16000]))
    else:
        for mth in methods:
            for m in re.finditer(r'    public [^\n]*\b%s\([^\{]*\{.*?\n    \}' % re.escape(mth), src, re.S):
                buf.write("===== %s.%s =====\n%s\n\n" % (cn, mth, m.group(0)))
open(r"c:\Users\24920\Documents\trae_projects\MT8666\decomp_routing.txt",'w',encoding='utf-8').write(buf.getvalue())
print(len(buf.getvalue()))
