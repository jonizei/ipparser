from ipfilter import IPFilter
from netaddr import *

# Find network address for given ip address
def ip_and(ip):
    ip_bits = ip.ip.bits()
    mask_bits = ip.netmask.bits()
    mask = ip.__str__().split('/')[1]

    tmp = ''

    ip_array = []

    for i in range(0, len(ip_bits)):
        if ip_bits[i] != '.':
            if ip_bits[i] == '1' and mask_bits[i] == '1':
                tmp += '1'
            else:
                tmp += '0'
        else:
            ip_array.append(str(int(tmp, 2)))
            tmp = ''

    ip_str = '.'
    return IPNetwork(ip_str.join(ip_array) + '/' + mask)

# Return filter that is assigned to the given parameter
def get_filter(params, key):
    if key == '-min':
        return IPSupernetFilter(int(params[key]))
    elif key == '-net':
        return IPNetworkFilter()
    else:
        return None

class IPSupernetFilter(IPFilter):

    def __init__(self, mask_size):
        self.mask_size = mask_size

    def filter(self, ip_list) -> list:
        new_list = []
        for ip in ip_list:
            tok = ip.__str__().split('/')
            if int(tok[1]) > self.mask_size:
                supernets = ip.supernet(self.mask_size)
                new_list.append(supernets[0])
            else:
                new_list.append(ip)

        return new_list

class IPNetworkFilter(IPFilter):

    def filter(self, ip_list) -> list:
        new_list = []
        for ip in ip_list:
            new_list.append(ip_and(ip))
        
        return new_list