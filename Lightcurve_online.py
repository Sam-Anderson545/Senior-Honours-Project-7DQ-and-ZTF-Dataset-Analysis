
import pandas as pd
import matplotlib.pyplot as plt
import requests
import numpy as np
from matplotlib import font_manager as fm


"""

This script reads a large CSV file containing lightcurve data for quasars, 
filters the data for specific unique identifiers (UIDs), and plots the 
lightcurves for those UIDs.

Note if you are running this code, the font used for the plots relies on a locally 
stored .ttf file. Alter the plotting code for your individual system.

"""


#URL = 'https://surveys.roe.ac.uk/al-web/7dq/data/merged/qsos/clean/lc_000000_005000.csv'
UIDS = [224700]

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


#print(URL)

# Retrieve the RA, Dec and other info for the quasar:

ra, dec, Lbol, MBH, MBH_err = [], [], [], [], []
for chunk in pd.read_csv('/Users/sam/Desktop/Uni/Y4/SHP/dr16q_vac_shen_matched.csv', usecols=['ra', 'dec', 'uid', 'Lbol', 'MBH', 'MBH_err'], chunksize=100_000):
    selected = chunk[chunk['uid'].isin(UIDS)]
    if not selected.empty:
        ra.append(float(selected['ra'].values[0]))
        dec.append(float(selected['dec'].values[0]))
        Lbol.append(float(selected['Lbol'].values[0]))
        MBH.append(float(selected['MBH'].values[0]))
        MBH_err.append(float(selected['MBH_err'].values[0]))

if len(ra) != 0:
    print(f'RA: {ra[0]}')
    print(f'Dec: {dec[0]}')
    print(f'Lbol: {Lbol[0]}')
    print(f'MBH: {MBH[0]}')
    print(f'MBH_err: {MBH_err[0]}')







# Read the CSV file in chunks and record the rows that correspond to the 
# desired UID. The intermediate fix here has been to use 'verify=False', 
# however this carries risks that should perhaps be avoided.


response = requests.get(URL, verify=False, stream=True)
response.raise_for_status()

matches = []
for chunk in pd.read_csv(response.raw, usecols=['uid', 'mjd', 'mag', 'band', 'sid'], chunksize=100_000,):
    selected = chunk[(chunk['uid'].isin(UIDS))]
    if not selected.empty:
        matches.append(selected)

#print(matches)



# Concatenate data into a single DataFrame, and separate it into the 
# different bands.

lightcurves = pd.concat(matches, ignore_index=True)
r_band = np.array([lightcurves[(lightcurves['band'] == 'r') & (lightcurves['sid']==11)]])
g_band = np.array([lightcurves[(lightcurves['band'] == 'g') & (lightcurves['sid']==11)]])
i_band = np.array([lightcurves[(lightcurves['band'] == 'i') & (lightcurves['sid']==11)]])


# Reshape the band arrays to 2d arrays that are easier to handle.

r_band_2d = r_band.reshape(r_band.shape[1], r_band.shape[2])
g_band_2d = g_band.reshape(g_band.shape[1], g_band.shape[2])
i_band_2d = i_band.reshape(i_band.shape[1], i_band.shape[2])


font_path = '/Users/sam/Desktop/Uni/Y4/SHP/cmunrm.ttf'

fm.fontManager.addfont(font_path)

# Plot all three bands on one set of axes
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 12

plt.style.use('seaborn-v0_8-deep')

plt.plot(i_band_2d[:,1], i_band_2d[:,2], '-o', label='i band', markersize=2)
plt.plot(g_band_2d[:,1], g_band_2d[:,2], '-o', label='g band', markersize=2)
plt.plot(r_band_2d[:,1], r_band_2d[:,2], '-o', label='r band', markersize=2)
plt.xlabel('Modified Julian Date', fontsize=12)
plt.ylabel('Magnitude', fontsize=12)
ax = plt.gca()
ax.invert_yaxis()
#plt.ylim(22, 14)
#plt.xlim(58000, 60000)
plt.title(f'Lightcurve for uid {UIDS[0]}', fontsize=14)
plt.legend()
plt.show()


