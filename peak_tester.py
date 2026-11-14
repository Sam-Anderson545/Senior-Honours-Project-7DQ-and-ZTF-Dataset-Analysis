import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import time
import requests
from scipy import stats



"""

Script of functions for identifying quasars that may be 'in outburst' based on lightcurve data. 
Includes two versions of functions for finding the difference between max and min magnitude of 
quasars, and a function to do a linear regression to describe the light curve, in order to 
indentify possible outbursts. Also added polynomial regression function, binned regression 
function and function for filtering out anomalous light curves.

"""


# First approach will be to take this one file at a time, i.e., manually select
# the lightcurve file, read it in, and select the quasars that appear to be 
# peaking. If this works well I can create another file and import the methods
# from this file into that second file, and hopefully also access the dataset
# online without having to download it. This is the ideal pipeline.



def main():

    """
    start = time.time()
    r_uids, g_uids, i_uids = in_outburst2(data, min_diff=2.0)

    mag_diff_data_r = data[data['uid'].isin(r_uids) & (data['band'] == 'r')]
    mag_diff_data_g = data[data['uid'].isin(g_uids) & (data['band'] == 'g')]
    mag_diff_data_i = data[data['uid'].isin(i_uids) & (data['band'] == 'i')]
    new_r_uids, r_slopes, r_pvalues = lin_regress(mag_diff_data_r, r_uids)
    new_g_uids, g_slopes, g_pvalues = lin_regress(mag_diff_data_g, g_uids)
    new_i_uids, i_slopes, i_pvalues = lin_regress(mag_diff_data_i, i_uids)
    end = time.time()

    print(f'Elapsed time: {end - start:.3f} seconds')
    #print(r_uids)
    #print(f'Number of r band UIDs: {len(new_r_uids)}')
    #print(f'Number of g band UIDs: {len(new_g_uids)}')
    #print(f'Number of i band UIDs: {len(new_i_uids)}')

    #print(new_uids[0])
    #print(slopes[0])


    uids = np.unique(np.concatenate((new_r_uids, new_g_uids, new_i_uids)))
    print(f'Number of unique UIDs across all bands: {len(uids)}')
    print(uids)
    """

    UIDS = [328144]


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


    #print(f'URL: {URL}')
    """
    response = requests.get(URL, verify=False, stream=True)
    response.raise_for_status()

    matches = []
    for chunk in pd.read_csv(response.raw, usecols=['uid', 'mjd', 'mag', 'band', 'sid'], chunksize=100_000,):
        selected = chunk[(chunk['uid'].isin(UIDS))]
        if not selected.empty:
            matches.append(selected)
    """


    response = requests.get(URL, verify=False, stream=True)
    response.raise_for_status()


    data = pd.read_csv(response.raw, usecols=['uid', 'mjd', 'mag', 'band', 'sid'])


    print(anomaly(data[data['uid'] == UIDS[0]]))


    
    """
    for uid in data['uid'].unique():
        if in_outburst([uid]):
            uids.append(uid)
    """


    """
    uid = 405001

    if in_outburst1([uid]):
        uids.append(uid)

    end = time.time()
    print(f'Elapsed time: {end - start:.2f} seconds')
    """

    """
    start = time.time()

    for uid in range(min_uid, max_uid + 1):
        if in_outburst1([uid]):
            uids.append(uid)

    #print(uids)

    end = time.time()
    print(f'Elapsed time: {end - start:.2f} seconds')

    """







def in_outburst1(UID, min_diff=2.0):

    """
    Function to test if a quasar is in outburst, by reading the csv file. Note this function is no longer used since 
    the function below, in_outburst2, is a better, more efficent version.

    NB: this function is more or less obsolete now that Copilot has written a 
    vastly more efficient version, run as in_outburst2.

    Inputs:
    - UID: the uid of the object being considered.
    - min_diff: the minimum magnitude difference that will be taken as an
      indication of an outburst.

    Outputs:
    - True or False: indicating where the quasar appears to be in outburst or not.
    """


    matches = []
    for chunk in pd.read_csv('/Users/sam/Desktop/Uni/Y4/SHP/lc_405001_410000.csv', usecols=['uid', 'mjd', 'mag', 'band', 'sid'], chunksize=100_000):
        selected = chunk[chunk['uid'].isin(UID)]
        if not selected.empty:
            matches.append(selected)


    matches = np.array(matches)


    if matches[:,:,2].max() - matches[:,:,2].min() > min_diff:
        return True
    else:
        return False
    




