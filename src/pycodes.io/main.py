import requests
import json
import sys
from Postcode import PostcodeObj

def main():
    print(PostcodeObj(sys.argv[1]))
    
if __name__ == "__main__":
    main()