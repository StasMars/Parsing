import requests
from bs4 import BeautifulSoup
import csv

from Glavsnab.models import Product


def parser(url: str, max_item: int):
    create_csv()
    page = 1
    count_items = 0
    while max_item > count_items:
        list_product = []
        res = requests.get(f'{url}&p={page}')
        soup = BeautifulSoup(res.text, 'lxml')
        products = soup.find_all('div', class_='product-card')

        for product in products:
            if count_items >= max_item:
                break
            count_items += 1
            name = product.get('data-product-name')
            sku = product.find('span', class_='product-card__key').text
            price_elem = product.find('span', itemprop='price')
            if price_elem:
                price = price_elem.get('content')
            else:
                price = 'Цены нет'
            name_elem = product.find('meta', itemprop='name')
            link = name_elem.findNext().get('href')
            list_product.append(Product(sku=sku,
                                        name=name,
                                        price=price,
                                        link=link))
        write_csv(list_product)
        page += 1


def create_csv():
    with open(f'glavsnab.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([
            'sku',
            'name',
            'price',
            'link'
        ])


def write_csv(products: list[Product]):
    with open(f'glavsnab.csv', mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for product in products:
            writer.writerow([
                product.sku,
                product.name,
                product.price,
                product.link
            ])


if __name__ == '__main__':
    parser(url='https://glavsnab.net/santehnika/smesiteli.html?limit=100', max_item=1320)
