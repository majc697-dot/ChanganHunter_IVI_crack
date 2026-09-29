# -*- coding: utf-8 -*-
from loguru import logger as _l
_l.remove()
from androguard.core.apk import APK
a = APK(r"c:\Users\24920\Documents\trae_projects\MT8666\CA_Launcher.apk")
# strings.xml names via resource table: drawable public names
names = set()
for pkg in a.get_android_resources().get_packages_names():
    arsc = a.get_android_resources()
for pkg in arsc.get_packages():
    for k in pkg.get_resolved_strings():
        pass
# iterate resource configs
for pkg in arsc.get_packages():
    for typ in pkg.get_types():
        if typ.get_type() in ('drawable','mipmap'):
            for entry in typ:
                if entry.is_overlayable():
                    pass
                try:
                    n = entry.get_key_name()
                    if n and ('music' in n.lower() or 'icon_app' in n.lower() or 'netease' in n.lower() or 'wangyi' in n.lower() or 'kugou' in n.lower() or 'kuwo' in n.lower() or 'media' in n.lower()):
                        names.add("%s/%s" % (typ.get_type(), n))
                except Exception:
                    pass
for n in sorted(names):
    print(n)
