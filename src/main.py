import sys
import argvparser as ap
from netaddr import *
from filters import *
import time
from iputils import *

# Read parameters
# Process given input file
# Write results to an output file
def main(argv):
    params = ap.parse(argv)
    ip_list = process_file(params)
    write_file(params['-O'], ip_list)

if __name__ == "__main__":
    start_time = time.time()
    main(sys.argv)
    elapsed = time.time() - start_time
    print(f"--- %s seconds ---" % (round(elapsed, 2)))