import sys
import argvparser as ap

def main(argv):
    params = ap.parse(argv)
    print(params)

if __name__ == "__main__":
    main(sys.argv)