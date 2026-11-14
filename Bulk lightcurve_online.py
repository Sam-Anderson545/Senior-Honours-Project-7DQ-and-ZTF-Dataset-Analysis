import pandas as pd
import matplotlib.pyplot as plt
import requests
import numpy as np
from matplotlib import font_manager as fm


"""
This script is intended for graphing many light curves, one after the other, for a 
list of UIDS provided in a text file. The light curve data is accessed online.

Note if you are running this code, the font used for the plots relies on a locally
stored .ttf file. Alter the plotting code for your individual system.
Also the text file route is specified explicitly, so change this as appropriate.
"""


# The 'with open(' lines below read in the UIDs from a text file, and convert them to integers.
with open('/Users/sam/Desktop/Uni/Y4/SHP/uid_data.txt', 'r') as f:
    UIDS = [int(float(line.strip())) for line in f.readlines()]


#print(UIDS)


n = 1

for uid in UIDS:

    
    if uid < 5000:
        URL = 'https://surveys.roe.ac.uk/al-web/7dq/data/merged/qsos/clean/lc_000000_005000.csv'
    else:
        
        if uid % 5000 == 0:
    
            end = uid
            start = uid - 4999
    
        else:
    
            end = ((uid // 5000) + 1) * 5000
            start = end - 4999

        URL = f'https://surveys.roe.ac.uk/al-web/7dq/data/merged/qsos/clean/lc_{start:06d}_{end:06d}.csv'




    response = requests.get(URL, verify=False, stream=True)
    response.raise_for_status()

    matches = []
    for chunk in pd.read_csv(response.raw, usecols=['uid', 'mjd', 'mag', 'band', 'sid'], chunksize=100_000,):
        selected = chunk[(chunk['uid'] == uid) & (chunk['sid'] == 11)]
        if not selected.empty:
            matches.append(selected)

    #print(matches)



    # Concatenate data into a single DataFrame, and separate it into the 
    # different bands.

    lightcurves = pd.concat(matches, ignore_index=True)
    r_band = np.array([lightcurves[lightcurves['band'] == 'r']])
    g_band = np.array([lightcurves[lightcurves['band'] == 'g']])
    i_band = np.array([lightcurves[lightcurves['band'] == 'i']])


    # Reshape the band arrays to 2d arrays that are easier to handle.

    r_band_2d = r_band.reshape(r_band.shape[1], r_band.shape[2])
    g_band_2d = g_band.reshape(g_band.shape[1], g_band.shape[2])
    i_band_2d = i_band.reshape(i_band.shape[1], i_band.shape[2])




    """
    matches = []
    for chunk in pd.read_csv(URL, usecols=['uid', 'mjd', 'mag', 'band'], chunksize=100_000):
        selected = chunk[chunk['uid'].isin(UIDS)]
        if not selected.empty:
            matches.append(selected)

    if not matches:
        raise ValueError(f'No rows found for uid(s): {UIDS}')

    print(matches)

    """

    # Plot all three bands for the current UID on a new set of axes.

        

    font_path = '/Users/sam/Desktop/Uni/Y4/SHP/cmunrm.ttf'

    fm.fontManager.addfont(font_path)

    # Plot all three bands on one set of axes
    plt.rcParams['font.family'] = 'serif'
    plt.rcParams['font.serif'] = ['CMU Serif', 'CMU Serif Roman']

    plt.style.use('seaborn-v0_8-deep')



    plt.figure()
    plt.plot(i_band_2d[:,1], i_band_2d[:,2], '-o', label='i band', markersize=2)
    plt.plot(g_band_2d[:,1], g_band_2d[:,2], '-o', label='g band', markersize=2)
    plt.plot(r_band_2d[:,1], r_band_2d[:,2], '-o', label='r band', markersize=2)
    plt.xlabel('Modified Julian Date')
    plt.ylabel('Magnitude')
    ax = plt.gca()
    ax.invert_yaxis()
    #plt.ylim(22, 14)
    #plt.xlim(58000, 60000)
    plt.title(f'Lightcurve for uid {uid}')
    plt.legend()
    plt.show()
    plt.close()
    print(n)
    n += 1
