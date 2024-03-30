
import os


def detectAndBuildFilename(filePath, candidates):
    """
    Function that test amongst candidate for a valid filename, useful to support
    legacy naming.

    :param filePath: base path where to test for filename
    :param candidates: list of filenames to test
    :return: the first name encountered as valid, none otherwise
    """
    for filename in candidates:
        if os.path.exists(os.path.join(filePath, filename)):
            return os.path.join(filePath,filename)

    return None


def printWarning(s):
    """
    Print a string, in console, in Yellow, as a warning
    :param s: the string to print
    :return: None
    """
    WARNING_COLOR = '\033[33;1m'
    COLOR_RESET = '\033[0m'
    print(f"{WARNING_COLOR}{s}{COLOR_RESET}")

def printError(s):
    """
    Print a string, in console, in Yellow, as an error
    :param s: the string to print
    :return:
    """
    ERROR_COLOR = '\033[31m'
    COLOR_RESET = '\033[0m'
    print(f"{ERROR_COLOR}{s}{COLOR_RESET}")

