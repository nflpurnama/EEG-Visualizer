import pandas as pd
import numpy as np
from scipy.signal import welch
from pywt import wavedec

def bandpower(data, sf, band):
    band = np.asarray(band)
    low, high = band

    segment_size = (1 / low) * sf
    if segment_size > len(data):
        segment_size = len(data)
    freqs, psd = welch(data, 
                       sf, 
                    #    nperseg = (1 / low) * sf,
                       nperseg = segment_size,
                       scaling = 'density', 
                       axis=0,
                       )
    psd = pd.DataFrame(psd, index = freqs, columns = data.columns)
    idx_min = np.argmax(np.round(freqs) > low) - 1
    idx_max = np.argmax(np.round(freqs) > high)
    psd = psd.iloc[idx_min:idx_max,:]
    psd = psd.mean()
    
    return psd

def power_measures(data, sample_rate):
    bandpasses = [[[0.1,4],'power_delta'],
                  [[4,8],'power_theta'],
                  [[8,12],'power_alpha'],
                  [[12,30],'power_beta'],
                  [[30,60],'power_gamma']
                 ]
    
    welch_df = pd.DataFrame()
    for bandpass, freq_name in bandpasses:
        bandpass_data = bandpower(data, sample_rate, bandpass)
        bandpass_data.index = [freq_name]
        
        if welch_df.empty:
            welch_df = bandpass_data
        else:
            welch_df = pd.concat([welch_df, bandpass_data])
        
    welch_df = welch_df.T
    
    return welch_df

def power_measure_channels(data, sample_rate):
    welch_df = pd.DataFrame()
    for channel_name in data:
        channel_df = pd.DataFrame(power_measures(pd.DataFrame(data[channel_name]), sample_rate))
        channel_df['channel'] = channel_name
        channel_df.index.name = 'feature'
        channel_df = channel_df.set_index('channel', append=True)
        channel_df = channel_df.swaplevel()

        if welch_df.empty:
            print(channel_name)
            welch_df = channel_df
        else:
            welch_df = pd.concat([welch_df, channel_df])

    welch_df = welch_df.T
    return welch_df



def wavelet_decompose_channels(data, level):
    data.columns.name='channel'
    data_t = data.transpose()
    coeffs_list = wavedec(data_t.values, wavelet='db4', level=level)
    nums = list(range(1,level+1))
    names=[]
    for num in nums:
        names.append('D' + str(num))    
    names.append('A' + str(nums[-1]))

    names = names[::-1]  

    i = 0
    wavelets = pd.DataFrame()
    for i, array in enumerate(coeffs_list):
        level_df = pd.DataFrame(array)
        level_df.index = data.columns
        level_df['level'] = names[i]
        level_df= level_df.set_index('level', append=True)
        level_df=level_df.T
        wavelets = pd.concat([wavelets,level_df], axis=1, sort=True)

    wavelets = wavelets.sort_values(['channel', 'level'], axis=1)
    return wavelets



def minus_small(data):    
    min_val = data.min()
    data = data.subtract(min_val).add(1)
    return data

def log_sum(data):
    absolute_sums = data.sum()
    absolute_sums_minus = minus_small(absolute_sums)
    absolute_sums_log = absolute_sums_minus.apply(np.log)
    absolute_sums_log.index += '_LSWT'
    return absolute_sums_log

def reformat(data, feature_name):
  data.index = [feature_name+level for level in data.index]
  data.index.name = 'feature'
  data = pd.DataFrame(data.unstack()).T
  return data

def log_sum_channels(data):
  absolute_sums = data.abs().sum()
  absolute_sums = absolute_sums.unstack('channel')
  absolute_sums_minus = absolute_sums.apply(minus_small)
  absolute_sums_log = absolute_sums_minus.apply(np.log)
  absolute_sums_log = reformat(absolute_sums_log, 'LSWT_')
  return absolute_sums_log



def ave(data):
    mean_data = data.mean()
    mean_data.index += '_mean'
    return mean_data

def ave_channels(data):
  mean_data = data.mean()
  mean_data = mean_data.unstack('channel')
  mean_data = reformat(mean_data, 'Mean_')
  return mean_data



def mean_abs(data):
    mean_abs_data = data.abs().mean()
    mean_abs_data.index += '_mean_abs'
    return mean_abs_data

def mean_abs_channels(data):
  mean_abs_data = data.abs().mean()
  mean_abs_data = mean_abs_data.unstack('channel')
  mean_abs_data = reformat(mean_abs_data, 'Mean_Abs_')
  return mean_abs_data



def coeff_std(data):
    std_data = data.std()
    std_data.index += '_std'
    return std_data

def coeff_std_channels(data):
  std_data = data.std()
  std_data = std_data.unstack('channel')
  std_data = reformat(std_data, 'STD_')
  return std_data



def ratio(data):
    data = data.abs().mean()
    decimation_levels = list(data.index)

    ratio_data=pd.Series(index=data.index)
    for level_no in range(0, len(decimation_levels)):
        if level_no == 0:
            ratio_data.loc[decimation_levels[level_no]] = data.loc[decimation_levels[level_no]]/data.loc[decimation_levels[level_no+1]]

        elif level_no == len(decimation_levels)-1:
            ratio_data.loc[decimation_levels[level_no]] = data.loc[decimation_levels[level_no]]/data.loc[decimation_levels[level_no-1]]
        else:
            before = data.loc[decimation_levels[level_no-1]]
            after = data.loc[decimation_levels[level_no+1]]
            mean_data = (before+after)/2

            ratio_data.loc[decimation_levels[level_no]] = data.loc[decimation_levels[level_no]]/mean_data

    ratio_data.index += '_Ratio'
    return ratio_data


def ratio_channels(epoch_data):
  decimation_levels = list(epoch_data.index)
  ratio_data=pd.Series()
  for level_no in range(0, len(decimation_levels)):
    if level_no == 0:
      ratio_data[decimation_levels[level_no]] = epoch_data.loc[decimation_levels[level_no]]/epoch_data.loc[decimation_levels[level_no+1]]
    elif level_no == len(decimation_levels)-1:
      ratio_data[decimation_levels[level_no]] = epoch_data.loc[decimation_levels[level_no]]/epoch_data.loc[decimation_levels[level_no-1]]
    else:
      before = epoch_data.loc[decimation_levels[level_no-1]]
      after = epoch_data.loc[decimation_levels[level_no+1]]
      mean_data = (before+after)/2

      ratio_data[decimation_levels[level_no]] = epoch_data.loc[decimation_levels[level_no]]/mean_data

  ratio_data.index.name = 'features'
  return ratio_data