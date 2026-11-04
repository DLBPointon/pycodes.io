import argparse
import logging
import sys
import textwrap
from pathlib import Path

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

logger = logging.getLogger(__name__)


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
        "--output",
        type=Path,
        help="Output file path",
    )

    parser.add_argument(
        "--code_type",
        type=str,
        default="postcodes",
        help="Code type to use (postcodes or outcodes).",
    )

    parser.add_argument(
        "--postcodes_base_url",
        type=str,
        default="0.0.0.0",
        help="Base URL for postcodes.io API.",
    )

    parser.add_argument(
        "--postcodes_port",
        type=str,
        default="8008",
        help="Port for postcodes.io API.",
    )
    return parser.parse_args()


def validate_postcode(postcode: str, function: str) -> str:
    """
    Very basic validation of the postcode format vs an outcode
    """
    if (
        function == "outcodes"
        and len(postcode) <= 4
        or function == "postcodes"
        and len(postcode) >= 4
    ):
        pass
    else:
        sys.exit("Postcode not correct for function")
    return postcode


def pull_lat_long(postcodeio: dict) -> tuple:
    """Return only the lat and long from the dict"""
    return postcodeio["latitude"], postcodeio["longitude"]


def run_and_collect_from_csv(
    csv_path: Path, function: str, base_url: str, output_path: Path
):

    with open(output_path, "w") as f_out:
        f_out.write(
            "postcode,area,lsoa,icb,parish,admin_district,admin_ward,latitude,longitude\n"
        )

        valid_counter = 0
        invalid_counter = 0
        input_lines = 0

        with csv_path.open() as f:
            for line in f:
                input_lines += 1

                data = line.split(",")
                postcode = data[0].strip()
                extra_1 = data[1].strip()  # Ward
                extra_2 = data[2].strip()  # District

                logger.info(f"---- Postcode: {postcode}\n")
                code = validate_postcode(postcode, function)
                postcodeio = PostcodeObj(code, function, base_url)

                latitude, longitude = pull_lat_long(postcodeio.lat_long)
                valid_counter += 1
                new_line = f'{postcode},"{extra_1}",{postcodeio.lsoa},"{postcodeio.icb}","{postcodeio.parish}","{postcodeio.admin_district}","{postcodeio.admin_ward}",{latitude},{longitude},"{extra_2}"\n'
                logger.info(new_line)
                f_out.write(new_line)

        logger.info(
            f"Input: {input_lines}, Valid: {valid_counter}, Invalid: {invalid_counter}"
        )


def main():
    args = parse_args()

    run_and_collect_from_csv(
        args.csv,
        args.code_type,
        f"{args.postcodes_base_url}:{args.postcodes_port}",
        args.output,
    )


if __name__ == "__main__":
    main()
