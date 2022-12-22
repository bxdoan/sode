import json
import asyncio
from pyppeteer import launch

URL_PATH = 'https://xoso.com.vn'


def read_json(filename):
    with open(filename, 'r') as f:
        return json.load(f)


def write_json(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f)


async def main():
    browser = await launch(
        ignoreHTTPSErrors=True,
        headless=False,
    )
    page = await browser.newPage()
    date_query = '21-12-2022'
    await page.goto(f'{URL_PATH}/xsmb-{date_query}.html')

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
        print(dimensions)

    except Exception as e:
        print(e)
        return

    await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
