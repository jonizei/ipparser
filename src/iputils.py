import argvparser as ap
from netaddr import *
from filters import *
import multiprocessing as mp
import os

DIVIDER = '-'

# Creates all filters that will be used
def create_filters(params):
    filters = []
    for key in params:
        tmp = get_filter(params, key)
        if tmp != None:
            filters.append(tmp)
    return filters

# Write IPNetworks to a text file
def write_file(filename, data):
    with open(filename, "w") as file:
        file.write("\n".join(address.__str__() for address in data))

def filter_list(ip_list, filters):
    new_list = []
    for ip in ip_list:
        tmp = ip
        for f in filters:
            tmp = f.filter(ip)
        new_list.append(tmp) 
    
    return new_list

# Parse unique values from list
def uniques(ip_list):
    tmp = set()
    for ip in ip_list:
        tmp.add(ip)
    return tmp

# Process a single line
def process_line(line):
    ip_list = []
    line = line.replace(' ', '')
    line = line.replace('\n', '')
    if line != '':
        tokens = line.split(DIVIDER)
        if len(tokens) < 2:
            ip_list.append(IPNetwork(tokens[0]))
        else:
            tmp = range_input(tokens[0], tokens[1])
            ip_list.extend(tmp)

    return ip_list

# Process single file chunk
def process_chunk(filename, chunk_start, chunk_end):
    chunk_results = []
    with open(filename, 'r') as f:
        f.seek(chunk_start)

        for line in f:
            chunk_start += len(line)
            if chunk_start > chunk_end:
                break
            chunk_results.append(process_line(line))
    return chunk_results

# Read input file with multiple processes
def paraller_read(filename):
    cpu_count = mp.cpu_count()
    file_size = os.path.getsize(filename)
    chunk_size = file_size // cpu_count

    chunk_args = []
    with open(filename, 'r') as f:
        def is_start_of_line(position):
            if position == 0:
                return True

            f.seek(position-1)
            return f.read(1) == '\n'

        def get_next_line_position(position):
            f.seek(position)
            f.readline()
            return f.tell()

        chunk_start = 0
        while chunk_start < file_size:
            chunk_end = min(file_size, chunk_start + chunk_size)

            while not is_start_of_line(chunk_end):
                chunk_end -= 1

            if chunk_start == chunk_end:
                chunk_end = get_next_line_position(chunk_end)

            args = (filename, chunk_start, chunk_end)
            chunk_args.append(args)

            chunk_start = chunk_end

    with mp.Pool(cpu_count) as p:
        chunk_results = p.starmap(process_chunk, chunk_args)

    results = []

    for chunk_result in chunk_results:
        for result in chunk_result:
            results.append(result)
    
    return results

# Filter chunk of ip addresses
def filter_chunk(chunk, filters):
    ip_list = filter_list(chunk, filters)
    unique_set = uniques(ip_list)
    return cidr_merge(unique_set)

# Filter ip addresses with multiple processes
def paraller_filter(results, filters):
    cpu_count = mp.cpu_count()
    filter_results = []
    results = [(x, filters) for x in results]
    with mp.Pool(cpu_count) as p:
        filter_results = p.starmap(filter_chunk, results)
    
    results = []
    for result in filter_results:
        results.extend(result)

    return results

# Process given input file
def process_file(params):
    filters = create_filters(params)
    results = paraller_read(params['-I'])
    results = paraller_filter(results, filters)
    return cidr_merge(results)
