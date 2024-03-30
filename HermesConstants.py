

class HermesConstants(object):

    SAMPLING_RATE = 250
    SAMPLING_PERIOD = (1/SAMPLING_RATE)

    CHANNELS = {"HEAD_L": 0, "HEAD_R": 1, "CHEEK_L": 2, "CHEEK_R": 3, "EAR_L": 4, "EAR_R": 5, "BROW": 6, "NOSE": 7}
    CHANNEL_NAMES = list(CHANNELS.keys())
