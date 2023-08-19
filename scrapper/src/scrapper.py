import requests
from bs4 import BeautifulSoup
import json
from db_save import save_data_to_DB
import threading
import time


URL_BASE = 'https://www.urparts.com'

def req_url(url, results, class_name, split_name=False, limit=5000):
    page = requests.get(URL_BASE + '/' + url)
    content = page.content
    soup = BeautifulSoup(content, 'html.parser')
    try:
        container = soup.find('div', class_=class_name)
        list = container.find('ul')
    except Exception as e:
        return
    count = 0
    for li in list.findAll('li'):
        link = li.find('a')
        name = link.get_text().strip()
        name_arr = name.split(' - ')
        if len(name_arr) > 1 and split_name:
            results.append({"code": name_arr[0], "name": name_arr[1], "url": link['href']})
        else:
            results.append({ "name": name, "url": link['href'] })
        count += 1
        if count > limit:
            break
    return count

def scrap_thread(category, brand, model):
        model['model_parts'] = []
        parts = req_url(model['url'], model['model_parts'], 'c_container allparts', split_name=True)
        print(f"{brand['name']} -> {category['name']} -> {model['name']} -> {parts} parts")

def scrape_data():
    print('SCRAPPING DATA')
    results = {}
    results['brands'] = []
    req_url('index.cfm/page/catalogue', results['brands'], 'c_container allmakes')

    # start URLs scrapping
    threads = []
    for brand in results['brands']:
        brand['categories'] = []
        req_url(brand['url'], brand['categories'], 'c_container allmakes allcategories')
        for category in brand['categories']:
            # the server slows down if we don't wait between requests
            # time.sleep(1)
            category['models'] = []
            req_url(category['url'], category['models'], 'c_container allmodels')
            for model in category['models']:
                thread = threading.Thread(target=scrap_thread, args=(category, brand, model,))
                thread.start()
                threads.append(thread)
    # Wait for all threads to finish
    for thread in threads:
        thread.join()
        
    # save data to json file
    file1 = open('results.json', 'w')
    file1.write(json.dumps(results))
    file1.close()
    print('DATA SCRAPPED')

start_time = time.time()
scrape_data()
save_data_to_DB()
print("--- %s seconds ---" % round(time.time() - start_time, 2))


