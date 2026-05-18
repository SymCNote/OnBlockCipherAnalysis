


% the difference
array[0..3] of var 0..1: dx;
array[0..3] of var 0..1: dy;
constraint dx = array1d(0..3,[0, 1, 1, 0]);
constraint dy = array1d(0..3,[1, 0, 1, 0]);
var 0..15: DX;
var 0..15: DY;
constraint DX = sum(i in 0..3)(dx[i] * pow(2,3-i));
constraint DY = sum(i in 0..3)(dy[i] * pow(2,3-i));


% the value
array[0..3] of var 0..1: x0;
array[0..3] of var 0..1: x1;
array[0..3] of var 0..1: y0;
array[0..3] of var 0..1: y1;
var 0..15: X0;
var 0..15: X1;
var 0..15: Y0;
var 0..15: Y1;
constraint X0 = sum(i in 0..3)(x0[i] * pow(2,3-i));
constraint X1 = sum(i in 0..3)(x1[i] * pow(2,3-i));
constraint Y0 = sum(i in 0..3)(y0[i] * pow(2,3-i));
constraint Y1 = sum(i in 0..3)(y1[i] * pow(2,3-i));

% difference <--> value
constraint forall(i in 0..3)(dx[i] = (x0[i] + x1[i]) mod 2);
constraint forall(i in 0..3)(dy[i] = (y0[i] + y1[i]) mod 2);


% ---===---

% x + y = z, z here
array[0..3] of var 0..1: dz;
var 0..15: DZ;
constraint DZ = sum(i in 0..3)(dz[i] * pow(2,3-i));
array[0..3] of var 0..1: z0;
array[0..3] of var 0..1: z1;
var 0..15: Z0;
var 0..15: Z1;
constraint Z0 = sum(i in 0..3)(z0[i] * pow(2,3-i));
constraint Z1 = sum(i in 0..3)(z1[i] * pow(2,3-i));

constraint Z0 = (X0 + Y0) mod 16;
constraint Z1 = (X1 + Y1) mod 16;
constraint forall(i in 0..3)(dz[i] = (z0[i] + z1[i]) mod 2);


% ----- ===== -----
% some test
int: alldz;
constraint DZ = alldz;

output["X: " ++ show(dx) ++ show(x0) ++ show(x1) ++ "\n"];
output["Y: " ++ show(dy) ++ show(y0) ++ show(y1) ++ "\n"];
output["Z: " ++ show(dz) ++ show(z0) ++ show(z1)];
