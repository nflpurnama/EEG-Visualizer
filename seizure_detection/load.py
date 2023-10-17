import numpy as np
import pandas as pd

from os import remove
from pyedflib import EdfReader
from werkzeug.datastructures import FileStorage

from seizure_detection.filemanager import retrieveEdf

def data_load(file: FileStorage, selected_channels=[]):
  temp_file_path = retrieveEdf(file)
  # use the reader to get an EdfReader file
  f = EdfReader(temp_file_path)
  
  # get a list of the EEG channels
  if len(selected_channels) == 0:
    selected_channels = f.getSignalLabels()

  print(selected_channels)
  # get the names of the signals
  channel_names = f.getSignalLabels()
  # get the sampling frequencies of each signal
  channel_freq = f.getSampleFrequencies()

  # make an empty file of 0's
  sigbufs = np.zeros((f.getNSamples()[0],len(selected_channels)))
  # for each of the channels in the selected channels
  for i, channel in enumerate(selected_channels):
    # add the channel data into the array
    sigbufs[:, i] = f.readSignal(channel_names.index(channel))
  
  # turn to a pandas df and save a little space
  df = pd.DataFrame(sigbufs, columns = selected_channels).astype('float32')
  
  # get equally increasing numbers upto the length of the data depending
  # on the length of the data divided by the sampling frequency
  index_increase = np.linspace(0,
                                len(df)/channel_freq[0],
                                len(df), endpoint=False)

  # round these to the lowest nearest decimal to get the seconds
  seconds = np.floor(index_increase).astype('uint16')

  # make a column the timestamp
  df['Time'] = seconds

  # make the time stamp the index
  df = df.set_index('Time')

  # name the columns as channel
  df.columns.name = 'Channel'

  f.close()
  remove(temp_file_path)
  return df, channel_freq[0]