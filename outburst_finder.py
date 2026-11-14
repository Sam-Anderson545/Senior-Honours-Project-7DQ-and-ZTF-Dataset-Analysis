from urllib import response
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import time
from scipy import stats
import peak_tester
import requests


"""

Script for running the methods written in peak tester across the entire dataset, by
accessing it online (without downloading). The aim is to produce a list of UIDs of
quasars that may be in outburst, and save this list so that it can be referred back
to later.

"""


# Minimum difference in magnitude to consider a quasar as potentially in outburst
min_diff = 3.0


def main():

    
    uids, slopes, residuals = [], [], []

    filename = 'https://surveys.roe.ac.uk/al-web/7dq/data/merged/qsos/clean/lc_000000_005000.csv'
    
    start_time = time.time()





    with requests.Session() as session:
        
        uids_in_file, grad, residual = test_file(filename, session)
        uids.extend(uids_in_file)
        slopes.extend(grad)
        residuals.extend(residual)

        print('1 of 106 files processed')

        filename = 'https://surveys.roe.ac.uk/al-web/7dq/data/merged/qsos/clean/lc_005001_010000.csv'

        end = 0

        n = 1

        while end != 535000:
            

            uids_in_file, grad, residual = test_file(filename, session)
            uids.extend(uids_in_file)
            slopes.extend(grad)
            residuals.extend(residual)

            n += 1
            print(n, 'of 106 files processed')
            filename, end = next_file(filename)







    end_time = time.time()

    print(f'Total elapsed time: {end_time - start_time:.3f} seconds / {(end_time - start_time)/60:.3f} minutes')

    print(f'Number of UIDs in entire dataset: {len(uids)}')



    # Save the UIDs to a text file for later reference
    with open('uid_data.txt', 'w') as uid_data:
        uid_data.write('\n'.join(map(str, uids)))
    uid_data.close()

    
    # Save the slopes to a text file for later reference
    with open('slopes.txt', 'w') as slopesList:
        slopesList.write('\n'.join(map(str, slopes)))
    slopesList.close()

    
    # Save the residuals to a text file for later reference
    with open('residuals.txt', 'w') as resiList:
        resiList.write('\n'.join(map(str, residuals)))
    resiList.close()
    

    #test_file('https://surveys.roe.ac.uk/al-web/7dq/data/merged/qsos/clean/lc_000000_005000.csv')
    


    



