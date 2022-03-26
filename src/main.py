import sys
import argvparser as ap
from netaddr import *
from filters import *
import time

DIVIDER = '-'

# Check if given line is either single ip address
# or a ip range. If line is ip range then extract the range
def process_line_generator(line):
    ip_list = []
    if line != '':
        line = line.replace(' ', '')
        tokens = line.split(DIVIDER)
        if len(tokens) < 2:
            ip_list.append(IPNetwork(tokens[0]))
        else:
            tmp = range_input(tokens[0], tokens[1])
            ip_list.extend(tmp)
    
    return (x for x in ip_list)
    

# Read text file
# Save lines as IPNetwork objects
# Parse ip ranges if have any
def input_file_generator(filename):
    with open(filename, 'r') as file:
        for line in file:
            yield process_line_generator(line)

# Write IPNetworks to a text file
def write_file(filename, data):
    with open(filename, "w") as file:
        file.write("\n".join(address.__str__() for address in data))

# Creates all filters that will be used
def create_filters(params):
    filters = []
    for key in params:
        tmp = get_filter(params, key)
        if tmp != None:
            filters.append(tmp)
    return filters

# Filter ip list using given filters
def filter_list_generator(ip_gen, filters):
    for item in ip_gen:
        for ip in item:
            tmp = ip
            for f in filters:
                tmp = f.filter(tmp)
            yield tmp
        
# Parse unique ip networks
def uniques(ip_gen):
    tmp = set()
    for ip in ip_gen:
        if not ip in tmp:
            yield ip
            tmp.add(ip)

# Read parameters
# Read input file
# Create required filters
# Filter the entire list
# Write results to an output file
def main(argv):
    params = ap.parse(argv)
    input_gen = input_file_generator(params['-I'])
    filters = create_filters(params)
    filtered_gen = filter_list_generator(input_gen, filters)
    unique_gen = uniques(filtered_gen)
    ip_list = cidr_merge(unique_gen)
    write_file(params['-O'], ip_list)

if __name__ == "__main__":
    start_time = time.time()
    main(sys.argv)
    print(f"--- %s seconds ---" % (time.time() - start_time))