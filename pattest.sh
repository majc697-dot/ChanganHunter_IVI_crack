#!/system/bin/sh
line='D/Launcher-library-common(12153): [ (CommonService.java:548)#OnHKChange] HK onHKChange keyCode : 3 keyState : 0 source 0'
case "$line" in
    *"#OnHKChange] HK onHKChange"*) echo MATCH ;;
    *) echo NOMATCH ;;
esac
