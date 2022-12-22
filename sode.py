import datetime
import json
import asyncio
from pyppeteer import launch

URL_PATH = 'https://xoso.com.vn'
FILE_NAME = 'xsmb.database.json'


def read_json(filename):
    with open(filename, 'r') as f:
        return json.load(f)


def write_json(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)


async def main():
    browser = await launch(
        ignoreHTTPSErrors=True,
        headless=False,
    )
    page = await browser.newPage()
    from_date_query = datetime.date(2022, 12, 1)
    to_date_query = datetime.date(2022, 12, 21)
    res = []
    while from_date_query < to_date_query:
        date_str = from_date_query.strftime('%d-%m-%Y')
        await page.goto(f'{URL_PATH}/xsmb-{date_str}.html')
        try:
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
            write_json(FILE_NAME, {"prices": res})
            from_date_query += datetime.timedelta(days=1)
        except Exception as e:
            print(e)
            continue

    await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
