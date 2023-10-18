
import logging
from pathlib import Path
from argparse import ArgumentParser
import pandas as pd

logger = logging.getLogger(__name__)

def main():

    parser = ArgumentParser()

    parser.add_argument(
        "--log",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Logging level.",
        default="WARNING",
    )

    parser.add_argument("--census", required=True, help="Census data file.")
    parser.add_argument("--vendor", required=True, help="Vendor data file.")

    parser.add_argument("-o", "--output", required=True, type=str, help="Output file.")

    args = parser.parse_args()

    level = getattr(logging, args.log)

    logging.basicConfig(level=level)
    logger.setLevel(level)

    output_path = Path(args.output)

    logger.info(f"Reading census file `{args.census}`")
    df_census = pd.read_csv(
        args.census,
        header=0,
        dtype={'STATE': str, 'COUNTY': str, 'TRACT': str}
    )

    logger.info(f"Reading vendor file `{args.census}`")
    df_vendor = pd.read_csv(
        args.vendor,
        header=0,
        dtype={'fips': str, 'cofips': str}
    )

    # Split up the fips in the vendor file.
    df_vendor['STATE'] = df_vendor['fips'].apply(lambda fips: fips[:2])
    df_vendor['COUNTY'] = df_vendor['fips'].apply(lambda fips: fips[2:5])
    df_vendor['TRACT'] = df_vendor['fips'].apply(lambda fips: fips[5:])

    # Merge the two.
    df_merged = df_vendor.merge(
        df_census,
        on=['STATE', 'COUNTY', 'TRACT'],
    )

    df_merged = df_merged[
        ['STATE', 'COUNTY', 'TRACT'] + [col for col in df_merged.columns if col not in ['STATE', 'COUNTY', 'TRACT']]
    ]

    output_path.parent.mkdir(exist_ok=True)
    df_merged.to_csv(output_path, index=False)


if __name__ == "__main__":
    main()