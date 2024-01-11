import requests
from bs4 import BeautifulSoup
import csv

from model import Product


def parser(url: str):
    create_csv()
    list_product = []
    res = requests.get(url=url)
    soup = BeautifulSoup(res.text, 'lxml')
    products = soup.find_all('div', class_='popular_item col-xs-6 col-sm-4')

    for product in products:
        cod = product.find('div', 'list-product-art').text
        name = product.find('a', class_='popular_name').text
        price = product.find('span', class_='poular_price').text
        link = product.find('a', class_='popular_name').get('href')
        list_product.append(Product(cod=cod,
                                    name=name,
                                    price=price,
                                    link=link
                                    ))
    write_csv(list_product)


def create_csv():
    with open(f'Clothes.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([
            'cod',
            'name',
            'price',
            'link'
        ])


def write_csv(products: list[Product]):
    with open(f'Clothes.csv', mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for product in products:
            writer.writerow([
                product.cod,
                product.name,
                product.price,
                product.link
            ])


if __name__ == '__main__':
    parser(url='https://unitorg-amur.ru/catalog/kempingovaya_mebel/')
