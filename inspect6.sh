#!/system/bin/sh
echo "########## autoai/native services in service list ##########"
service list | grep -iE 'autoai|music|media|hard|key|can|mcu|vehicle|hades|nfore|changan|p201'
echo
echo "########## running autoai processes ##########"
ps -A | grep -iE 'autoai|nfore|hades|kugou|netease|tianqin|changan'
echo
echo "########## KUGOU services ##########"
dumpsys activity services com.kugou.android.auto 2>/dev/null | grep -E 'ServiceRecord|intent|app=' | head -30
echo
echo "########## NETEASE services ##########"
dumpsys activity services com.netease.cloudmusic.iot 2>/dev/null | grep -E 'ServiceRecord|intent|app=' | head -30
echo
echo "########## common.app media-related services ##########"
dumpsys activity services com.autoai.common.app 2>/dev/null | grep -E 'ServiceRecord' | head -40
echo
echo "########## all packages containing 'hardkey' receiver scan via dumpsys ##########"
dumpsys package | grep -B5 -iE 'hardkey|hard_key|HardKey' | grep -iE 'package:|Action:' | head -40
