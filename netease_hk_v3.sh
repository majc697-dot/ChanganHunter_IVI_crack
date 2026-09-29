#!/system/bin/sh
# Steering-wheel media key bridge (v3)
# Forwards HW keys 2(prev)/3(next)/12(play-pause) to the active 3rd-party
# media session (NetEase / KuGou) via standard MediaSession dispatch.
# Original KuGou SDK link is neutralized (service disabled) so it no-ops.
# Forwards only while the 3rd-party session is actually playing (state=3);
# otherwise keys fall through to the factory source (radio/BT/USB).
LOG=/data/local/tmp/netease_hk.log
RAW=/data/local/tmp/netease_hk.raw

echo "$(date) bridge v3 start pid=$$" > $LOG
: > $RAW
logcat -c 2>/dev/null

logcat -v brief 'Launcher-library-common:V' '*:S' 2>/dev/null | while IFS= read -r line; do
    case "$line" in
        *"OnHKChange"*"keyCode"*) ;;
        *) continue ;;
    esac
    echo "$line" >> $RAW
    code=$(echo "$line" | grep -o 'keyCode[ :]*[0-9]*' | grep -o '[0-9]*$')
    state=$(echo "$line" | grep -o 'keyState[ :]*[0-9]*' | grep -o '[0-9]*$')
    [ "$state" = "0" ] || continue
    case "$code" in
        2) key=previous ;;
        3) key=next ;;
        12) key=play-pause ;;
        *) continue ;;
    esac
    ds=$(dumpsys media_session 2>/dev/null)
    # pick a 3rd-party session that is ACTUALLY playing (state=3, active=true)
    targets=$(echo "$ds" | awk '
        /Sessions Stack/ {instack=1}
        instack && /package=/ {pkg=$0; sub(/.*package=/,"",pkg); act=""; st=""}
        instack && /active=/ {act=$0}
        instack && /state=PlaybackState/ {
            if ((pkg ~ /cloudmusic|kugou/) && ($0 ~ /state=3/) && (act ~ /active=true/)) print pkg
        }')
    case "$targets" in
        *cloudmusic*) pkg=com.netease.cloudmusic.iot ;;
        *kugou*) pkg=com.kugou.android.auto ;;
        *) echo "$(date) skip code=$code no3p-playing" >> $LOG; continue ;;
    esac
    echo "$(date) FWD code=$code -> $key ($pkg)" >> $LOG
    /system/bin/media dispatch "$key" >> $LOG 2>&1
done
echo "$(date) bridge exit" >> $LOG
