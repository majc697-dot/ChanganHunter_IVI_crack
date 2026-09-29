# -*- coding: utf-8 -*-
# find which classes call IEasyMediaNotifier methods and setMediaSource-like methods
from loguru import logger as _l
_l.remove()
from androguard.misc import AnalyzeAPK
APK_PATH = r"c:\Users\24920\Documents\trae_projects\MT8666\P201_COMMON_APP.apk"
a, d_list, dx = AnalyzeAPK(APK_PATH)
targets = ['onFocusChanged','onPlayStateChanged','onSourceChanged','onPlayModeChanged','onUsbStateChanged']
for t in targets:
    print(f"\n===== callers of {t} =====")
    for meth in dx.find_methods(methodname=t):
        try:
            for tup in meth.get_xref_from():
                print(tup[1], '->', tup[2].name, tup[2].descriptor)
        except Exception as e:
            print('err', e)
