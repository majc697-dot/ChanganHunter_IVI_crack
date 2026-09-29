# -*- coding: utf-8 -*-
from loguru import logger as _l
_l.remove()
from androguard.core.apk import APK
a = APK(r"c:\Users\24920\Documents\trae_projects\MT8666\netease_iot.apk")
print("package:", a.get_package(), "version:", a.get_androidversion_name())
print("sharedUserId:", a.get_attribute_value('manifest','sharedUserId'))
print("\n===== services with intent filters =====")
for s in a.get_services():
    name = s if isinstance(s,str) else s.get('name')
    filters = a.get_intent_filters('service', name)
    acts = filters.get('action',[]) if filters else []
    if acts or any(k in (name or '') for k in ('autoai','adapter','Auto','Media','Play')):
        print(name, '=>', acts)
print("\n===== receivers mentioning media/autoai/auto =====")
for r in a.get_receivers():
    name = r if isinstance(r,str) else r.get('name')
    filters = a.get_intent_filters('receiver', name)
    acts = filters.get('action',[]) if filters else []
    joined = ' '.join(acts)
    if any(k in (name or '')+joined for k in ('MEDIA','media','autoai','AutoSdk','adapter','easymedia','EasyMedia')):
        print(name, '=>', acts)
