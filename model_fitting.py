from urllib import response
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import time
from scipy import stats
import peak_tester
import requests
from scipy.optimize import curve_fit
from matplotlib import font_manager as fm

"""
Code for finding optimal values of parameters to model outburst behaviour, either as microlensing or
some other thing.
Based on equations from Grieve 2025.

Note this code relies on locally stored files at many points. Change the specified file paths
as appropriate for your system.
"""

"""
# Online data without newest ZTF stuff
UIDS = [442282]

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

# Read the CSV file in chunks and record the rows that correspond to the 
# desired UID. The intermediate fix here has been to use 'verify=False', 
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
r_band = np.array([lightcurves[lightcurves['band'] == 'r']])
g_band = np.array([lightcurves[lightcurves['band'] == 'g']])
i_band = np.array([lightcurves[lightcurves['band'] == 'i']])

# Reshape the band arrays to 2d arrays that are easier to handle.

r_band_2d = r_band.reshape(r_band.shape[1], r_band.shape[2])
g_band_2d = g_band.reshape(g_band.shape[1], g_band.shape[2])
i_band_2d = i_band.reshape(i_band.shape[1], i_band.shape[2])

r_band_2d = r_band_2d[np.argsort(r_band_2d[:, 1])]
g_band_2d = g_band_2d[np.argsort(g_band_2d[:, 1])]
i_band_2d = i_band_2d[np.argsort(i_band_2d[:, 1])]
"""






UID = 442282

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






r_data = np.array([r_matches])
g_data = np.array([g_matches])
i_data = np.array([i_matches])


r_band_2d = r_data.reshape(r_data.shape[1], r_data.shape[2])
g_band_2d = g_data.reshape(g_data.shape[1], g_data.shape[2])
i_band_2d = i_data.reshape(i_data.shape[1], i_data.shape[2])


all_bands = np.concatenate((r_band_2d, g_band_2d, i_band_2d), axis=0)
all_bands = all_bands[np.argsort(all_bands[:, 0])]

"""
plt.plot(all_bands[:,0], all_bands[:,1], '-o', label='all bands', markersize=2)
ax = plt.gca()
ax.invert_yaxis()
plt.show()
"""


"""
r_band_2d = r_band_2d[np.argsort(r_band_2d[:, 0])]
g_band_2d = g_band_2d[np.argsort(g_band_2d[:, 0])]
i_band_2d = i_band_2d[np.argsort(i_band_2d[:, 0])]
"""

"""
font_path = '/Users/sam/Desktop/Uni/Y4/SHP/cmunrm.ttf'

fm.fontManager.addfont(font_path)

# Plot all three bands on one set of axes
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['CMU Serif', 'CMU Serif Roman']

plt.style.use('seaborn-v0_8-deep')

plt.plot(i_matches.values[:,0], i_matches.values[:,1], '-o', label='i band', markersize=2)
plt.plot(g_matches.values[:,0], g_matches.values[:,1], '-o', label='g band', markersize=2)
plt.plot(r_matches.values[:,0], r_matches.values[:,1], '-o', label='r band', markersize=2)
plt.xlabel('Modified Julian Date', fontsize=12)
plt.ylabel('Magnitude', fontsize=12)
ax = plt.gca()
ax.invert_yaxis()
#plt.ylim(22, 14)
#plt.xlim(58000, 60000)
plt.title(f'Lightcurve for uid {UID}', fontsize=14)
plt.legend()
plt.show()
"""





def mufunc(t, y0, t0, te, c):

    """
    The mu(t) function.

    Inputs:
    - t: time
    - y0: the impact parameter
    - t0: the midpoint epoch
    - te: the Einstein radius crossing time
    - c: a constant offset

    Outputs:
    - mu(t): the magnification as a function of time
    """


    return -2.5 * np.log10((yfunc(t, y0, t0, te)**2 + 2)/(yfunc(t, y0, t0, te) * np.sqrt(yfunc(t, y0, t0, te)**2 + 4))) + c



def yfunc(t, y0, t0, te):

    """
    The y(t) function.

    Inputs:
    - t: time
    - y0: the impact parameter
    - t0: the midpoint epoch
    - te: the Einstein radius crossing time

    Outputs:
    - y(t): the impact parameter as a function of time
    """

    return np.sqrt((y0**2 + (((t-t0))/te)**2))




start_guess = [0.1, 59500, 100, 20]
bounds = ([0, 57000, 0, -np.inf], [4, 61000, np.inf, np.inf])


##########################################

"""
total_curve = pd.concat([r_matches, g_matches, i_matches], ignore_index=True)
total_curve = total_curve.sort_values(by='mjd').reset_index(drop=True)
"""

params, covariance = curve_fit(mufunc, all_bands[:,0], all_bands[:,1], p0=start_guess, bounds=bounds)

