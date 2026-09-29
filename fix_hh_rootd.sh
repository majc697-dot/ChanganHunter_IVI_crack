#!/system/bin/sh
# 从 hh_rootd.sh 中移除 setenforce 0，保持全局 Enforcing
setprop ctl.stop hh_rootd
sleep 1

mount -o rw,remount /

cat > /system/xbin/hh_rootd.sh <<'EOF'
#!/system/bin/sh
while true; do
  toybox nc -s 127.0.0.1 -p 9753 -l /system/bin/sh
  sleep 1
done
EOF

chmod 755 /system/xbin/hh_rootd.sh
chcon u:object_r:system_file:s0 /system/xbin/hh_rootd.sh
mount -o ro,remount /

setprop ctl.start hh_rootd
sleep 2

getenforce
echo "=== test connect ==="
echo "id; exit" | toybox nc -w 3 127.0.0.1 9753
echo "NC_RC=$?"
