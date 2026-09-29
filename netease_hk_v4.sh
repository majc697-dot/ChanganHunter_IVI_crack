#!/system/bin/sh
# Steering-wheel media key bridge (v4)
# Forwards HW keys 2(prev)/3(next)/12(play-pause) to the 3rd-party
# media session (NetEase / KuGou) via standard MediaSession dispatch.
# Factory KuGou SDK link is neutralized (service disabled).
# Gate:
#   state=3 (playing)  -> always forward
#   state=2 (paused)   -> forward only within GRACE ms after the pause,
#                         so play/prev/next can resume the last app;
#                         after that keys fall back to factory sources.
LOG=/data/local/tmp/netease_hk.log
RAW=/data/local/tmp/netease_hk.raw
GRACE=600000          # 10 minutes

echo "$(date) bridge v4 start pid=$$" > $LOG
: > $RAW
logcat -c 2>/dev/null

logcat -v brief 'Launcher-library-common:V' '*:S' 2>/dev/null | while IFS= read -r line; do
    case "$line" in
        *"OnHKChange"*"keyCode"*) ;;
        *) continue ;;
    esac
    echo "$line" >> $RAW
    code=$(echo "$line" | grep -o 'keyCode[ :]*[0-9]*' | grep -o '[0-9]*$')
    hkstate=$(echo "$line" | grep -o 'keyState[ :]*[0-9]*' | grep -o '[0-9]*$')
    [ "$hkstate" = "0" ] || continue
    case "$code" in
        2) key=previous ;;
        3) key=next ;;
        12) key=play-pause ;;
        *) continue ;;
    esac
    nowms=$(awk '{printf "%d", $1*1000}' /proc/uptime)
    # output: pkg playbackstate updatedMs
    sessions=$(dumpsys media_session 2>/dev/null | awk '
        /Sessions Stack/ {instack=1}
        instack && /package=/ {pkg=$0; sub(/.*package=/,"",pkg); act=""}
        instack && /active=/ {act=$0}
        instack && /state=PlaybackState/ {
            ps=$0; sub(/.*state=/,"",ps); sub(/[^0-9].*/,"",ps)
            up=$0; sub(/.*updated=/,"",up); sub(/[^0-9].*/,"",up)
            if ((pkg ~ /cloudmusic|kugou/) && (act ~ /active=true/)) print pkg":"ps":"up
        }')
    pkg=""
    for want in com.netease.cloudmusic.iot com.kugou.android.auto; do
        row=$(echo "$sessions" | grep "^$want:")
        [ -n "$row" ] || continue
        ps=${row#*:}; ps=${ps%%:*}
        up=${row##*:}
        if [ "$ps" = "3" ]; then pkg=$want; break; fi
        if [ "$ps" = "2" ] && [ -n "$up" ]; then
            age=$((nowms - up))
            if [ "$age" -lt "$GRACE" ]; then pkg=$want; break; fi
        fi
    done
    if [ -z "$pkg" ]; then
        echo "$(date) skip code=$code no-active-3p" >> $LOG
        continue
    fi
    echo "$(date) FWD code=$code -> $key ($pkg)" >> $LOG
    /system/bin/media dispatch "$key" >> $LOG 2>&1
done
echo "$(date) bridge exit" >> $LOG