print(f'Variance output: {np.diag(covariance)}')

"""
plt.plot(all_bands[:,0], all_bands[:,1], '-o', label='all bands', markersize=2)
ax = plt.gca()
ax.invert_yaxis()
plt.plot(all_bands[:,0], mufunc(all_bands[:,0], *params), 'k--', label='Best Fit Line', linewidth=1.5)
plt.xlabel('Modified Julian Date', fontsize=12)
plt.ylabel('Magnitude', fontsize=12)
plt.title(f'Lightcurve for uid {UID}', fontsize=14)
plt.legend()
plt.show()
"""


mid_epo = params[1]


def yfunc2(t, y0, te):

    """
    The y(t) function.

    Inputs:
    - t: time
    - y0: the impact parameter
    - te: the Einstein radius crossing time

    Outputs:
    - y(t): the impact parameter as a function of time
    """

    return np.sqrt((y0**2 + (((t-mid_epo))/te)**2))


def mufunc2(t, y0, te, c):

    """
    The mu(t) function when the midpoint epoch has already been found.

    Inputs:
    - t: time
    - y0: the impact parameter
    - te: the Einstein radius crossing time
    - c: a constant offset

    Outputs:
    - mu(t): the magnification as a function of time
    """


    return -2.5 * np.log10((yfunc2(t, y0, te)**2 + 2)/(yfunc2(t, y0, te) * np.sqrt(yfunc2(t, y0, te)**2 + 4))) + c


start_guess = [0.1, 100, 20]
bounds = ([0, -np.inf, -np.inf], [4, np.inf, np.inf])


r_params, r_covariance = curve_fit(mufunc2, r_matches.values[:,0], r_matches.values[:,1], p0=start_guess, bounds=bounds)
g_params, g_covariance = curve_fit(mufunc2, g_matches.values[:,0], g_matches.values[:,1], p0=start_guess, bounds=bounds)
i_params, i_covariance = curve_fit(mufunc2, i_matches.values[:,0], i_matches.values[:,1], p0=start_guess, bounds=bounds)



##########################################

"""
r_params, r_covariance = curve_fit(mufunc, r_matches.values[:,0], r_matches.values[:,1], p0=start_guess, bounds=bounds)
g_params, g_covariance = curve_fit(mufunc, g_matches.values[:,0], g_matches.values[:,1], p0=start_guess, bounds=bounds)
i_params, i_covariance = curve_fit(mufunc, i_matches.values[:,0], i_matches.values[:,1], p0=start_guess, bounds=bounds)


print(f'variance for r band: {np.diag(r_covariance)}')
print(f'variance for g band: {np.diag(g_covariance)}')
print(f'variance for i band: {np.diag(i_covariance)}')
"""

time_data = np.linspace(58000, 61000, 1000)

"""
r_curve = []
for t in time_data:
    r_curve.append(mufunc(t, *r_params))

g_curve = []
for t in time_data:
    g_curve.append(mufunc(t, *g_params))

i_curve = []
for t in time_data:
    i_curve.append(mufunc(t, *i_params))
"""

#print(i_curve)

#print(f'r_params: {r_params}')
#print(f'g_params: {g_params}')




font_path = '/Users/sam/Desktop/Uni/Y4/SHP/cmunrm.ttf'

fm.fontManager.addfont(font_path)

# Plot all three bands on one set of axes
plt.rcParams['font.family'] = 'serif'
#plt.rcParams['font.serif'] = ['CMU Serif', 'CMU Serif Roman']
plt.rcParams['font.size'] = 12

plt.style.use('seaborn-v0_8-deep')

#print(len(i_matches.values[:,0]))


plt.scatter(i_matches.values[:,0], i_matches.values[:,1], label='i band', s=9)
plt.scatter(g_matches.values[:,0], g_matches.values[:,1], label='g band', s=9)
plt.scatter(r_matches.values[:,0], r_matches.values[:,1], label='r band', s=9)
#plt.plot(i_matches.values[:,0], i_curve, label='i band fit', color='blue')
#plt.plot(g_matches.values[:,0], g_curve, label='g band fit', color='green')
#plt.plot(r_matches.values[:,0], r_curve, label='r band fit', color='red')
plt.plot(time_data, mufunc2(time_data, *r_params), label='R fit', color='red')
plt.plot(time_data, mufunc2(time_data, *g_params), label='G fit', color='green')
plt.plot(time_data, mufunc2(time_data, *i_params), label='I fit', color='blue')
plt.xlabel('Modified Julian Date', fontsize=12)
plt.ylabel('Magnitude', fontsize=12)
ax = plt.gca()
ax.invert_yaxis()
#plt.ylim(22, 14)
#plt.xlim(58000, 60000)
plt.title(f'Lightcurve for uid {UID}', fontsize=14)
plt.legend()
plt.show()



