import sys
import argvparser as ap
from netaddr import *
import pprint

DIVIDER = '-'

def get_ip_range(start, end):
    ip_range = list(iter_iprange(start, end))
    ip_list = []

    for ip in ip_range:
        ip_list.append(IPNetwork(ip.__str__()))

    return ip_list

def read_file(filename):
    ip_list = []

    with open(filename, "r") as file:
        lines = file.read().split("\n")
        for line in lines:
            line = line.replace(' ', '')
            tokens = line.split(DIVIDER)
            if len(tokens) < 2:
                ip_list.append(IPNetwork(tokens[0]))
            else:
                tmp = get_ip_range(tokens[0], tokens[1])
                ip_list.extend(tmp)

    return ip_list

def write_file(filename, data : list):
    with open(filename, "w") as file:
        for address in data:
            file.write(address.__str__() + "\n")

def main(argv):
    params = ap.parse(argv)
    ip_list = read_file(params['-I'])
    ip_list = cidr_merge(ip_list)
    write_file(params['-O'], ip_list)

if __name__ == "__main__":
    main(sys.argv)