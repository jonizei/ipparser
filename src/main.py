import sys
import argvparser as ap
from netaddr import *
import pprint
from filters import *
from tmphandler import *
import time
import threading
from ipthread import IPThread

TMP_DIR = './tmp'
TMP_FILE_01 = TMP_DIR + '/temp_01.txt'
TMP_FILE_02 = TMP_DIR + '/temp_02.txt'
TMP_FILE_01_2 = TMP_DIR + '/temp_01_2.txt'
TMP_FILE_02_2 = TMP_DIR + '/temp_02_2.txt'
DIVIDER = '-'

# Create list of ip networks from 
# list of strings
def create_ip_list(lines):
    ip_list = []
    
    for line in lines:
        if line != '':
            line = line.replace(' ', '')
            tokens = line.split(DIVIDER)
            if len(tokens) < 2:
                ip_list.append(IPNetwork(tokens[0]))
            else:
                tmp = range_input(tokens[0], tokens[1])
                ip_list.extend(tmp)

    return ip_list


# Read text file
# Save lines as IPNetwork objects
# Parse ip ranges if have any
def read_file(filename):
    ip_list = []

    with open(filename, "r") as file:
        lines = file.read().split("\n")
        ip_list = create_ip_list(lines)

    return ip_list

# Write IPNetworks to a text file
def write_file(filename, data : list):
    with open(filename, "w") as file:
        for address in data:
            file.write(address.__str__() + "\n")

# Creates all filters that will be used
def create_filters(params):
    filters = []
    for key in params:
        tmp = get_filter(params, key)
        if tmp != None:
            filters.append(tmp)

    return filters

# Filter ip list using given filters
def filter_list(ip_list, filters):
    new_list = ip_list
    for f in filters:
        new_list = f.filter(new_list)

    return new_list

def flip_tmp_files(f_from, f_to):
    tmp = f_from
    f_from = f_to
    f_to = tmp

    return (f_from, f_to)

def read_input(input_file):
    lcount = rawgencount(input_file)
    halfA = round(lcount / 2, 0)
    halfB = lcount - halfA
    filter = IPInputFilter()
    index = 0

    tmpA_file = open(TMP_FILE_01, 'w')
    tmpB_file = open(TMP_FILE_02, 'w')

    with open(input_file, 'r') as file:
        lines = file.read().split('\n')
        for line in lines:
            if index < halfA+1:
                tmpA_file.write(filter.filter_single(line) + '\n')
            else:
                tmpB_file.write(filter.filter_single(line) + '\n')
            index += 1

    tmpA_file.close()
    tmpB_file.close()       

def filter_list_test(filters):
    tmp01_from = TMP_FILE_01
    tmp01_to = TMP_FILE_01_2
    tmp02_from = TMP_FILE_02
    tmp02_to = TMP_FILE_02_2

    for f in filters:
        thread1 = IPThread(1, "Thread-1", tmp01_from, tmp01_to, f)
        thread2 = IPThread(2, "Thread-2", tmp02_from, tmp02_to, f)

        thread1.start()
        thread2.start()

        thread1.join()
        thread2.join()

        tmp01_from, tmp01_to = flip_tmp_files(tmp01_from, tmp01_to)
        tmp02_from, tmp02_to = flip_tmp_files(tmp02_from, tmp02_to)
        #write_tmp_file(f_from, f_to, f)
        #f_from, f_to = flip_tmp_files(f_from, f_to)
        

# Read parameters
# Read input file
# Create required filters
# Filter the entire list
# Write results to an output file
def main(argv):
    params = ap.parse(argv)
    ip_list = read_file(params['-I'])
    filters = create_filters(params)
    ip_list = filter_list(ip_list, filters)
    ip_list = cidr_merge(ip_list)
    write_file(params['-O'], ip_list)

def main_test(argv):
    init_files(TMP_DIR, [TMP_FILE_01, TMP_FILE_02, TMP_FILE_01_2, TMP_FILE_02_2])
    params = ap.parse(argv)
    read_input(params['-I'])
    filters = create_filters(params)
    filter_list_test(filters)

if __name__ == "__main__":
    start_time = time.time()
    #main(sys.argv)
    main_test(sys.argv)
    print(f"--- %s seconds ---" % (time.time() - start_time))