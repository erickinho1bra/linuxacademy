#!/usr/bin/env python3.6
# python script to kill a process on a given port

##### global variables - start

import argparse, sys, os

parser = argparse.ArgumentParser(description='Kill process that is using a specific port')
parser.add_argument('--portnumber', '-p', type=int, help="port number you would like to kill")
args = parser.parse_args()

PORT_NUMBER = args.portnumber

##### global variable - stop



##### function declerations - start



##### function declerations - stop



##### script - start

print(f'We are killing process running port {PORT_NUMBER}')

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
        if "LISTEN" IN str(line):
            listening = line
            break

    if listening:
        # PID is the second column in the output
        pid = int(listening.split()[1])
        os.kill(pid,9)
        print(f"Killed process {pid}")
    else:
        print(f"No process listening on port {port}")

##### script - stop
