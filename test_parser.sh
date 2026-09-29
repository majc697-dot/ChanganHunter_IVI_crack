#!/system/bin/sh
dumpsys media_session 2>/dev/null | awk '
    /Sessions Stack/ {instack=1}
    instack && /package=/ {pkg=$0; sub(/.*package=/,"",pkg); act=""}
    instack && /active=/ {act=$0}
    instack && /state=PlaybackState/ {
        ps=$0; sub(/.*state=/,"",ps); sub(/[^0-9].*/,"",ps)
        up=$0; sub(/.*updated=/,"",up); sub(/[^0-9].*/,"",up)
        print "DBG pkg=" pkg " act=" act " ps=" ps " up=" up
        if ((pkg ~ /cloudmusic|kugou/) && (act ~ /active=true/)) print pkg":"ps":"up
    }'
