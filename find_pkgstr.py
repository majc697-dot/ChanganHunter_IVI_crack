# -*- coding: utf-8 -*-
from loguru import logger as _l
_l.remove()
from androguard.misc import AnalyzeAPK
a, d_list, dx = AnalyzeAPK(r"c:\Users\24920\Documents\trae_projects\MT8666\CA_Launcher.apk")
for s in dx.get_strings():
    if s.get_value() == 'android.intent.action.PACKAGE_ADDED':
        for tup in s.get_xref_from():
            print(tup[0], getattr(tup[1],'name',tup[1]))
