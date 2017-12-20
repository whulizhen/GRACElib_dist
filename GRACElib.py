# GRACE data extraction script
# data source:  https://podaac.jpl.nasa.gov/dataset/GRACE_L1B_GRAV_JPL_RL02
#                ftp://podaac-ftp.jpl.nasa.gov/allData/grace/L1B/JPL/RL02



import os
import struct
import datetime
from datetime import datetime
from struct import *
from sys import path
from datetime import timedelta

class dataStruct:
    pass




## get all the binary data
def getData(filename):
    if not os.path.isfile(filename):
        print("ERROR: %s is not a valid file." % (filename));
        return None;

    file = open(filename,"rb");
    line = "";
    while "ND OF HEADER" not in line:
        line = file.readline();
    # read in the data
    data_b = file.read();
    file.close();
    #print len(data_b);
    return data_b;


# get the KBR raning measurements
def getKBR(filename):
    data=[];
    # in GPS time system
    reftime_str = '2000/01/01/12:00:00.000000';
    timeformat='%Y/%m/%d/%H:%M:%S.%f';
    reftime = datetime.strptime(reftime_str, timeformat);
    data_b = getData(filename);
    # KBR data formats (big ending)
    kbr_format='>i10d4HB';
    size=calcsize(kbr_format);
    #print size;
    i=0;
    while i < len(data_b):
        delta_sec, \
        biased_range,range_rate,range_accl, \
        iono_corr, \
        lighttime_corr,lighttime_rate,lighttime_accl, \
        ant_centr_corr,ant_centr_rate,ant_centr_accl, \
        K_A_SNR,Ka_A_SNR,K_B_SNR,Ka_B_SNR,qualflg = struct.unpack(kbr_format,data_b[i:size+i]);
        i = i + size;
        dt=timedelta(days=0, seconds=delta_sec, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0);
        gps_time = reftime + dt;

        #print gps_time.strftime('%Y-%m-%d %H:%M:%S'), biased_range, range_rate, range_accl,iono_corr  \
        #    acl_x_res, acl_y_res,acl_z_res;
        kbr = dataStruct();
        kbr.time = gps_time;
        kbr.biased_range = biased_range;
        kbr.range_rate = range_rate;
        kbr.range_accl = range_accl;
        kbr.iono_corr = iono_corr;
        kbr.lighttime_corr = lighttime_corr;
        kbr.lighttime_rate = lighttime_rate;
        kbr.lighttime_accl = lighttime_accl;
        kbr.ant_centr_corr = ant_centr_corr;
        kbr.ant_centr_rate = ant_centr_rate;
        kbr.ant_centr_accl = ant_centr_accl;


        data.append(kbr);

    return data;

# get the position of GRACE satellite from GPS receiver
def getGNV(filename):
    data=[];
    # in GPS time system
    reftime_str = '2000/01/01/12:00:00.000000';
    timeformat='%Y/%m/%d/%H:%M:%S.%f';
    reftime = datetime.strptime(reftime_str, timeformat);
    data_b = getData(filename);
    # SCA data formats (big ending)
    sca_format='>i2c12dB';
    size=calcsize(sca_format);
    #print size;
    i=0;
    while i < len(data_b):
        delta_sec , grace_ID, coord_ref, \
        xpos, ypos,zpos,xpos_err,ypos_err,zpos_err,   \
        xvel,yvel,zvel,xvel_err,yvel_err,zvel_err,qualflg = struct.unpack(sca_format,data_b[i:size+i]);
        i = i + size;
        dt=timedelta(days=0, seconds=delta_sec, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0);
        gps_time = reftime + dt;

        # if coord_ref ='E': Earth-Fixed
        # coord_ref = 'I' : Earth-Inertial
        #print gps_time.strftime('%Y-%m-%d %H:%M:%S'), coord_ref,xpos,ypos,zpos,xvel,yvel,zvel,xpos_err,ypos_err,zpos_err;
        gnv = dataStruct();
        gnv.time = gps_time;
        gnv.xpos = xpos;
        gnv.ypos = ypos;
        gnv.zpos = zpos;
        gnv.xvel = xvel;
        gnv.yvel = yvel;
        gnv.zvel = zvel;
        gnv.coord_ref = coord_ref;
        data.append(gnv);

    return data;



