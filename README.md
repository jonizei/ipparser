# ipparser

  Merges list of ip addresses into networks.

## How to run

  1. Download newest release
  2. Type "ipparser -I \<input text file\> -O \<output text file\> \<optional parameters\>" to a command prompt

## Optional parameters
  
  -min \<number\> = minimun accepted network<br/>
  -net = find network address for every ip address 
  
## Possible inputs

  input file can contain these lines:
    - <\ip address\>
    - <\ip address\>/<\subnet mask\>
    - <\ip address\> - <\ip address\>
    - <\ip address\>/<\subnet mask\> - <\ip address\>/<\subnet mask\>
    - <\ip address\> - <\host net\>
