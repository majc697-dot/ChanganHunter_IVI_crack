# -*- coding: utf-8 -*-
from loguru import logger as _l
_l.remove()
from androguard.core.apk import APK
A = '{http://schemas.android.com/apk/res/android}name'
E = '{http://schemas.android.com/apk/res/android}exported'
a = APK(r"c:\Users\24920\Documents\trae_projects\MT8666\P201_COMMON_APP.apk")
root = a.get_android_manifest_xml()
app = root.find('application')
for tag in ('activity','activity-alias'):
    for el in app.findall(tag):
        name = el.get(A); exp = el.get(E)
        acts = [x.get(A) for f in el.findall('intent-filter') for x in f.findall('action')]
        if exp == 'true' or acts:
            print(('%-6s' % tag), name, '| exp=%s' % exp, '|', ','.join(acts))
