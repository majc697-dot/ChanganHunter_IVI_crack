# -*- coding: utf-8 -*-
import zipfile
APK = r"c:\Users\24920\Documents\trae_projects\MT8666\CA_Launcher.apk"
z = zipfile.ZipFile(APK)
for n in z.namelist():
    if n.startswith('res/xml') or 'workspace' in n.lower():
        print(n, z.getinfo(n).file_size)
