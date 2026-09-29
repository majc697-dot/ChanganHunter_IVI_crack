# -*- coding: utf-8 -*-
from loguru import logger as _l
_l.remove()
from androguard.core.dex import DEX

path = r"c:\Users\24920\Documents\trae_projects\MT8666\CA_Launcher.apk"
import zipfile, io
z = zipfile.ZipFile(path)
found = set()
for n in z.namelist():
    if n.endswith('.dex'):
        d = DEX(z.read(n))
        for c in d.get_classes():
            if c.get_name() == 'Lcom/autoai/project/home/R$drawable;':
                for f in c.get_fields():
                    nm = f.get_name()
                    if any(k in nm.lower() for k in ('music','icon_app','media','kugou','kuwo','netease')):
                        found.add(nm)
for x in sorted(found):
    print(x)
