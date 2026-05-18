
dx4 = 0b0000
dy4 = 0b0000
dg4 = 0b0011

seen_dh = set()

for dx_bit in (0, 1):   
    dx = (dx4 << 1) | dx_bit
    for dy_bit in (0, 1):
        dy = (dy4 << 1) | dy_bit
        for dg_bit in (0, 1):    
            dg = (dg4 << 1) | dg_bit
            
            for x0 in range(32):
                x1 = x0 ^ dx
                for y0 in range(32):
                    y1 = y0 ^ dy
                    for g0 in range(32):
                        g1 = g0 ^ dg

                        z0 = (x0 + y0) & 0x1F
                        z1 = (x1 + y1) & 0x1F

                        mask = 0x1E
                        if ((y0 ^ z0) & mask) == (g0 & mask) and ((y1 ^ z1) & mask) == (g1 & mask):
                        
                            h0 = (z0 + g0) & 0x1F
                            h1 = (z1 + g1) & 0x1F

                            dh = h0 ^ h1
                            
                            seen_dh.add(dh)


for dh in sorted(seen_dh):
    print(f"{dh:02d}: {dh:05b}")
print("\n#dh:", len(seen_dh)/2)
