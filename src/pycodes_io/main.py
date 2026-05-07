import argparse
import sys
import textwrap
from pathlib import Path

from pycodes_io.Compare import ComparisonObj
from pycodes_io.Doogal import DoogalObj
from pycodes_io.Postcode import PostcodeObj

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
        "--postcode",
        type=str,
        help="Postcode in format of PE122LN or PE12, depending on function you need.",
    )
    parser.add_argument(
        "--csv", type=Path, help="CSV formatted file C1=postcode, C2=other_data"
    )
    parser.add_argument(
        "--function",
        choices=["postcodes", "outcodes"],
        required=True,
        help="api endpoint to use.",
    )
    parser.add_argument(
        "--use_doogal",
        action="store_true",
        help="Boolean to use doogal api to compare with postcodes.io",
    )
    parser.add_argument(
        "--postcodes_base_url",
        type=str,
        default="192.168.1.227:8070",
        help="Base URL for postcodes.io API.",
    )
    parser.add_argument(
        "--dry_run",
        action="store_true",
        help="Boolean to run in dry mode, i.e. don't write output to CSV",
    )
    return parser.parse_args()


def validate_postcode(postcode: str, function: str) -> str:
    """
    Very basic validation of the postcode format vs an outcode
    """
    if function == "outcodes" and len(postcode) <= 4:
        pass
    elif function == "postcodes" and len(postcode) >= 4:
        pass
    else:
        sys.exit("Postcode not correct for function")
    return postcode


def pull_lat_long(postcodeio: dict) -> tuple:
    """Return only the lat and long from the dict"""
    return postcodeio["latitude"], postcodeio["longitude"]


def run_and_collect_from_csv(csv_path: Path, function: str, base_url: str):
    output_dict = {}

    with csv_path.open() as f:
        for line in f:
            postcode, area = line.split(",")
            postcode = postcode.strip()
            area = area.strip()

            code = validate_postcode(postcode, function)
            postcodeio = PostcodeObj(code, function, base_url)

            print(f"---- Postcode: {postcode}\n{postcodeio}\n")

            latitude, longitude = pull_lat_long(postcodeio.lat_long)
            output_dict[postcode] = [latitude, longitude, area]

    return output_dict


def output_data_to_csv(output_dict: dict):

    with open("output.csv", "w") as f:
        f.write("postcode,latitude,longitude,area\n")
        for postcode, data in output_dict.items():
            f.write(f"{postcode},{data[0]},{data[1]},{data[2]}\n")


def main():
    args = parse_args()

    if args.csv:
        output_dict = run_and_collect_from_csv(
            args.csv, args.function, args.postcodes_base_url
        )

        if not args.dry_run:
            output_data_to_csv(output_dict)

    if args.postcode:
        code = validate_postcode(args.postcode, args.function)
        postcodeio = PostcodeObj(code, args.function, args.postcodes_base_url)

        if args.use_doogal:
            doogal = DoogalObj(code, args.function)
            print(ComparisonObj(postcodeio, doogal))
        else:
            print(postcodeio)


if __name__ == "__main__":
    main()
