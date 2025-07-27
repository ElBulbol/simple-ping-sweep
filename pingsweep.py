import subprocess
import sys
import argparse
from subprocess import PIPE
import platform

os_name = platform.system().lower()
windows = 'windows' in os_name or 'msys' in os_name or 'cygwin' in os_name
print(windows)
suc = 0

parser = argparse.ArgumentParser(description='Ping Scan Network')
parser.add_argument("-network", dest="network", help="Network segment [Example: 192.168.56]", required=True)
parser.add_argument("-machines", dest="machines", help="Number of machines", type=int, required=True)
parsed_args = parser.parse_args()

for ip in range(1, parsed_args.machines + 1):
    ipAddress = parsed_args.network + '.' + str(ip)
    print(f"Scanning {ipAddress}")
    if windows:
        raw_output = subprocess.Popen(['ping', ipAddress], stdin=PIPE, stdout=PIPE, stderr=PIPE).communicate()[0]
        finalout = raw_output.decode('utf-8', errors='ignore')
        finalout = "\n".join(finalout.splitlines()[:-5])
        print(finalout)
        if "TTL=" in finalout or "time=" in finalout:
            print(f"The IP Address {ipAddress} has responded with an ECHO_REPLY!")
            suc += 1
    else:
        raw_output = subprocess.Popen(['/bin/ping','-c1',ipAddress],stdout = subprocess.PIPE).communicate()[0]
        finalout = raw_output.decode('utf-8', errors='ignore')
        finalout = "\n".join(finalout.splitlines()[:-5])
        print(finalout)
        if "TTL=" in finalout or "time=" in finalout:
            print(f"The IP Address {ipAddress} has responded with an ECHO_REPLY!")
            suc += 1
if parsed_args.machines == suc:
    print("All the ping requests were successful")
else:
    print(f"Just {suc} devices responded")
