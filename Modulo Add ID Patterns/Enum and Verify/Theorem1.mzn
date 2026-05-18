

array[0..3] of var 0..1: dx;
array[0..3] of var 0..1: dy;
constraint dx = array1d(0..3,[0, 1, 1, 0]);
constraint dy = array1d(0..3,[1, 0, 1, 0]);
var 0..15: DX;
var 0..15: DY;
constraint DX = sum(i in 0..3)(dx[i] * pow(2,3-i));
constraint DY = sum(i in 0..3)(dy[i] * pow(2,3-i));

array[0..3] of var 0..1: dz;
var 0..15: DZ;
constraint DZ = sum(i in 0..3)(dz[i] * pow(2,3-i));


constraint dz[3] = (dx[3] + dy[3]) mod 2; % the lowest bit
constraint forall(i in 0..2)(
  if ((dx[i+1] = dy[i+1]) /\ (dx[i+1] = dz[i+1])) then ((dx[i] + dy[i] + dz[i]) mod 2 = dx[i+1]) endif
);

int: alldz;
constraint DZ = alldz;


  
