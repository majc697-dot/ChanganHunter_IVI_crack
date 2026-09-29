#!/system/bin/sh
# burst N parallel screencaps, then timestamp when each returns
d=/data/local/tmp/burst
rm -rf $d; mkdir -p $d
N=10
i=0
while [ $i -lt $N ]; do
    (
      t0=$(date +%s.%N)
      screencap -p $d/c_$i.png
      t1=$(date +%s.%N)
      echo "$i start=$t0 end=$t1" > $d/t_$i.txt
    ) &
    i=$((i+1))
    sleep 0.05
done
wait
cat $d/t_*.txt
md5sum $d/c_*.png
