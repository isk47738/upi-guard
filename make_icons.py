import sys
import os

# Generate simple PNG icons using only stdlib
def make_png_icon(size, filename):
    import struct, zlib

    def make_png(w, h, pixels_rgba):
        def chunk(tag, data):
            c = struct.pack('>I', len(data)) + tag + data
            c += struct.pack('>I', zlib.crc32(tag + data) & 0xffffffff)
            return c

        raw = b''
        for row in pixels_rgba:
            raw += b'\x00'
            for r, g, b, a in row:
                raw += bytes([r, g, b, a])

        ihdr = struct.pack('>IIBBBBB', w, h, 8, 2, 0, 0, 0)
        # 8 bit depth, color type 2 = RGB (we'll use 6 = RGBA)
        ihdr = struct.pack('>II', w, h) + bytes([8, 6, 0, 0, 0])
        idat = zlib.compress(raw)

        return (b'\x89PNG\r\n\x1a\n'
                + chunk(b'IHDR', ihdr)
                + chunk(b'IDAT', idat)
                + chunk(b'IEND', b''))

    # Build pixels: dark navy bg with shield emoji approximation
    pixels = []
    cx, cy = size // 2, size // 2
    r_outer = int(size * 0.42)
    r_inner = int(size * 0.28)

    for y in range(size):
        row = []
        for x in range(size):
            dx, dy = x - cx, y - cy
            dist = (dx*dx + dy*dy) ** 0.5
            # Background gradient (dark navy)
            bg_r = max(10, min(80, int(10 + (x/size)*50)))
            bg_g = max(15, min(90, int(15 + (y/size)*40)))
            bg_b = max(30, min(140, int(30 + (dist/r_outer)*80)))

            if dist < r_outer:
                # Gradient circle fill (blue to teal)
                t = dist / r_outer
                ir = int(79 + (0 - 79) * t)
                ig = int(142 + (212 - 142) * t)
                ib = int(247 + (170 - 247) * t)
                alpha = 255
                # Shield shape (pentagon-ish)
                in_shield = (abs(dx) < r_outer * 0.75) and not (dy > r_outer * 0.5 and abs(dx) > r_outer * (0.75 - (dy - r_outer*0.5) / (r_outer*0.5)))
                if in_shield:
                    row.append((ir, ig, ib, alpha))
                else:
                    row.append((bg_r, bg_g, bg_b, 255))
            else:
                row.append((bg_r, bg_g, bg_b, 255))
        pixels.append(row)

    with open(filename, 'wb') as f:
        f.write(make_png(size, size, pixels))

    print(f"Created {filename} ({size}x{size})")

out_dir = os.path.dirname(os.path.abspath(__file__))
make_png_icon(192, os.path.join(out_dir, 'icon-192.png'))
make_png_icon(512, os.path.join(out_dir, 'icon-512.png'))
print("Icons generated successfully!")
