import sys, zlib, struct
# 4 logic tiles, 16x16 each: wall, meadow patch, wetland patch, ledge
cols=[(200,40,40,160),(60,180,60,140),(40,90,200,140),(220,180,40,160)]
w,h=64,16
rows=b''
for y in range(h):
    r=b'\x00'
    for x in range(w):
        r+=bytes(cols[x//16])
    rows+=r
def chunk(t,d): return struct.pack('>I',len(d))+t+d+struct.pack('>I',zlib.crc32(t+d)&0xffffffff)
png=b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',w,h,8,6,0,0,0))+chunk(b'IDAT',zlib.compress(rows,9))+chunk(b'IEND',b'')
open(sys.argv[1],'wb').write(png)
