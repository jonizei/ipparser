# ipparser

  Merges list of ip addresses into networks.

## How to run

  1. Download newest release
  2. Type "ipparser -I \<input text file\> -O \<output text file\> \<optional parameters\>" to a command prompt

## Optional parameters
  
  -min \<number\> = minimun accepted network<br/>
  -net = find network address for every ip address<br/> 
  -mp = process file using multiprocessing (version >= v0.4.0)<br/>
  -count = count addresses in the input file (version >= v0.4.0)<br/>
  
## Possible inputs

  input file can contain these lines:<br/>
    - \<ip address\><br/>
    - \<ip address\>/\<subnet mask\><br/>
    - \<ip address\> - \<ip address\><br/>
    - \<ip address\>/\<subnet mask\> - \<ip address\>/\<subnet mask\><br/>
    - \<ip address\> - \<host net\><br/>
    