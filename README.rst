A GRACE data extraction library
=======================

This project is used to extract the data from GRACE (Gravity Recovery And Climate Experiment)
L1B binary data files. The data types in L1B includes KBR (K Band Ranging),
GNV (GPS Navigation position), SCA (Star Camera Assembly ),
spacecraft mass history and acceleration observations (with an accuracy of 1 nm/s^2).
The binary data format is from the "GRACE Level 1B data Product User Handbook".

In this library, the functions for getting the data are listed here:
getKBR(filename)
getGNV(filename)
getSCA(filename)
getACC(filename)
getMass(filename)

The return values for these functions are a list containing the data struct of corresponding data types.
All the definition of the data types are as follows:

KBR {
  time;
  biased_range;
  range_rate;
  range_accl;
  iono_corr;
  lighttime_corr;
  lighttime_rate;
  lighttime_accl;
  ant_centr_corr;
  ant_centr_rate;
  ant_centr_accl;
  }

GNV {
  coord_ref;
  time;
  xpos;
  ypos;
  zpos;
  xvel;
  yvel;
  zvel;
}

SCA {
  time;
  quatangle;
  quaticoeff;
  quatjcoeff;
  quatkcoeff;
}

MASS {
  time;
  mass;
}

ACC {
  time;
  lin_acc_x;
  lin_acc_y;
  lin_acc_z;
}

The time is defined as GPS time system and is stored as "datetime" in python library.
