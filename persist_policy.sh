#!/system/bin/sh
# 持久化当前运行时策略到 precompiled_sepolicy，并预验证可加载性
MP=/data/local/tmp/magiskpolicy

echo "=== 1. save runtime policy to tmp ==="
$MP --save /data/local/tmp/new_sepolicy
echo "SAVE_RC=$?"
ls -la /data/local/tmp/new_sepolicy

echo "=== 2. verify loadable (load back into kernel) ==="
$MP --load /data/local/tmp/new_sepolicy
echo "LOAD_RC=$?"

echo "=== 3. still alive? test hh_rootd ==="
echo "id; exit" | toybox nc -w 3 127.0.0.1 9753
echo "NC_RC=$?"

echo "=== 4. backup vendor precompiled then overwrite ==="
mount -o rw,remount /vendor
cp /vendor/etc/selinux/precompiled_sepolicy /data/local/tmp/precompiled_sepolicy.bak2
cp /data/local/tmp/new_sepolicy /vendor/etc/selinux/precompiled_sepolicy
chmod 644 /vendor/etc/selinux/precompiled_sepolicy
echo "CP_RC=$?"
ls -la /vendor/etc/selinux/precompiled_sepolicy*
mount -o ro,remount /vendor

echo "=== 5. final state ==="
getenforce
ps -A | grep -E 'hh_rootd|nc' | grep -v grep
