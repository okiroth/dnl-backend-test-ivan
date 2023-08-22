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
    asyncio.run(scrape_data())
    save_json_to_DB()
    print("--- %s seconds ---" % round(time.time() - start_time, 2))




async def scrape_data():
    print('SCRAPPING DATA')
    results = {}

    ## First Request
    html = requests.get(URL_BASE + '/' + URL_BRANDS).content
    results['brands'] = process_html(html, 'c_container allmakes')

    urls = 0
    countme = 0

    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False, limit=2000)) as session:

        ## Task Brands
        tasks = []
        for brand in results['brands']:
            tasks.append(asyncio.create_task(fetch(session, brand['url'])))
            urls += 1
        responses_0 = await asyncio.gather(*tasks)

        ## Process Brands Respones ---> Tasks Categories
        for ii, html in enumerate(responses_0):
            brand = results['brands'][ii]
            brand['categories'] = process_html(html, 'c_container allmakes allcategories')

            print(ii, '==============  ' + brand['name'] + '  ==============')

            tasks = []
            for category in brand['categories']:
                tasks.append(asyncio.create_task(fetch(session, category['url'])))
                urls += 1
            responses_1 = await asyncio.gather(*tasks)

            # Process Categories Respones ---> Tasks Models
            for iii, html in enumerate(responses_1):
                category = brand['categories'][iii]
                category['models'] = process_html(html, 'c_container allmodels')

                tasks = []
                for model in category['models']:
                    countme += 1
                    task = asyncio.create_task(fetch(session, model['url']), name=f'model ')

                    task.add_done_callback(progress)
                    tasks.append(task)
                responses_2 = await asyncio.gather(*tasks)

                # Process Parts
                for iiii, html in enumerate(responses_2):
                    model = category['models'][iiii]
                    model['parts'] = process_html(html, 'c_container allparts')

    print('TOTAL parts ' + str(countme))
    print('URLS: ', urls)
    # save_to_json(results)
    print('SCRAPPING DATA DONE')


async def fetch(session, url):
    print(url)
    async with session.get(URL_BASE + '/' + url) as response:
        return await response.text()


def progress(task):
    # report progress of the task
    print(task.get_name())

def process_html(html, class_name, split_name=False):
    res = []
    soup = BeautifulSoup(html, 'html.parser')
    try:
        container = soup.find('div', class_=class_name)
        list = container.find('ul')
    except Exception as e:
        return []
    ul = list.findAll('li')
    for li in ul:
        link = li.find('a')
        name = link.get_text().strip()
        name_arr = name.split('-')
        if len(name_arr) > 1 and split_name:
            res.append({
                'code': name_arr[0].strip(), 
                'name': name_arr[1].strip(), 
                'url': link['href']
            })
        else:
            res.append({ 'name': name, 'url': link['href'] })
    return res


def save_to_json(results):
    file1 = open('results.json', 'w')
    file1.write(json.dumps(results, indent=1))
    file1.close()


# CALL STARTPOINT
run()
###############