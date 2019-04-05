import os
import psutil

def find_procs_by_name(pid):
    p = psutil.Process(pid)

find_procs_by_name(12988)
