# -*- coding: utf-8 -*-
# Minimal binary AXML parser
import zipfile, struct, sys

APK = r"c:\Users\24920\Documents\trae_projects\MT8666\CA_Launcher.apk"
TARGET = sys.argv[1] if len(sys.argv) > 1 else 'res/xml/default_workspace.xml'

data = zipfile.ZipFile(APK).read(TARGET)

def u16(o): return struct.unpack_from('<H', data, o)[0]
def u32(o): return struct.unpack_from('<I', data, o)[0]

assert u16(0) == 0x0003 and u16(2) == 0x0008
# string pool starts at 8
sp = 8
assert u16(sp) == 0x0001
sp_size = u32(sp+4)
string_count = u32(sp+8)
style_count = u32(sp+12)
flags = u32(sp+16)
strings_start = u32(sp+20)
is_utf8 = bool(flags & 0x1 << 8)
offs = [u32(sp+28+i*4) for i in range(string_count)]
pool = sp + strings_start
strings = []
for off in offs:
    p = pool + off
    if is_utf8:
        # uleb char len, uleb byte len
        def uleb(q):
            r=0
            while True:
                b=data[q];q+=1; r=(r<<7)|(b&0x7f)
                if not b&0x80: return r,q
        _,p = uleb(p); n,p = uleb(p)
        s = data[p:p+n].decode('utf-8','replace')
    else:
        n = u16(p); p += 2
        s = data[p:p+n*2].decode('utf-16-le','replace')
    strings.append(s)

# walk chunks after string pool
out = []
indent = 0
p = sp + sp_size
end = len(data)
while p < end:
    ctype = u16(p); csize = u32(p+4)
    if csize <= 0: break
    if ctype == 0x0100:  # START_NAMESPACE
        pass
    elif ctype == 0x0101:  # END_NAMESPACE
        pass
    elif ctype == 0x0102:  # START_ELEMENT
        name_idx = u32(p+20)
        name = strings[name_idx] if name_idx < len(strings) else str(name_idx)
        attr_start = u16(p+24)
        attr_size = u16(p+26)
        attr_count = u16(p+28)
        ap = p + attr_start
        attrs = []
        for i in range(attr_count):
            a = ap + i*attr_size
            ns_i = u32(a); n_i = u32(a+4); raw_i = u32(a+8)
            tsize = u32(a+12); t0 = data[a+16]; t1 = data[a+17]
            val = u32(a+20)
            aname = strings[n_i] if n_i < len(strings) else str(n_i)
            if raw_i != 0xffffffff and raw_i < len(strings):
                aval = strings[raw_i]
            else:
                types = {0x03:'str',0x04:'float',0x10:'int',0x11:'ref',0x12:'bool'}
                aval = str(val) if t1 in (0x10,0x12,0x11) else f"@{val:08x}"
            attrs.append(f'{aname}="{aval}"')
        out.append('  '*indent + '<' + name + (' ' + ' '.join(attrs) if attrs else '') + '>')
        indent += 1
    elif ctype == 0x0103:  # END_ELEMENT
        indent -= 1
        name_idx = u32(p+20)
        name = strings[name_idx] if name_idx < len(strings) else str(name_idx)
        out.append('  '*indent + f'</{name}>')
    p += csize

print('\n'.join(out))
