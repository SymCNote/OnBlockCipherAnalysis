


% differential x
array[0..3] of 0..1: dx41;  % <-- give value X[4,3,2,1]
var 0..1: dx0;
array[0..4] of var 0..1: dx;
constraint dx[4] = dx0 /\ forall(i in 0..3)(dx[i] = dx41[i]);
% value x
array[0..4] of var 0..1: x0;
array[0..4] of var 0..1: x1;
constraint forall(i in 0..4)(dx[i] = (x0[i] + x1[i]) mod 2);
% to int x
var 0..31: ix0 = sum(i in 0..4)(x0[i] * pow(2,4-i));
var 0..31: ix1 = sum(i in 0..4)(x1[i] * pow(2,4-i));

% differential y
array[0..3] of 0..1: dy41;  % <-- give value Y[4,3,2,1]
var 0..1: dy0;
array[0..4] of var 0..1: dy;
constraint dy[4] = dy0 /\ forall(i in 0..3)(dy[i] = dy41[i]);
% value y
array[0..4] of var 0..1: y0;
array[0..4] of var 0..1: y1;
constraint forall(i in 0..4)(dy[i] = (y0[i] + y1[i]) mod 2);
var 0..31: iy0 = sum(i in 0..4)(y0[i] * pow(2,4-i));
var 0..31: iy1 = sum(i in 0..4)(y1[i] * pow(2,4-i));

% --- value z ---
array[0..4] of var 0..1: z0;
array[0..4] of var 0..1: z1;
var 0..31: iz0 = sum(i in 0..4)(z0[i] * pow(2,4-i));
var 0..31: iz1 = sum(i in 0..4)(z1[i] * pow(2,4-i));

% differential g
array[0..3] of 0..1: dg41;  % <-- give value Y[4,3,2,1]
var 0..1: dg0;
array[0..4] of var 0..1: dg;
constraint dg[4] = dg0 /\ forall(i in 0..3)(dg[i] = dg41[i]);
% value g
array[0..4] of var 0..1: g0;
array[0..4] of var 0..1: g1;
constraint forall(i in 0..4)(dg[i] = (g0[i] + g1[i]) mod 2);
var 0..31: ig0 = sum(i in 0..4)(g0[i] * pow(2,4-i));
var 0..31: ig1 = sum(i in 0..4)(g1[i] * pow(2,4-i));

% --- value f ---
array[0..4] of var 0..1: f0;
array[0..4] of var 0..1: f1;
var 0..31: if0 = sum(i in 0..4)(f0[i] * pow(2,4-i));
var 0..31: if1 = sum(i in 0..4)(f1[i] * pow(2,4-i));

% differential u
array[0..3] of 0..1: du41;  % <-- give value U[4,3,2,1]
var 0..1: du0;
array[0..4] of var 0..1: du;
constraint du[4] = du0 /\ forall(i in 0..3)(du[i] = du41[i]);
% value u
array[0..4] of var 0..1: u0;
array[0..4] of var 0..1: u1;
constraint forall(i in 0..4)(du[i] = (u0[i] + u1[i]) mod 2);
var 0..31: iu0 = sum(i in 0..4)(u0[i] * pow(2,4-i));
var 0..31: iu1 = sum(i in 0..4)(u1[i] * pow(2,4-i));

% differential h
array[0..3] of 0..1: dh41;  % <-- give value H[4,3,2,1]
var 0..1: dh0;
array[0..4] of var 0..1: dh;
constraint dh[4] = dh0 /\ forall(i in 0..3)(dh[i] = dh41[i]);
% value h
array[0..4] of var 0..1: h0;
array[0..4] of var 0..1: h1;
constraint forall(i in 0..4)(dh[i] = (h0[i] + h1[i]) mod 2);
var 0..31: ih0 = sum(i in 0..4)(h0[i] * pow(2,4-i));
var 0..31: ih1 = sum(i in 0..4)(h1[i] * pow(2,4-i));

% ------------------------------------------------------------

% propagation x add y = z
constraint iz0 = (ix0 + iy0) mod 32;
constraint iz1 = (ix1 + iy1) mod 32;

% g = z xor y
constraint forall(i in 0..4)(g0[i] = (z0[i] + y0[i]) mod 2);
constraint forall(i in 0..4)(g1[i] = (z1[i] + y1[i]) mod 2);

% propagation z add g = f
constraint if0 = (iz0 + ig0) mod 32;
constraint if1 = (iz1 + ig1) mod 32;

% u = g xor f
constraint forall(i in 0..4)(u0[i] = (g0[i] + f0[i]) mod 2);
constraint forall(i in 0..4)(u1[i] = (g1[i] + f1[i]) mod 2);

% propagation f add u = h
constraint ih0 = (if0 + iu0) mod 32;
constraint ih1 = (if1 + iu1) mod 32;

% output["dx: " ++ show(dx) ++ " | x0: " ++ show(x0) ++ " | x1: " ++ show(x1) ++ "\n"];
% output["dy: " ++ show(dy) ++ " | y0: " ++ show(y0) ++ " | y1: " ++ show(y1) ++ "\n"];
% % output["dz: " ++ show(dz) ++ " | z0: " ++ show(z0) ++ " | z1: " ++ show(z1) ++ "\n"];
% output["dg: " ++ show(dg) ++ " | g0: " ++ show(g0) ++ " | g1: " ++ show(g1) ++ "\n"];
% output["dh: " ++ show(dh) ++ " | h0: " ++ show(h0) ++ " | h1: " ++ show(h1) ++ "\n"];