# get the star camera assembly data, quarternions
def getSCA(filename):
    data=[];
    # in GPS time system
    reftime_str = '2000/01/01/12:00:00.000000';
    timeformat='%Y/%m/%d/%H:%M:%S.%f';
    reftime = datetime.strptime(reftime_str, timeformat);
    data_b = getData(filename);
    # SCA data formats (big ending)
    sca_format='>icB5dB';
    size=calcsize(sca_format);
    #print size;
    i=0;
    while i < len(data_b):
        delta_sec , grace_ID, sca_id, \
        quatangle, quaticoeff,quatjcoeff,quatkcoeff,qual_rss,   \
        qualflg =struct.unpack(sca_format,data_b[i:size+i]);
        i = i + size;
        dt=timedelta(days=0, seconds=delta_sec, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0);
        gps_time = reftime + dt;

        #print gps_time.strftime('%Y-%m-%d %H:%M:%S'), quatangle,quaticoeff,quatjcoeff,quatkcoeff \
        #    acl_x_res, acl_y_res,acl_z_res;
        sca = dataStruct();
        sca.time = gps_time;
        sca.quatangle = quatangle;
        sca.quaticoeff = quaticoeff;
        sca.quatjcoeff = quatjcoeff;
        sca.quatkcoeff = quatkcoeff;
        data.append(sca);

    return data;




def getMass(filename):
    data=[];
    # in GPS time system
    reftime_str = '2000/01/01/12:00:00.000000';
    timeformat='%Y/%m/%d/%H:%M:%S.%f';
    reftime = datetime.strptime(reftime_str, timeformat);

    data_b = getData(filename);

    #mass_format='>2i2cBc4d';
    #size=calcsize(mass_format);
    #print size;
    i=0;
    #len(data_b)
    while i < len(data_b):

        sec,microsec, time_ref, grace_id, qualflg, prod_flag = struct.unpack('>2i2cBc',data_b[i:12+i]);
        #print sec,microsec, time_ref, grace_id, qualflg, prod_flag, hex(ord(prod_flag));
        i = i + 12;
        count=0;
        value=[0, 0, 0, 0, 0, 0, 0, 0];
        bit=[0, 0, 0, 0, 0, 0, 0, 0];
        # 1 bit
        if(ord(prod_flag) & 0x1):
            #print 'SC mass from thruster usage';
            count=count+1;
            bit[count-1]=0;
        # 2 bit
        if(ord(prod_flag) & 0x2):
            #print 'SC Mass error bit0';
            count=count+1;
            bit[count-1]=1;
        # 3 bit
        if(ord(prod_flag) & 0x4):
            #print 'SC Mass from tank observations';
            count=count+1;
            bit[count-1]=2;
        # 4 bit
        if(ord(prod_flag) & 0x8):
            #print 'SC Mass error bit2';
            count=count+1;
            bit[count-1]=3;
        # 5 bit
        if(ord(prod_flag) & 0x10):
            #print 'gas mass tank 1 (thr. usage)';
            count=count+1;
            bit[count-1]=4;
        # 6 bit
        if(ord(prod_flag) & 0x20):
            #print 'gas mass tank 2 (thr. usage)';
            count=count+1;
            bit[count-1]=5;
        # 7 bit
        if(ord(prod_flag) & 0x40):
            #print 'gas mass tank 1 (tank obs)';
            count=count+1;
            bit[count-1]=6;
        # 8 bit
        if(ord(prod_flag) & 0x80):
            #print 'gass mass tank2(tank obs)';
            count=count+1;
            bit[count-1]=7;

        #print i,count, bit;
        for j in range(count):
            value[bit[j]]= struct.unpack('>d',data_b[i:i+8]);
            i = i + 8;

        dt=timedelta(days=0, seconds=sec, microseconds=microsec, milliseconds=0, minutes=0, hours=0, weeks=0);
        gps_time = reftime + dt;

        #print gps_time.strftime('%Y-%m-%d %H:%M:%S'), value[0],value[1],value[2],value[3],value[4],value[5],value[6],value[7]
        mass = dataStruct();
        mass.time = gps_time;
        if value[2] != 0.0 :
            mass.mass = value[2];
        elif value[0] != 0.0 :
            mass.mass = value[0];
        data.append(mass);

    return data;

