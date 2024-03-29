import ipfilter as ipfilter
from netaddr import *

DIVIDER = '-'

# Find network address for given ip address
def ip_and(ip):
    ip_bits = ip.ip.bits()
    mask_bits = ip.netmask.bits()
    mask = ip.prefixlen
    ip_array = []
    
    tmp_bits = ''

    for i in range(0, len(ip_bits)):
        if ip_bits[i] != '.':
            if ip_bits[i] == '1' and mask_bits[i] == '1':
                tmp_bits += '1'
            else:
                tmp_bits += '0'
        else:
            ip_array.append(str(int(tmp_bits, 2)))
            tmp_bits = ''
    
    return IPNetwork('.'.join(ip_array) + '/' + str(mask))

# Return filter that is assigned to the given parameter
def get_filter(params, key):
    if key == 'MIN':
        return IPSupernetFilter(ipfilter.ANY, int(params[key]))
    elif key == 'NET':
        return IPNetworkFilter(ipfilter.LAST)
    else:
        return None

# Get all ip addresses from a range
def get_ip_range(start, end):
    ip_range = iter_iprange(start, end)
    return [IPNetwork(ip.__str__()) for ip in ip_range]

# Parse begin and end ip from an input
# Return range of ip addresses
def range_input(part1, part2):
    if not '.' in part2 and len(part2) < 4:
        part2 = '.'.join(part1.split('.')[0:3]) + '.' + part2

    return get_ip_range(part1, part2)

# Filter for setting minimum netmask
class IPSupernetFilter(ipfilter.IPFilter):

    def __init__(self, type, mask_size):
        super().__init__(type)
        self.mask_size = mask_size

    def filter(self, ip):
        tok = ip.__str__().split('/')
        if int(tok[1]) > self.mask_size:
            supernets = ip.supernet(self.mask_size)
            ip = supernets[0]
        
        return ip

# Filter for setting every address to its network address
class IPNetworkFilter(ipfilter.IPFilter):

    def filter(self, ip):
        return ip_and(ip)