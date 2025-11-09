# ipparser

ipparser is a command-line tool for processing and optimizing lists of IP addresses.  
It combines addresses that belong to the same network, producing a minimal and efficient list of network ranges.

## Features

- Merges individual IP addresses into network ranges  
- Supports various input formats (single IPs, CIDR blocks, and ranges)  
- Offers multiprocessing for faster processing on large files  
- Can count the total number of IP addresses in the input file  

## How to Run

1. Download the latest release  
2. Run the following command in a terminal:

   ```
   ipparser -I <input file> -O <output file> [optional parameters]
   ```

## Optional Parameters

- `-min <number>` — Minimum accepted network size  
- `-net` — Calculate the network address for every IP  
- `-mp` — Enable multiprocessing (available since v0.4.0)  
- `-count` — Count all IP addresses in the input file (available since v0.4.0)  

## Accepted Input Formats

The input file can contain any of the following formats:

- `<ip address>`  
- `<ip address>/<subnet mask>`  
- `<ip address> - <ip address>`  
- `<ip address>/<subnet mask> - <ip address>/<subnet mask>`  
- `<ip address> - <host net>`  
