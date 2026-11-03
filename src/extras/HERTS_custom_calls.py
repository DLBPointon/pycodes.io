import argparse
from importlib import invalidate_caches
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
        "--csv", type=Path, help="CSV formatted file C1=postcode, C2=other_data"
    )
    parser.add_argument(
        "--postcodes_base_url",
        type=str,
        default="192.168.1.227:8070",
        help="Base URL for postcodes.io API.",
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

    with open("/home/dlbpointon/Documents/pycodes.io/HERTS_june26_V2.csv", "w") as f_out:
        f_out.write("postcode,area,lsoa,icb,parish,admin_district,admin_ward,latitude,longitude\n")

        with csv_path.open() as f:
            for line in f:
                if "Unit Postcode" in line:
                    pass
                else:
                    data = line.split(",")
                    postcode = data[0].strip()
                    lat = data[1].strip()
                    long = data[2].strip()
                    pcn = data[-1].strip()

                    print(f"---- Postcode: {postcode}\n")
                    code = validate_postcode(postcode, function)
                    postcodeio = PostcodeObj(code, function, base_url)

                    latitude, longitude = pull_lat_long(postcodeio.lat_long)
                    new_line = f'{postcode},{pcn},{postcodeio.lsoa},"{postcodeio.icb}",{postcodeio.parish},"{postcodeio.admin_district}","{postcodeio.admin_ward}",{latitude},{longitude}\n'
                    print(new_line)
                    f_out.write(new_line)


def main():
    args = parse_args()

    run_and_collect_from_csv(
        args.csv, "postcodes", args.postcodes_base_url
    )


if __name__ == "__main__":
    main()
