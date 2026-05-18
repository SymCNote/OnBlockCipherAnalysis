



from z3 import *

dx, dy, dz = BitVecs('dx dy dz', 5)
s = Solver()

# 5-bit addition is naturally mod 32.
# Since all values are left-shifted by 1 (LSB = 0), this effectively models
# 4-bit modular arithmetic (mod 16) stored in bits [4:1].
# The LSB of the sum is always 0, and the carry out of bit 4 is auto-dropped.
s.add(dz == dx + dy)                   # No % needed — wrapping is automatic

s.add(dx == BitVecVal(8, 5) << 1)      # 8 << 1 = 16  (10000)
s.add(dy == BitVecVal(9, 5) << 1)      # 5 << 1 = 10  (01010)
s.add(dz == BitVecVal(1, 5) << 1)     # 13 << 1 = 26 (11010), since 8+5=13

print(s.check())   
print(s)
if s.check() == sat:
	m = s.model()
	print(bin(m[dx].as_long()), bin(m[dy].as_long()), bin(m[dz].as_long())) 
