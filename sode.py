import argparse
import datetime
import json
import asyncio
from pyppeteer import launch

URL_PATH = 'https://xoso.com.vn'
FILE_NAME = 'xsmb.database.json'
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


async def main(from_date_query=None, to_date_query=None):
    browser = await launch(
        ignoreHTTPSErrors=True,
        headless=False,
    )
    page = await browser.newPage()
    if from_date_query is None:
        from_date_query = BEGIN_DATE
    if to_date_query is None:
        to_date_query = datetime.date.today() - datetime.timedelta(days=1)

    res = []
    while from_date_query < to_date_query:
        date_str = to_date_query.strftime('%d-%m-%Y')
        url_query = f'{URL_PATH}/xsmb-{date_str}.html'
        print(f'Querying {url_query}')
        try:
            await page.goto(url_query, {"waitUntil": 'load'})

            dimensions = await page.evaluate('''() => {
            const special = document
              .querySelectorAll("span.special-prize")[0]
              .textContent.trim();
    
            const prize1 = document
              .querySelectorAll("span.prize1")[0]
              .textContent.trim();
    
            let prize2 = [];
            document.querySelectorAll("span.prize2").forEach((prize) => {
              prize2 = [...prize2, prize.textContent.trim()];
            });
            let prize3 = [];
            document.querySelectorAll("span.prize3").forEach((prize) => {
              prize3 = [...prize3, prize.textContent.trim()];
            });
            let prize4 = [];
            document.querySelectorAll("span.prize4").forEach((prize) => {
              prize4 = [...prize4, prize.textContent.trim()];
            });
            let prize5 = [];
            document.querySelectorAll("span.prize5").forEach((prize) => {
              prize5 = [...prize5, prize.textContent.trim()];
            });
            let prize6 = [];
            document.querySelectorAll("span.prize6").forEach((prize) => {
              prize6 = [...prize6, prize.textContent.trim()];
            });
            let prize7 = [];
            document.querySelectorAll("span.prize7").forEach((prize) => {
              prize7 = [...prize7, prize.textContent.trim()];
            });
    
            return {
              special,
              prize1,
              prize2,
              prize3,
              prize4,
              prize5,
              prize6,
              prize7,
            };
          }''')
            dimensions['date'] = date_str
            res.append(dimensions)
            write_json(FILE_NAME, {"prizes": res})
            await asyncio.sleep(1)
            to_date_query -= datetime.timedelta(days=1)
        except Exception as e:
            await browser.close()
            print(e)
            to_date_query -= datetime.timedelta(days=1)
            browser = await launch(
                ignoreHTTPSErrors=True,
                headless=False,
            )
            page = await browser.newPage()
            continue

    await browser.close()


if __name__ == "__main__":
    # Argparse arguments
    parser = argparse.ArgumentParser(
        description="Scan all data from 2007 to now."
    )

    parser.add_argument(
        "-f", "--from-date",
        help="\033[32m\033[1m\nFrom date (default 18-08-2007)\033[0m"
    )

    parser.add_argument(
        "-t", "--to-date",
        help="\033[32m\033[1m\nTo date (default yesterday) \033[0m"
    )

    from_date = s2d(parser.parse_args().from_date)
    to_date = s2d(parser.parse_args().to_date)
    asyncio.run(main(from_date_query=from_date, to_date_query=to_date))
