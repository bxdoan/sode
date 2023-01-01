import argparse
import datetime
import json
import asyncio
from pyppeteer import launch

URL_PATH = 'https://xoso.com.vn'
FILE_NAME = 'xsmb.json'
FILE_ANALYSE = 'analise.json'
BEGIN_DATE = datetime.date(2007, 8, 18)


def read_json(filename):
    with open(filename, 'r') as f:
        return json.load(f)


def write_json(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)


def s2d(val: 'str') -> datetime.date:
    dt = s2dt(val)
    d  = dt.date() if dt else None
    return d


def s2dt(val:'str') -> datetime:
    """
    handles all conversions of string (with or without timezone) to datetime (with timezone) except YYYY-MM
    if no timezone is stated, UTC is assumed
    """
    if not val: return None

    val = val.strip("'").strip('"')
    try:
        dt = datetime.datetime.strptime(val, '%d-%m-%Y')
        return dt
    except ValueError:
        return None


async def main(file=None):

    # read existing data
    data = read_json(FILE_NAME)
    total_sode = {}
    prizes = data['prizes']
    for prize_in_day in prizes:
        day_check = s2dt(prize_in_day['date'])
        # for key and value in dict
        for key, value in prize_in_day.items():
            if "prize" in key:
                if isinstance(value, list):
                    total_sode = count_sode_in_list_prize(value, total_sode)
                elif isinstance(value, str):
                    total_sode = count_sode_in_prize(value, total_sode)
            elif "special" in key:
                total_sode = count_sode_in_prize(value, total_sode)

    write_json(FILE_ANALYSE, total_sode)


def count_sode_in_list_prize(prizes : list, total_sode : dict) -> dict:
    for prize in prizes:
        total_sode = count_sode_in_prize(prize, total_sode)
    return total_sode


def count_sode_in_prize(prize_str : str, total_sode: dict) -> dict:
    sode = prize_str[-2:]
    if sode in total_sode:
        total_sode[sode] += 1
    else:
        total_sode[sode] = 1
    return total_sode


if __name__ == "__main__":
    # Argparse arguments
    parser = argparse.ArgumentParser(
        description="Scan all data from 2007 to now."
    )

    parser.add_argument(
        "-f", "--file", default=FILE_NAME,
        help=f"\033[32m\033[1m\nFile name to analyse (default {FILE_NAME})\033[0m"
    )
    file = parser.parse_args().file

    asyncio.run(main(file=file))
