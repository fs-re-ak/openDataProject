
import os, sys
import csv
from utils import detectAndBuildFilename

def loadTrialsEvents(recPath, removeBlinks=True, showEvents=False):
    """
        This function loads the trials from the event file of a recording.
        Events recording depends on a legacy format and is a bit degenerated.
    """

    # TODO: Utils detect filename
    fileFullpath = detectAndBuildFilename(os.path.join(recPath, "rawData"), ["rawEvents.csv"])

    if not os.path.isfile(fileFullpath):
        print(f"[eventUtils.py] no valid Events to load {fileFullpath}")
        return None

    events = []
    
    with open(fileFullpath, 'r') as eventsFile:
        reader = csv.reader(eventsFile)

        for row in reader:

            event = []
        
            # clean up spurious characters
            for i in range(len(row)):
                row[i] = row[i].strip("'") # patch for ' inserted in Event types, by Vizia
                row[i] = row[i].lstrip()
                row[i] = row[i].rstrip()
                row[i] = removeChars(row[i], "[]\'")

            event.append(float(row[0]))
            event.append(row[1])

            # patch to extract info
            if event[1]=='TRIAL':
                event.append(row[3])
            elif event[1]=='OFFSET':
                event.append(row[2])

            events.append(event)


    # according to experiment, the first event SYSTEM_CONFIG is sent 1 seconds after experiment starts
    timeRef = events[0][0]-1

    # A correction factor "offset" event can be added manually in case events need to be
    # shifted in time.
    try:
        offset = extractMultipleEventIDs(events, ["OFFSET"])
        if len(offset) > 0:
            offset = float(offset[0][2])
        else:
            offset = 0
    except Exception as e:
        print(offset)
        print(f"offset not applied {e}")
        offset = 0

    "adjust time"
    for event in events:
        event[0] = event[0] + offset - timeRef

    if showEvents:
        print(events)

    # keep only TRIAL type of events
    events = extractMultipleEventIDs(events, ["TRIAL"])
    
    # remove blink repetition, if desired
    if removeBlinks:
        events = removeConsecutiveBlinks(events)
    
    return events

def extractMultipleEventIDs(events, eventIDs):
    """
    Used to select a set of events and reject everything else.
    """
    subset = []
    for event in events:
        if event[1] in eventIDs:
            subset.append(event)
    return subset

def removeChars(inputString, charsToRemove):
    for char in charsToRemove:
        inputString = inputString.replace(char, '')
    return inputString

def removeConsecutiveBlinks(events):
    """
    In the experiment, each blink is tagged. This function removes duplicates for
    when each blink is not required.
    """
    filteredEvents = []
    previous_string = None
    
    for event in events:
        if event[2] != previous_string:
            filteredEvents.append(event)
        previous_string = event[2]
    return filteredEvents
