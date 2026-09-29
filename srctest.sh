#!/system/bin/sh
# kill kugou so it cannot grab focus; then make netease play; observe source mapping
am force-stop com.kugou.android.auto
sleep 1
logcat -c -b all
# launch netease and play
am start -n com.netease.cloudmusic.iot/.app.LoadingActivity >/dev/null 2>&1
sleep 6
input keyevent 126
sleep 6
echo "===== focus/source related log ====="
logcat -d -b all -v threadtime | grep -iE 'FocusManager|SourceManager|CenterManager|onSourceChanged|post .*source|netease|bindService|Failed binding|Unable to bind|NetEaseMusic|MODULE_' | grep -viE 'httpdns|ExtensionLog|MediaSessionService|MediaButtonEvent|NMCache' | head -80
echo
echo "===== current media session ====="
dumpsys media_session | grep -E 'Media button session|SessionTag|state=PlaybackState' | head
