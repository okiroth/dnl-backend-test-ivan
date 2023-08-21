import requests
import aiohttp
import asyncio
from bs4 import BeautifulSoup
import json
from database_handler import save_json_to_DB
import time

URL_BASE = 'https://www.urparts.com'
URL_BRANDS = 'index.cfm/page/catalogue'

def run():
    start_time = time.time()
    # asyncio.run(scrape_data())
    # save_json_to_DB()
    print("--- %s seconds ---" % round(time.time() - start_time, 2))


async def scrape_data():
    print('SCRAPPING DATA')
    results = {}
    results['brands'] = []
    brands = request_ul(URL_BRANDS, 'c_container allmakes')
    append_results(brands, results['brands'])
    # start URLs scrapping
    brands_total = len(results['brands'])
    ii = 0
    for brand in results['brands']:
        ii += 1
        print(f"[{ii}/{brands_total}] {brand['name']}...")
        brand_count = 0
        brand['categories'] = []
        categories = request_ul(brand['url'], 'c_container allmakes allcategories')
        append_results(categories, brand['categories'])
        for category in brand['categories']:
            category['models'] = []
            models = request_ul(category['url'], 'c_container allmodels')
            append_results(models, category['models'])
            async with aiohttp.ClientSession() as session:
                tasks = []
                for model in category['models']:
                    model['model_parts'] = []
                    tasks.append(asyncio.ensure_future(get_model_parts(session, model)))
                res_model_parts = await asyncio.gather(*tasks)
                for model_parts_count in res_model_parts:
                    brand_count += model_parts_count
        print(f"[{ii}/{brands_total}] {brand['name']}...{brand_count:,.0f} parts")
    save_to_json(results)
    print('DATA SCRAPPED')


async def get_model_parts(session, model):
    async with session.get(URL_BASE + '/' + model['url']) as resp:
        page = await resp.text()
        parts = get_ul_from_html(page, 'c_container allparts')
        append_results(parts, model['model_parts'], split_name=True)
        return len(model['model_parts'])


def request_ul(url, class_name):
    page = requests.get(URL_BASE + '/' + url)
    content = page.content
    return get_ul_from_html(content, class_name)


def get_ul_from_html(content, class_name):
    soup = BeautifulSoup(content, 'html.parser')
    try:
        container = soup.find('div', class_=class_name)
        list = container.find('ul')
    except Exception as e:
        return []
    return list.findAll('li')


def append_results(ul, results, split_name=False, limit=5000):
    count = 0
    for li in ul:
        link = li.find('a')
        name = link.get_text().strip()
        name_arr = name.split('-')
        if len(name_arr) > 1 and split_name:
            results.append({
                "code": name_arr[0].strip(), 
                "name": name_arr[1].strip(), 
                "url": link['href']
            })
        else:
            results.append({ "name": name, "url": link['href'] })
        count += 1
        if count > limit:
            break


def save_to_json(results):
    file1 = open('results.json', 'w')
    file1.write(json.dumps(results))
    file1.close()


# CALL STARTPOINT
run()
###############