def in_outburst2(data, min_diff=2.0):
    
    """
    Function to extract which of the quasars in a given dataset are in outburst by finding the difference between the maximum and minimum magnitude 
    of each quasar, and comparing it to a threshold value.

    Inputs:
    - data: a pandas dataframe containing the lightcurve data for the quasars
      being considered.
    - min_diff: the minimum magnitude difference that will be taken as an
      indication of an outburst.

    Outputs:
    - r_uids: a list of the uids of the quasars that appear to be in outburst in 
      r band.
    - g_uids: a list of the uids of the quasars that appear to be in outburst in
      g band.
    - i_uids: a list of the uids of the quasars that appear to be in outburst in
      i band.
    """



    """
    The below lines were largely written by me. They are likely slower and 
    less efficient than the lines lower down, which were written entirely by Copilot.
    

    uids = []

    data = np.array(data)

    for uid in np.unique(data[:,0]):
        selected = data[data[:,0] == uid]

        if selected[:,2].max() - selected[:,2].min() > min_diff:
            uids.append(uid)

    return uids
    """


    """
    The below few lines are a far more efficient way of writing the in_outburst2 
    function, given by Copilot.
    """

    """
    # This code written before I had separated lightcurve data into bands.
    ranges = data.groupby("uid")["mag"].agg(["min", "max"])
    return ranges.index[
        ranges["max"] - ranges["min"] > min_diff
    ].tolist()
    """

    """
    # The below lines run the algorithm for all data, regardless of the survery of
    # origin.
    r_band = [data[data['band'] == 'r']]
    g_band = [data[data['band'] == 'g']]
    i_band = [data[data['band'] == 'i']]
    """


    # The below three lines run the algorithm only for the ZTF data, identified
    # by the 'survey ID' (sid) number 11.
    r_band = [data[(data['band'] == 'r') & (data['sid'] == 11)]]
    g_band = [data[(data['band'] == 'g') & (data['sid'] == 11)]]
    i_band = [data[(data['band'] == 'i') & (data['sid'] == 11)]]

    r_ranges = r_band[0].groupby("uid")["mag"].agg(["min", "max"])
    g_ranges = g_band[0].groupby("uid")["mag"].agg(["min", "max"])
    i_ranges = i_band[0].groupby("uid")["mag"].agg(["min", "max"])

    r_uids = r_ranges.index[
        r_ranges["max"] - r_ranges["min"] > min_diff
    ].tolist()

    g_uids = g_ranges.index[
        g_ranges["max"] - g_ranges["min"] > min_diff
    ].tolist()

    i_uids = i_ranges.index[
        i_ranges["max"] - i_ranges["min"] > min_diff
    ].tolist()

    return r_uids, g_uids, i_uids






def lin_regress(min_diff_data, uids):
   
    """
    Function to do a linear regression on the lightcurve data for a set of quasars, and 
    return a list of the uids of the quasars for which the regression is significant.
    This function is intended to be used after the in_outburst2 function.

    Inputs:
    - min_diff_data: the data frame containing lightcurve data for the quasars that have
      a minimum magnitude difference greater than the threshold.
    - uids: a list of the uids of the quasars to be considered.

    Outputs:
    - new_uids: a list of the uids of the quasars for which the linear regression is significant.
    - slopes: a list of the gradients of the linear regression for each quasar.
    - pvalues: a list of the p-values of the linear regression for each quasar.
    """

    new_uids, slopes, pvalues, rvalues = [], [], [], []

    for uid in uids:
        selected = min_diff_data[min_diff_data['uid'] == uid]
        x = selected['mjd']
        y = selected['mag']

        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)


        # The criteria for determining signs of outburst:

        if p_value < 1.0e-10 and slope < 0:
                new_uids.append(uid)
                slopes.append(slope)
                rvalues.append(p_value)


            
    return new_uids, slopes, rvalues



def poly_regress(min_diff_data, uids, degree=2):

    """
    Function to do a polynomial regression on the lightcurve data for a set of quasars, and 
    return a list of the uids of the quasars for which the regression is significant.
    This function is intended to be used after the in_outburst2 function.

    Inputs:
    - min_diff_data: the data frame containing lightcurve data for the quasars that have
      a minimum magnitude difference greater than the threshold.
    - uids: a list of the uids of the quasars to be considered.
    - degree: the degree of the polynomial to fit.

    Outputs:
    - new_uids: a list of the uids of the quasars for which the polynomial regression is significant.
    - coeffns: a list of the polynomial coefficients of the regression for each quasar.
    - residuals: a list of the residuals of the polynomial regression for each quasar.
    """

    new_uids = []
    coeffns = []
    residuals = []

    for uid in uids:
        selected = min_diff_data[min_diff_data['uid'] == uid]
        x = selected['mjd']
        y = selected['mag']

        coeffs, residual, rank, s, rcond = np.polyfit(x, y, degree, full=True)

        # The current criterion for selecting quasars that may be in outburst is that the 
        # polynomial regression has a negative leading coefficient, indicating that the 
        # quasar is increasing in luminosity.

        if abs(coeffs[0]) > 1e-7:
            new_uids.append(uid)
            coeffns.append(coeffs)
            residuals.append(residual)


    return new_uids, coeffns, residuals