def test_file(filename, session):

    """
    Function to run the peak_tester methods on a single file, so that this method can then be called on each 
    file in the database.

    Inputs:
    - filename: str, the name of the file to be tested.
    - session: requests.Session object, to maintain a persistent connection to the server.

    Outputs:
    - uids: np.array, the unique UIDs of quasars that may be in outburst, across all bands.
    For linear and polynomial regression, the following should also be returned (for bin_regress, only residuals):
    - slopes: np.array. For a linear regression, the gradient. For a polynomial regression, the 
      coefficient of the highest order term.
    - residuals: np.array. For a linear regression, the r-value. For a polynomial regression, the
      residuals of the fit. For bin_regress, the r-value of the linear regression.
    """

    response = session.get(filename, verify=False, stream=True)
    response.raise_for_status()


    data = pd.read_csv(response.raw, usecols=['uid', 'mjd', 'mag', 'band', 'sid'])

    

    # Filter out anomalous light curves and those with too few data points:
    
    remove_uids = [2062, 14459, 18750, 31605, 115831, 158545, 328144, 344453, 373000, 393937, 411524, 442282, 494232]
    for uid, quasar_data in data.groupby('uid'):
        too_few_points = len(quasar_data[quasar_data['sid'] == 11]) < 40
        anomalous = peak_tester.anomaly(quasar_data)

        if too_few_points or anomalous:
            remove_uids.append(uid)


    new_data = data[~data['uid'].isin(remove_uids)]


    r_uids, g_uids, i_uids = peak_tester.in_outburst2(new_data, min_diff=min_diff)

    # Filter the data to only include the desired UIDs
    mag_diff_data_r = new_data[new_data['uid'].isin(r_uids) & (new_data['band'] == 'r')]
    mag_diff_data_g = new_data[new_data['uid'].isin(g_uids) & (new_data['band'] == 'g')]
    mag_diff_data_i = new_data[new_data['uid'].isin(i_uids) & (new_data['band'] == 'i')]


    new_r_uids, new_g_uids, new_i_uids = [], [], []



    
    # Multiple criteria method:
    """
    for uid, quasar_data in mag_diff_data_r.groupby('uid'):
        UID = [uid]
        good_uid, r_val = peak_tester.bin_regress(quasar_data, UID, min_rs=4, bins=10)
        #new_r_uids, r_slopes, r_rvalues = peak_tester.lin_regress(quasar_data, uid)
        #new_r_uids, r_rvalues = peak_tester.bin_regress(quasar_data, uid, min_rs=3, bins=5)
        if len(good_uid) > 0:
            new_r_uids.append(good_uid[0])
            #r_rvalues.append(r_val[0])
        else:
            good_uid, slope, r_val = peak_tester.lin_regress(quasar_data, UID)
            if len(good_uid) > 0:
                new_r_uids.append(good_uid[0])
                #r_slopes.append(slope[0])
                #r_rvalues.append(r_val[0])
            else:
                good_uid, r_val = peak_tester.bin_regress(quasar_data, UID, min_rs=3, bins=5)
                if len(good_uid) > 0:
                    new_r_uids.append(good_uid[0])
                    #r_rvalues.append(r_val[0])





    for uid, quasar_data in mag_diff_data_g.groupby('uid'):
            UID = [uid]
            good_uid, r_val = peak_tester.bin_regress(quasar_data, UID, min_rs=4, bins=10)
            #new_r_uids, r_slopes, r_rvalues = peak_tester.lin_regress(quasar_data, uid)
            #new_r_uids, r_rvalues = peak_tester.bin_regress(quasar_data, uid, min_rs=3, bins=5)
            if len(good_uid) > 0:
                new_g_uids.append(good_uid[0])
                #r_rvalues.append(r_val[0])
            else:
                good_uid, slope, r_val = peak_tester.lin_regress(quasar_data, UID)
                if len(good_uid) > 0:
                    new_g_uids.append(good_uid[0])
                    #r_slopes.append(slope[0])
                    #r_rvalues.append(r_val[0])
                else:
                    good_uid, r_val = peak_tester.bin_regress(quasar_data, UID, min_rs=3, bins=5)
                    if len(good_uid) > 0:
                        new_g_uids.append(good_uid[0])
                        #r_rvalues.append(r_val[0])





    for uid, quasar_data in mag_diff_data_i.groupby('uid'):
            UID = [uid]
            good_uid, r_val = peak_tester.bin_regress(quasar_data, UID, min_rs=4, bins=10)
            #new_r_uids, r_slopes, r_rvalues = peak_tester.lin_regress(quasar_data, uid)
            #new_r_uids, r_rvalues = peak_tester.bin_regress(quasar_data, uid, min_rs=3, bins=5)
            if len(good_uid) > 0:
                new_i_uids.append(good_uid[0])
                #r_rvalues.append(r_val[0])
            else:
                good_uid, slope, r_val = peak_tester.lin_regress(quasar_data, UID)
                if len(good_uid) > 0:
                    new_i_uids.append(good_uid[0])
                    #r_slopes.append(slope[0])
                    #r_rvalues.append(r_val[0])
                else:
                    good_uid, r_val = peak_tester.bin_regress(quasar_data, UID, min_rs=3, bins=5)
                    if len(good_uid) > 0:
                        new_i_uids.append(good_uid[0])
                        #r_rvalues.append(r_val[0])


    """

    



    # Binned linear regression:
    """
    new_r_uids, r_rvalues = peak_tester.bin_regress(mag_diff_data_r, r_uids, bins=10)
    new_g_uids, g_rvalues = peak_tester.bin_regress(mag_diff_data_g, g_uids, bins=10)
    new_i_uids, i_rvalues = peak_tester.bin_regress(mag_diff_data_i, i_uids, bins=10)
    """

    
    # Linear regression:
    
    new_r_uids, r_slopes, r_rvalues = peak_tester.lin_regress(mag_diff_data_r, r_uids)
    new_g_uids, g_slopes, g_rvalues = peak_tester.lin_regress(mag_diff_data_g, g_uids)
    new_i_uids, i_slopes, i_rvalues = peak_tester.lin_regress(mag_diff_data_i, i_uids)
    

    
    # Polynomial regression:
    """
    degree = 2
    new_r_uids, r_slopes, r_residuals = peak_tester.poly_regress(mag_diff_data_r, r_uids, degree=degree)
    new_g_uids, g_slopes, g_residuals = peak_tester.poly_regress(mag_diff_data_g, g_uids, degree=degree)
    new_i_uids, i_slopes, i_residuals = peak_tester.poly_regress(mag_diff_data_i, i_uids, degree=degree)
    """

    
    uids = np.unique(np.concatenate((new_r_uids, new_g_uids, new_i_uids)))
    #print(f'Number of unique UIDs across all bands: {len(uids)}')
    #print(uids)

    """
    residuals = []
    residuals.extend(r_residuals)
    residuals.extend(g_residuals)
    residuals.extend(i_residuals)
    """
    """
    residuals = []
    residuals.extend(r_rvalues)
    residuals.extend(g_rvalues)
    residuals.extend(i_rvalues)
    """
    """
    slopes = []
    slopes.extend(r_slopes)
    slopes.extend(g_slopes)
    slopes.extend(i_slopes)
    """

    return uids, [], []
    



def next_file(filename):
    
    """
    Function to generate the next filename based on the previous one, i.e.,
    add 5000 to the start and end of the filename.

    Inputs:
    - filename: str, the name of the previous file.
    
    Outputs:
    - next_filename: str, the name of the next file.
    - end: int, the end number of the next file.
    """



    base = 'https://surveys.roe.ac.uk/al-web/7dq/data/merged/qsos/clean/lc_'

    start = int(filename.split('_')[-2])
    end = int(filename.split('_')[-1].split('.')[0])


    next_start = start + 5000
    next_end = end + 5000



    next_filename = f'{base}{next_start:06d}_{next_end:06d}.csv'
    #print(f'Next filename: {next_filename}')

    return next_filename, next_end




     

if __name__ == '__main__':
    main()


