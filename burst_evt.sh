#!/system/bin/sh
# sh burst_evt.sh <tag> <dispatch-after-ms|none>
tag=$1
after=$2
d=/data/local/tmp/b_$tag
rm -rf $d; mkdir -p $d
N=12
i=0
T0=$(date +%s.%N)
while [ $i -lt $N ]; do
    (
      screencap -p $d/c_$i.png
      echo "$i $(date +%s.%N)" > $d/t_$i.txt
    ) &
    i=$((i+1))
    sleep 0.04
done
if [ "$after" != none ]; then
    # busy-wait approximate offset, then dispatch
    target=$(echo "$T0 $after" | awk '{printf "%.3f", $1+$2/1000.0}')
    while :; do
        now=$(date +%s.%N)
        [ "$(echo "$now $target" | awk '{print ($1>=$2)}')" = 1 ] && break
    done
    echo "DISPATCH at $(date +%s.%N)" > $d/event.txt
    /system/bin/media dispatch next
fi
wait
cat $d/t_*.txt | sort -n
cat $d/event.txt 2>/dev/null
