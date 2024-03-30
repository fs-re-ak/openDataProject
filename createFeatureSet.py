
import os,sys
import numpy as np
import pandas as pd
from multiprocessing import freeze_support
from emgUtils import loadHermesSignals, showHermesBioSignals
from utils import printWarning, printError
from eventsUtils import loadTrialsEvents

from ExperimentsConstants import ExperimentsConstants
from HermesConstants import HermesConstants

REMOVE_WEAK_EXPRESSIONS = False
RMS_ACTIVE = True
INSPECT_RAW_SIGNALS = True

if __name__ == '__main__':

    # in case multiprocessing is needed
    freeze_support()

    #get all recordings
    recordings = os.listdir("dataset")

    # remove all recordings marked with a z (code to remove)
    recordings = [x for x in recordings if 'z' not in x]
    
    # weak recordings are identified with w
    if REMOVE_WEAK_EXPRESSIONS:
        recordings = [x for x in recordings if 'w' not in x]

    # unique trial id, just in case
    trialCounter = 1
    allValues = pd.DataFrame()

    # for all recordins
    for recording in recordings:

        print(recording)
        recPath = os.path.join("dataset", recording)

        # load rawdata
        emgSignals = loadHermesSignals(recPath)
        # load raw events
        events = loadTrialsEvents(recPath,showEvents=True)

        if INSPECT_RAW_SIGNALS:
            showHermesBioSignals(emgSignals,channels=[HermesConstants.CHANNEL_NAMES[0]], events=events)

        for event in events:

            for i in range(ExperimentsConstants.NB_WINDOWS):
                columnNames = []
                data = []

                # define sample window
                start = float(event[0] + i*ExperimentsConstants.SAMPLE_WINDOW_LENGTH)
                end = float(event[0] + (i+1)*ExperimentsConstants.SAMPLE_WINDOW_LENGTH)

                # compute active features and add to feature set
                if RMS_ACTIVE:
                    tmp = emgSignals[HermesConstants.CHANNEL_NAMES].loc[emgSignals['Timestamp'].between(start, end)]
                    rms = np.sqrt(np.mean(tmp.values ** 2, axis=0))
                    columnNames += [ x + "_RMS" for x in HermesConstants.CHANNEL_NAMES]
                    data += rms.tolist()

                # assemble dataframe
                data = np.array(data)
                samplesDf = pd.DataFrame(data=data.reshape((1, data.shape[0])), columns=columnNames)

                # complete meta information and add to the set
                samplesDf["Tag"] = event[2]
                samplesDf["Trial"] = trialCounter
                samplesDf["Recording"] = recording
                allValues = pd.concat([allValues, samplesDf], ignore_index=True)

            trialCounter += 1

    # compute stats (mean) for reference
    stats = allValues.groupby('Tag', as_index=False)[columnNames].mean()

    # save file
    allValues.to_csv(os.path.join("features","featuresDf.csv"),index=False)
    stats.to_csv(os.path.join("features","stats.csv"),index=False)