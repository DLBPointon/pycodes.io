import argparse
import textwrap
import requests
import json
import sys
from Postcode import PostcodeObj


DESCRIPTION = """
---------------------------------------
            PyCodes.io
---------------------------------------
           by DLBPointon
---------------------------------------
A small wrapper to call API's of:
    Postcodes.io
    Doogal

These both serve data on postcodes
and other related data.

This script has been writted for use
in decerning which is better for use
at Citizens advice.
"""


def parse_args():
  parser = argparse.ArgumentParser(
      prog="get_READMEs",
      formatter_class=argparse.RawDescriptionHelpFormatter,
      description=textwrap.dedent(DESCRIPTION),
  )
  parser.add_argument(
      "postcode", type=str, help="Postcode in format of PE122LN or PE12, depending on function you need."
  )
  parser.add_argument(
      "function", choices=["postcodes","outcodes"], help="api endpoint to use."
  )
  return parser.parse_args()


def validate_postcode(args):
    if args.function == "outcodes" and len(args.postcode) <= 4:
        pass
    elif args.function == "postcodes" and len(args.postcode) >= 4:
        pass
    else:
        sys.exit("Postcode not correct for function")
    return args.postcode

def main():
    args = parse_args()
    code = validate_postcode(args)
    print(PostcodeObj(code, args.function))

if __name__ == "__main__":
    main()
