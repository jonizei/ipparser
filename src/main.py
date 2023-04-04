
import sys
import argvparser as ap
from netaddr import *
from filters import *
import time
from iputils import *
import multiprocessing as mp

DIVIDER = '-'

# Read parameters
# Process given input file
# Write results to an output file
def main(argv):
    params = ap.parse(argv)

    if not ap.required_params_exists(params):
        print("Input or output file is missing.")
    else:
        count = 0
        if 'COUNT' in params:
            count = count_items(params['INPUT'])
        
        if 'MULTI_PROCESS' in params:
            ip_list = process_file_multiprocessing(params)
        else:
            ip_list = process_file_serial(params)

        write_file(params['OUTPUT'], ip_list)

        if count > 0:
            print(f"%d items processed" % (count))


if __name__ == "__main__":
    mp.freeze_support()
    start_time = time.time()
    main(sys.argv)
    elapsed = time.time() - start_time
    print(f"--- %s seconds ---" % (round(elapsed, 2)))