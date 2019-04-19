#/usr/bin/env python3.6

import os
import subprocess
from argparse import ArgumentParser

parser = ArgumentParser(description='kill the running process listening on a given port')
parser.add_argument('port', type=int, help='the process you want to search for')

port = parser.parse_args().port

try:
    result = subprocess.run(
            ['lsof', '-n', '-i4TCP:%s' % port],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
except subprocess.CalledProcessError:
    print(f'No process listening on port {port}')
else:
    listening = None

    for line in result.stdout.splitlines():
        if "LISTEN" in str(line):
            listening = line
            break

    if listening:
        # PID is lthe second column in the output
        pid = int(listening.split()[1])
        os.kill(pid,9)
        print(f"Killed process {pid}")
    else:
        print(f"No process listening on port {port}")
