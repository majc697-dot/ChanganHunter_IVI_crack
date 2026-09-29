# -*- coding: utf-8 -*-
from loguru import logger as _l
_l.remove()
from androguard.misc import AnalyzeAPK
APK_PATH = r"c:\Users\24920\Documents\trae_projects\MT8666\P201_COMMON_APP.apk"
a, d_list, dx = AnalyzeAPK(APK_PATH)
for t in ['onFocusChanged','onPlayStateChanged','onPlayModeChanged']:
    print(f"\n===== xref callers of {t} =====")
    for meth in dx.find_methods(methodname=t):
        for tup in meth.get_xref_from():
            cls = tup[0].name if hasattr(tup[0],'name') else str(tup[0])
            m2 = tup[1]
            print(cls, '->', getattr(m2,'name',m2))
