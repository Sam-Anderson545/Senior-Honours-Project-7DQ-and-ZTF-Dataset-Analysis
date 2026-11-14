
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager as fm
import requests


"""

Script to read downloaded, locally stored brand new ZTF light curve data and plot it, given a 7DQ UID.
List of 'good_uids' inputted manually, this is the list of UIDs for which data has been downloaded in all
R, G and I bands.

This script relies on data being stored locally, and the font used for the plots relies on a locally 
stored .ttf file. Alter the code for your individual system.

"""


UID = 158545

good_uids = [2062, 14459, 18750, 31605, 115831, 158545, 224700, 293123, 328144, 344453, 373000, 393937, 411524, 442282, 483900, 494232]


# Make sure the UID is one of those that data has been downloaded for:

if UID not in good_uids:
    raise ValueError("UID is not in the list of good UIDs")


# Handle cases of more than three files (only one so far is UID 393937):

if UID == 393937:

    r_band1 = f'/Users/sam/Desktop/Uni/Y4/SHP/New ZTF Data/ZTF_{UID}_R1.tbl'
    g_band1 = f'/Users/sam/Desktop/Uni/Y4/SHP/New ZTF Data/ZTF_{UID}_G1.tbl'
    i_band1 = f'/Users/sam/Desktop/Uni/Y4/SHP/New ZTF Data/ZTF_{UID}_I1.tbl'
    r_band2 = f'/Users/sam/Desktop/Uni/Y4/SHP/New ZTF Data/ZTF_{UID}_R2.tbl'
    g_band2 = f'/Users/sam/Desktop/Uni/Y4/SHP/New ZTF Data/ZTF_{UID}_G2.tbl'
    i_band2 = f'/Users/sam/Desktop/Uni/Y4/SHP/New ZTF Data/ZTF_{UID}_I2.tbl'

    r_matches1 = pd.read_csv(r_band1, usecols=[3, 4], skiprows=54, sep=r"\s+", header=None, names=["mjd", "mag"])
    g_matches1 = pd.read_csv(g_band1, usecols=[3, 4], skiprows=54, sep=r"\s+", header=None, names=["mjd", "mag"])
    i_matches1 = pd.read_csv(i_band1, usecols=[3, 4], skiprows=54, sep=r"\s+", header=None, names=["mjd", "mag"])

    r_matches2 = pd.read_csv(r_band2, usecols=[3, 4], skiprows=54, sep=r"\s+", header=None, names=["mjd", "mag"])
    g_matches2 = pd.read_csv(g_band2, usecols=[3, 4], skiprows=54, sep=r"\s+", header=None, names=["mjd", "mag"])
    i_matches2 = pd.read_csv(i_band2, usecols=[3, 4], skiprows=54, sep=r"\s+", header=None, names=["mjd", "mag"])

    r_matches = pd.concat([r_matches1, r_matches2], ignore_index=True)
    g_matches = pd.concat([g_matches1, g_matches2], ignore_index=True)
    i_matches = pd.concat([i_matches1, i_matches2], ignore_index=True)

    r_matches = r_matches.sort_values(by='mjd').reset_index(drop=True)
    g_matches = g_matches.sort_values(by='mjd').reset_index(drop=True)
    i_matches = i_matches.sort_values(by='mjd').reset_index(drop=True)


else:

    r_band = f'/Users/sam/Desktop/Uni/Y4/SHP/New ZTF Data/ZTF_{UID}_R.tbl'
    g_band = f'/Users/sam/Desktop/Uni/Y4/SHP/New ZTF Data/ZTF_{UID}_G.tbl'
    i_band = f'/Users/sam/Desktop/Uni/Y4/SHP/New ZTF Data/ZTF_{UID}_I.tbl'

    r_matches = pd.read_csv(r_band, usecols=[3, 4], skiprows=54, sep=r"\s+", header=None, names=["mjd", "mag"])
    g_matches = pd.read_csv(g_band, usecols=[3, 4], skiprows=54, sep=r"\s+", header=None, names=["mjd", "mag"])
    i_matches = pd.read_csv(i_band, usecols=[3, 4], skiprows=54, sep=r"\s+", header=None, names=["mjd", "mag"])






#########################################################
"""
Add in earlier data so longer term behaviour can be seen.
"""



if UID < 5000:
    URL = 'https://surveys.roe.ac.uk/al-web/7dq/data/merged/qsos/clean/lc_000000_005000.csv'
else:
    
    if UID % 5000 == 0:

        end = UID
        start = UID - 4999

    else:

        end = ((UID // 5000) + 1) * 5000
        start = end - 4999

    URL = f'https://surveys.roe.ac.uk/al-web/7dq/data/merged/qsos/clean/lc_{start:06d}_{end:06d}.csv'


#print(URL)

# Read the CSV file in chunks and record the rows that correspond to the 
# desired UID. The intermediate fix here has been to use 'verify=False', 
# however this carries risks that should perhaps be avoided.


response = requests.get(URL, verify=False, stream=True)
response.raise_for_status()

matches = []
for chunk in pd.read_csv(response.raw, usecols=['uid', 'mjd', 'mag', 'band', 'sid'], chunksize=100_000,):
    selected = chunk[(chunk['uid'] == UID)]
    if not selected.empty:
        matches.append(selected)

#print(matches)


# Concatenate data into a single DataFrame, and separate it into the 
# different bands.

lightcurves = pd.concat(matches, ignore_index=True)
r_band = lightcurves[(lightcurves['band'] == 'r') & (lightcurves['sid'].isin([2,3,5,7]))]
g_band = lightcurves[(lightcurves['band'] == 'g') & (lightcurves['sid'].isin([2,3,5,7]))]
i_band = lightcurves[(lightcurves['band'] == 'i') & (lightcurves['sid'].isin([2,3,5,7]))]

r_band = np.array([r_band['mjd'].values, r_band['mag'].values])
g_band = np.array([g_band['mjd'].values, g_band['mag'].values])
i_band = np.array([i_band['mjd'].values, i_band['mag'].values])


# Reshape the band arrays to 2d arrays that are easier to handle.

r_band_old = r_band.T
g_band_old = g_band.T
i_band_old = i_band.T

r_matches = r_matches.to_numpy()
g_matches = g_matches.to_numpy()
i_matches = i_matches.to_numpy()

r_band_all = np.vstack([r_band_old, r_matches])
g_band_all = np.vstack([g_band_old, g_matches])
i_band_all = np.vstack([i_band_old, i_matches])


#########################################################









font_path = '/Users/sam/Desktop/Uni/Y4/SHP/cmunrm.ttf'

fm.fontManager.addfont(font_path)

# Plot all three bands on one set of axes
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['CMU Serif', 'CMU Serif Roman']
plt.rcParams['font.size'] = 12

plt.style.use('seaborn-v0_8-deep')

plt.plot(i_band_all[:,0], i_band_all[:,1], '-o', label='i band', markersize=2)
plt.plot(g_band_all[:,0], g_band_all[:,1], '-o', label='g band', markersize=2)
plt.plot(r_band_all[:,0], r_band_all[:,1], '-o', label='r band', markersize=2)
plt.axvline(x=60019, color='gray', linestyle='--', linewidth=1)
plt.xlabel('Modified Julian Date', fontsize=12)
plt.ylabel('Magnitude', fontsize=12)
ax = plt.gca()
ax.invert_yaxis()
#plt.ylim(22, 14)
#plt.xlim(58000, 61100)
plt.title(f'Lightcurve for uid {UID}', fontsize=14)
plt.legend()
plt.show()





