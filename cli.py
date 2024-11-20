# stdlib
import argparse
import pathlib

# 3rd party
# ---------

# local
from . import parser as pdf_parser


def cli():
    """Main command line interface entry-point."""
    parser = create_parser()
    args = parser.parse_args()

    src = args.src
    dst = args.dst
    ignore_exceptions = not args.raise_exceptions

    pdf_parser.pdf_to_json_scores(src, dst, ignore_exceptions)


def create_parser() -> argparse.ArgumentParser:
    """Creates the argparse.ArgumentParser object for this package.

    Returns:
        argparse.ArgumentParser: The parser.
    """
    description = "Tools for extracting risk scores from thermography exam reports."
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument(
        "src",
        metavar="pdf_file",
        type=pathlib.Path,
        help="The PDF file from which to extract risk scores.",
    )
    parser.add_argument(
        "-o",
        dest="dst",
        metavar="json_file",
        type=pathlib.Path,
        default=None,
        help="The JSON file to write scores to. If not specified the filename is "
        + "determined from the PDF filename.",
    )
    parser.add_argument(
        "--raise-exceptions",
        action="store_true",
        help="Raise an exception if scores are not found.",
    )

    return parser
