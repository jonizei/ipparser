import sys
import argvparser as ap
from netaddr import *
import pprint
from filters import *

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

if __name__ == "__main__":
    main(sys.argv)