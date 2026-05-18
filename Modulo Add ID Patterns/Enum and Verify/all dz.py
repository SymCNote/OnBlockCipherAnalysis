



dx = 0b0110
dy = 0b1010

print(f"dx={dx:04b}")
print(f"dy={dy:04b}")


seen = set()

for x0 in range(16):
    x1 = x0 ^ dx
    for y0 in range(16):
        y1 = y0 ^ dy
        z0 = (x0 + y0) & 0xF
        z1 = (x1 + y1) & 0xF
        dz = z0 ^ z1
        if dz not in seen:
            seen.add(dz)
            print(f"dz={dz:04b} ({dz})")