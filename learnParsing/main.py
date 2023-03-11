import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import re
import csv


def get_data(url):
    date = datetime.now()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
    }
    # получаем страницу с акциями и сохраняем ее в index.html
    req = requests.get(url=url, headers=headers)

    with open("index.html", 'w') as file:
        file.write(req.text)

    with open("index.html", 'r') as file:
        src = file.read()

    # сбор категорий и ссылок
    soup = BeautifulSoup(src, "lxml")

    categories = soup.find_all(class_="sales-list__item")
    categories_dict = {}

    for cat in categories:
        cat_name = cat.find(class_="sales-list__title").text.strip()

        rep = [',', ' ', '-', '\xa0', '\xad']
        for item in rep:
            if item in cat_name:
                cat_name = cat_name.replace(item, "_")

        cat_link = "https://7745.by" + cat.get('href').strip()
        categories_dict[cat_name] = cat_link

    # запись категорий и ссылок в json
    with open("categories_dict.json", 'w') as file:
        json.dump(categories_dict, file, indent=4, ensure_ascii=False)

    with open("categories_dict.json") as file:
        categories_dict = json.load(file)

    # сбор данных каждой категории


    for category_name, category_link in categories_dict.items():

        with open(f"data/{category_name}_{date.strftime('%Y_%b_%d')}.csv", 'w', newline = '') as file:
            writer = csv.writer(file)
            writer.writerow(
                (
                    'Name',
                    'Link',
                    'Old price',
                    'New price',
                    'Discount'
                )
            )


        category_page = requests.get(url=category_link, headers=headers)
        soup_cat = BeautifulSoup(category_page.text, 'lxml')

        try:
            page_count = int(soup_cat.find_all('a', class_='pagination-point active')[-1].text)
        except Exception:
            page_count = 0

        print(f'Обрабатываю категорию {category_name}. Всего страниц - {page_count}')

        for page in range(1, page_count + 1):

            res = requests.get(url=f'{category_link}/{page}', headers=headers)
            soup_cpp = BeautifulSoup(res.text, 'lxml')

            products = soup_cpp.find_all('div', class_='catalog-item__wrapper')

            #products_list = []
            for item in products:
                try:
                    product_name = item.find('a', class_='item-block_name').text.strip()
                    product_name = re.sub(r'(\n)|( )|(\.)|(\xa0)|(\r)|(\xd7)', '', product_name)
                except:
                    product_name = 'No_product_name'
                try:
                    product_link = item.find('a', class_='item-block_name').get('href').strip()
                    product_link = 'https://7745.by' + re.sub(r'(\n)|( )|(\.)|(\xa0)|(\r)|(\xd7)', '', product_link)
                except:
                    product_link = 'No_product_link'
                try:
                    product_price_old = item.find('div', class_="item-block_secondary-price").find_all('span')[-1].text.strip()
                    product_price_old = re.sub(r'(\n)|( )|(\.)|(\xa0)|(\r)|(\xd7)', '', product_price_old)
                except:
                    product_price_old = 'No_old_price'
                try:
                    product_price_new = item.find('div', {'class': re.compile((r'item-block_main-price-block'))}).text.strip()
                    product_price_new = re.sub(r'(\n)|( )|(\.)|(\xa0)|(\r)|(\xd7)', '', product_price_new)
                except:
                    product_price_new = 'No_new_price'
                try:
                    product_discount = item.find('span', class_="product-sale-sticker__value product-sale-sticker__value--tile").text.strip()
                    product_discount = re.sub(r'(\n)|( )|(\.)|(\xa0)|(\r)|(\xd7)', '', product_discount)
                except:
                    product_discount = 'No_discount'
                #products_list.append([product_name, 'https://7745.by' + product_link, re.sub(r'(\n)|( )|(\.)|(\xa0)|(\r)', '', product_price_new), re.sub(r'(\n)|( )|(\.)|(\xa0)|(\r)', '', product_price_old), re.sub(r'(\n)|( )|(\.)|(\xa0)|(\r)', '', product_discount)])

                with open(f"data/{category_name}_{date.strftime('%Y_%b_%d')}.csv", 'a', newline = '') as file:
                    writer = csv.writer(file)
                    writer.writerow(
                        [
                            product_name,
                            product_link,
                            product_price_old,
                            product_price_new,
                            product_discount
                        ]
                    )

            print(f'Обработал {page} из {page_count} страниц.')



def main():
    url = "https://7745.by/sale"
    get_data(url)


if __name__ == "__main__":
    main()