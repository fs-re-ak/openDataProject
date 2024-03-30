
import os, sys
import csv
import numpy as np
import pandas as pd
from utils import detectAndBuildFilename, printError
from scipy.signal import lfilter, butter
import matplotlib.pyplot as plt

from HermesConstants import HermesConstants

FILTER_ORDER = 4
FCs_BANDPASS = np.array([1, 45])


def loadHermesSignals(recPath):
    """
    Loads hermes biosignals, which is a 2d array of floats, in
    which the first column are the timestamps and the remaining columns
    are the biosignals.

    NOTE: eeg.tmp is a legacy name, it contains all biosignals recorded
    through the electrodes.

    :param recPath: path of the recording
    :return: pandas array containing the emg signals
    """

    # build and validate filename
    filenameCandidates = ["eeg.tmp"]
    filePath = os.path.join(recPath, "rawData")
    filename = detectAndBuildFilename(filePath,filenameCandidates)

    if filename is None:
        printError(f'[emgUtils.py] No valid Biosignals files found {recPath}')
        return None

    # load and preprocess emg signals
    emgData = np.genfromtxt(filename, delimiter=",")
    emgData[:, 1:] = conditionEMG(emgData[:, 1:])

    return pd.DataFrame(data=emgData, columns=["Timestamp"] + HermesConstants.CHANNEL_NAMES)


def conditionEMG(samples, fs=250, bandpassFcs=FCs_BANDPASS, filterOrder=FILTER_ORDER):
    """
    This function process EMG signals using a set of two filters. The lfilter
    was selected, because it can be used in real-time application as well.

    We found that 2-stage filters is more stable than a 1-stage, with twice the order.

    :param samples: numpy array MxN, where M are the observations and N the channels
    :param fs: sampling rate (default 250Hz)
    :param bandpassFcs: numpy array 1x2 containing the low and high FCs of the bandpass filter (default 15-45Hz)
    :param filterOrder: ordre of the two-stage filter, (default 4)
    :return:
    """

    b, a = butter(filterOrder, bandpassFcs / (fs / 2), btype='bandpass')

    for i in range(samples.shape[1]):
        samples[:, i] = lfilter(b, a, samples[:, i])
        samples[:, i] = lfilter(b, a, samples[:, i])

    return samples
        

def showHermesBioSignals(emg_df, channels=HermesConstants.CHANNEL_NAMES, events=None):
    """
    Function that shows the signals of the Hermes (stored in dataframe) on
    by one for validation purpose.

    :param emg_df: dataframe containing the biosignals of the Hermes
    :param channels: channels to show (default: all)
    :param events: if events are provided, each event will be added as a vertical line
    :return: None
    """

    for channel in channels:
        plt.plot(emg_df["Timestamp"],emg_df[channel])
        plt.title(channel)

        if events is not None:
            for event in events:
                plt.vlines(event[0], emg_df[channel].min(), emg_df[channel].max())
                plt.text(event[0], 0, event[2])

        plt.show()
