from glob import glob
from pathlib import Path
from termcolor import colored

TABLE_FILE_EXT = { '.xlsx', '.xls', 'xlsm', 'xlsb', '.csv', '.tsv', '.txt' }


def expandpath(fp_str):
    """Unix-like file interpretor in Python
    
    Deals with wildcards `*` and home alias `~` in paths
    """
    return [ Path(fp) for fp in glob(str(Path(fp_str).expanduser())) ]


def UnexpectedFile(msg, color="red"):
    print(colored(msg, color))
    raise Exception("Unexpected input")

def FileNotFound(msg, color="red"):
    print(colored(msg, color))
    raise Exception("File doesn't exist")
