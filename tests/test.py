import GRACElib
from GRACElib import *

gnv_file =  "/Users/lizhen/experiments/GRACE/grace_1B_2008-01-25_02/GNV1B_2008-01-25_A_02.dat";
nav_data = getGNV(gnv_file);
print nav_data[300].xpos
