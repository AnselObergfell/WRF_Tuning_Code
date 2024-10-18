import netCDF4
import numpy as np
import os
import re
import glob
# Takes data from outfolder, filters out non evaluated times, extracts SWDOWN ~ obs_swdtot, returns SWDOWN and saves
def process(wrffolder,epoch_name,rad_type = 'SWDOWN'):
    def get_time_from_filename(filename):
        m = re.match(r"wrfout_d0\d_2009-05-(\d\d)_(\d\d):(\d\d):(\d\d)", filename)
        return (int(m[1]) - 6) * 24 + int(m[2]) + int(m[3]) / 60 + int(m[4]) / 3600

    outfile = glob.glob(os.path.join(wrffolder, "wrfout_d02*"))
    outfile = sorted(outfile, key=os.path.getmtime, reverse=True)[0]
    
    df = netCDF4.Dataset(outfile)
    
    if rad_type.upper() in ['SWDOWN', 'SWDDIR', 'SWDDIF']:
      data = df[rad_type][:].mean(axis=1).mean(axis=1)
    elif rad_type.upper() == 'SWDTOT':
      swddif = df['SWDDIF'][:].mean(axis=1).mean(axis=1)[36:]
      swddir = df['SWDDIR'][:].mean(axis=1).mean(axis=1)[36:]
      data = swddif + swddir
    else:
      raise ValueError("Invalid radiation type")
    
    np.save(epoch_name + '.npy', data)
    return data[36:]

def process_bnl(wrffolder, epoch_name):
    def getTIMES(df):
        TIMES = np.zeros(len(df['Times'][:]))
        for i, time in enumerate(df['Times'][:]):
          seconds = int(time[-2] + time[-1])
          minutes = int(time[-5] + time[-4])
          hours = int(time[-8] + time[-7])
          day = int(time[-11] + time[-10])-6
          TIMES[i] = day*24 + hours + minutes/60 + seconds/3600
        return TIMES
    outfile = 'wrfout_d02_2009-05-06_06:00:00'
    nc = netCDF4.Dataset(os.path.join(wrffolder, outfile))
    TIME = getTIMES(nc)[36:]
    SWDOWN = nc['SWDOWN'][:].mean(axis=1).mean(axis=1)[36:]
    SWDDIR = nc['SWDDIR'][:].mean(axis=1).mean(axis=1)[36:]
    SWDDIF = nc['SWDDIF'][:].mean(axis=1).mean(axis=1)[36:]
    SWDTOT = SWDDIR + SWDDIF
    data = np.array([TIME, SWDOWN, SWDDIR, SWDDIF, SWDTOT])
    np.save(epoch_name + '.npy', data)
    return data