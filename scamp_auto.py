import subprocess as sp
import os
import get_files
import target_data
import config

def scamp_call(files):
    """
    Calls scamp on initial input fits files list.
    """