def bin_regress(mag_diff_data, UIDS, min_rs=3, bins=5):


    """
    Function to take the data reduced by minimum magnitude difference, and bin it into a given number of bins, 
    then perform a linear regression on each bin. This function could perhaps be made more efficient, but this 
    is not a priority at the moment.
    
    Inputs:
    - mag_diff_data: the data reduced by minimum magnitude difference, for a single band (either R, G, or I).
    - bins: int, the number of bins to use for the binning.
    - min_rs: int, the minimum number of r values that must be less than -0.2 for a quasar to be considered in outburst.
    - UIDS: np.array, the UIDs of quasars to consider.

    Outputs:
    - new_uids: np.array, the unique UIDs of quasars that may be in outburst, across all bands.
    - r_values: np.array, the r-values of the linear regression for each UID.
    """

    new_uids = []
    p_values = []

    for uid in UIDS:

        selected = mag_diff_data[mag_diff_data['uid'] == uid]
        # Create bin edges:
        min_mjd = selected['mjd'].min()
        max_mjd = selected['mjd'].max()
        bin_edges = np.linspace(min_mjd, max_mjd, bins + 1)

        # Bin the data
        """
        bin1 = selected[(selected['mjd'] >= bin_edges[0]) & (selected['mjd'] < bin_edges[1])]
        bin2 = selected[(selected['mjd'] >= bin_edges[1]) & (selected['mjd'] < bin_edges[2])]
        bin3 = selected[(selected['mjd'] >= bin_edges[2]) & (selected['mjd'] < bin_edges[3])]
        bin4 = selected[(selected['mjd'] >= bin_edges[3]) & (selected['mjd'] < bin_edges[4])]
        bin5 = selected[(selected['mjd'] >= bin_edges[4]) & (selected['mjd'] <= bin_edges[5])]
        """

        binned_data = [selected[(selected['mjd'] >= bin_edges[i]) & (selected['mjd'] < bin_edges[i + 1])] for i in range(bins)]

        # Compute mean magnitude in each bin
        mean_mags = [binned_data[i]['mag'].mean() if not binned_data[i].empty else np.nan for i in range(bins)]

        # Perform linear regression on each bin
        results = []
        for i in range(len(binned_data)):
            bin_data = binned_data[i]
            if len(bin_data) > 1:
                slope, intercept, r_value, p_value, std_err = stats.linregress(bin_data['mjd'], bin_data['mag'])
                results.append((i, slope, intercept, r_value, p_value, std_err))


        slopes = [results[i][1] for i in range(len(results))]
        r_values = [results[i][3] for i in range(len(results))]
        
        
        n = 0

        # if mean_mags[-3] < mean_mags[-4] < mean_mags[-5]:

        for i in range(len(r_values)):
            if r_values[i] < -0.2:
                n += 1

        if n >= min_rs:
            new_uids.append(uid)
            r_values.append(r_values)






        """
        for i in range(len(r_values)):
            if r_values[i] < -0.2:
                n += 1

        if n >= 4:
            new_uids.append(uid)
            r_values.append(r_values)
        """
        
        """
        # Check if the mean magnitudes are decreasing over the last three bins
        if mean_mags[-1] < mean_mags[-2] < mean_mags[-3]:
            new_uids.append(uid)
        """

    if len(new_uids) == 0:
        return np.array([]), np.array([])
    else:
        return new_uids, r_values
    

        """ 
        if all(slopes[i] < 0 for i in range(len(slopes))):
            new_uids.append(uid)

        if all(slopes[i] > 0 for i in range(len(slopes))):
            return
        """

        

def anomaly(data):

    """
    Function to find the light curves that sit very uniformly at a particular magnitude, but have one outlier
    of significantly higher luminosity outisde the general trend. These quasars are interfering with the data 
    analysis and should be removed from the dataset.
    At least for now, the idea is to use this function before the minimum magnitude difference function.

    Inputs:
    - data: a pandas dataframe containing the lightcurve data for one quasar.

    Outputs:
    - True or False: indicating whether the quasar appears to have an anomalous data point.
    """

    # Find the mean and standard deviation of the magnitudes
    mean = data['mag'].mean()
    std = data['mag'].std()

    #print(f'Mean: {mean}, Standard Deviation: {std}')

    n = 0
    for i in data['mag']:
        #print(i)
        if abs(i - mean) > (7 * std):
            n += 1

    #print(n)

    if n == 1:
        return True
    else:
        return False









if __name__ == "__main__":
    main()


