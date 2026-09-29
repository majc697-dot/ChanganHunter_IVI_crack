# -*- coding: utf-8 -*-
from loguru import logger as _l
_l.remove()
from androguard.misc import AnalyzeAPK
a, d_list, dx = AnalyzeAPK(r"c:\Users\24920\Documents\trae_projects\MT8666\P201_COMMON_APP.apk")
# who calls SourceManager.setCurrentSource
cls = dx.classes.get('Lcom/autoai/common/center/manager/SourceManager;')
for m in cls.get_methods():
    if m.name == 'setCurrentSource':
        for tup in m.get_xref_from():
            print("CALLER:", tup[0].name, '->', tup[1].name, tup[1].descriptor)
# search broadcast actions related to source in all classes
import re
hits = set()
for d in d_list:
    for s in d.get_strings():
        if re.search(r'source|SOURCE', s) and ('action' in s.lower() or 'intent' in s.lower() or s.startswith('com.autoai')) and len(s) < 90:
            hits.add(s)
for h in sorted(hits):
    print("STR:", h)
