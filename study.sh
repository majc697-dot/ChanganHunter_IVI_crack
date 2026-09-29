#!/system/bin/sh
d=/data/local/tmp/f_study
rm -rf $d; mkdir -p $d
ev=$d/events.txt
: > $ev
i=0
# phase 1: 8s idle (32 frames @0.25s), phase2: 12s with 3 dispatches
total=80
while [ $i -lt $total ]; do
    screencap -p $d/f_$(printf %03d $i).png
    t=$((i*250))
    if [ $i -eq 44 ] || [ $i -eq 56 ] || [ $i -eq 68 ]; then
        echo "dispatch-next at frame $i t=${t}ms wall=$(date +%H:%M:%S.%N)" >> $ev
        /system/bin/media dispatch next
    fi
    i=$((i+1))
    sleep 0.25
done
echo done
