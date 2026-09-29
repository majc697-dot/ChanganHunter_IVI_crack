# -*- coding: utf-8 -*-
from loguru import logger as _l
_l.remove()
from androguard.core.apk import APK
import hashlib
for p in [r"c:\Users\24920\Documents\trae_projects\MT8666\CA_Launcher.apk",
          r"c:\Users\24920\Documents\trae_projects\MT8666\P201_COMMON_APP.apk"]:
    a = APK(p)
    print("="*70)
    print(p.split("\\")[-1])
    for c in a.get_certificates():
        print("subject:", c.subject.human_friendly)
        print("issuer :", c.issuer.human_friendly)
        print("serial :", hex(c.serial_number))
        print("not_before:", c.not_valid_before, "not_after:", c.not_valid_after)
        der = c.dump()
        print("sha256:", hashlib.sha256(der).hexdigest())
        print("md5   :", hashlib.md5(der).hexdigest())