def getACC(filename):
    
    data=[];
    # in GPS time system
    reftime_str = '2000/01/01/12:00:00.000000';
    timeformat='%Y/%m/%d/%H:%M:%S.%f';
    reftime = datetime.strptime(reftime_str, timeformat);

    data_b = getData(filename);

    # acc1B data formats (big ending)
    acc_format='>ic9dB';
    size=calcsize(acc_format);
    #print size;
    i=0;
    while i < len(data_b):
        delta_sec,grace_ID, \
        lin_acc_x, lin_acc_y,lin_acc_z,   \
        ang_acc_x, ang_acc_y,ang_acc_z,   \
        acl_x_res, acl_y_res,acl_z_res,qualflg =struct.unpack(acc_format,data_b[i:size+i]);
        i = i + size;
        dt=timedelta(days=0, seconds=delta_sec, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0);
        gps_time = reftime + dt;

        #print gps_time.strftime('%Y-%m-%d %H:%M:%S'), lin_acc_x, lin_acc_y, lin_acc_z ;
        #    acl_x_res, acl_y_res,acl_z_res;
        acc1b = dataStruct();
        acc1b.time = gps_time;
        acc1b.lin_acc_x = lin_acc_x;
        acc1b.lin_acc_y = lin_acc_y;
        acc1b.lin_acc_z = lin_acc_z;
        data.append(acc1b);

    return data;





#
# acc_time=[];
# acc_x=[];
# acc_y=[];
# acc_z=[];
#
# mass_time=[];
# mass=[];
#
# acc_file = "/Users/lizhen/experiments/GRACE/grace_1B_2008-01-25_02/ACC1B_2008-01-25_A_02.dat";
# mass_file = "/Users/lizhen/experiments/GRACE/grace_1B_2008-01-25_02/MAS1B_2008-01-25_A_02.dat";
# sca_file =  "/Users/lizhen/experiments/GRACE/grace_1B_2008-01-25_02/SCA1B_2008-01-25_A_02.dat";
# kbr_file =  "/Users/lizhen/experiments/GRACE/grace_1B_2008-01-25_02/KBR1B_2008-01-25_X_02.dat";
# gnv_file =  "/Users/lizhen/experiments/GRACE/grace_1B_2008-01-25_02/GNV1B_2008-01-25_A_02.dat";
# kbr_data = getKBR(kbr_file);
# sca_data = getSCA(sca_file);
# acc_data = getAcc(acc_file);
# mass_data = getMass(mass_file);
# nav_data = getGNV(gnv_file);
#
# size =len(acc_data); #range(size)
# #start1: 40980
# #start2: 42700
# length = 140
# for i in range(42700,42700+length):
#     acc_time.append(acc_data[i].time.strftime('%Y/%m/%d/%H:%M:%S.%f'));
#     acc_x.append(acc_data[i].lin_acc_x);
#     acc_y.append(acc_data[i].lin_acc_y);
#     acc_z.append(acc_data[i].lin_acc_z);
#     ##print mydata[i].time.strftime('%Y/%m/%d/%H:%M:%S.%f'), mydata[i].lin_acc_x,mydata[i].lin_acc_y,mydata[i].lin_acc_z
#
# size =len(mass_data);
# for i in range(size):
#     mass_time.append(mass_data[i].time.strftime('%Y/%m/%d/%H:%M:%S.%f'));
#     mass.append(mass_data[i].mass);
#     #print mass_data[i].time.strftime('%Y/%m/%d/%H:%M:%S.%f'), mass_data[i].mass[0]
#
#
# #myfigure = plt.figure( num= 1,figsize=(15,10),dpi = 127,tight_layout=True,frameon=True);
#
# acc =[acc_x,acc_y,acc_z];
# acc_mag=ListMag(acc);
# #timeAxisLinePlot(['acc_time','acc_x','acc_z'], [acc_time,acc_x,acc_z],'GRACE acceleration','GPS Time','Acceleration[m/s^2]');
# #timeAxisLinePlot(['acc_time','acc_y'], [acc_time,acc_y],'GRACE acceleration','GPS Time','Acceleration[m/s^2]');
# #timeAxisLinePlot(['acc_time','acc_mag'], [acc_time,acc_mag],'GRACE acceleration','GPS Time','Acceleration[m/s^2]');
#
# #plt.show();
# #myfigure.savefig('graceA_2008-1-25/graceA_acc_mag_test.pdf');
# #plt.close(1);
