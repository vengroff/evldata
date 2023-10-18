
import logging
from pathlib import Path
from argparse import ArgumentParser

import censusdis.data as ced
from censusdis.datasets import ACS5
from censusdis.states import ALL_STATES_AND_DC

logger = logging.getLogger(__name__)


dataset = ACS5

def main():
    parser = ArgumentParser()

    parser.add_argument(
        "--log",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Logging level.",
        default="WARNING",
    )

    parser.add_argument(
        "-v", "--vintage", default=2018, type=int, help="Year to get data."
    )
    parser.add_argument("-o", "--output", required=True, type=str, help="Output file.")

    args = parser.parse_args()

    level = getattr(logging, args.log)

    logging.basicConfig(level=level)
    logger.setLevel(level)

    vintage = args.vintage
    output_path = Path(args.output)

    variables = None
    leaves_of_group = 'B03002'

    df = ced.download(
        dataset,
        vintage,
        download_variables=variables,
        leaves_of_group=leaves_of_group,
        state=ALL_STATES_AND_DC,
        county='*',
        tract='*',
    )

    output_path.parent.mkdir(exist_ok=True)

    df.to_csv(output_path, index=False)


if __name__ == "__main__":
    main()
