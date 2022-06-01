
#!/usr/bin/env python3.7
# This is a script to take in a port number, see if it is running, then if it is, it will kill it but if it is not running then it'll do nothing.

import os
import subprocess
from argparse import ArgumentParser

##### global variables - start

parser = ArgumentParser(description='kill the running process listening on a given port')
parser.add_argument('port', type=int, help='the process you want to search for')

port = parser.parse_args().port
=======
#!/usr/bin/env python3.6
# <add comments here>

##### global variables - start




##### global variable - stop



##### function declerations - start



=======


##### function declerations - stop



##### script - start


try:
    result = subprocess.run(
        ['lsof', '-n', '-i4TCP:%s' % port],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
except subprocess.CalledProcessError:
    print(f'No process listening on port {port}')
else:
    listening = None

    for line in result.stdout.splitlines():
        if "LISTEN" in str(line):
            listening = line
            break
    
    if listening:
        # PID is the second column in the output
        pid = int(listening.split()[1])
        os.kill(pid,9)
        print(f"Killed process {pid}")
    else:
        print(f"No process listening on port {port}")
        exit(6)
=======



##### script - stop
