import requests
from bs4 import BeautifulSoup
import csv

from model import Product


def parser(url: str):
    create_csv()
    list_product = []
    res = requests.get(url=url)
    soup = BeautifulSoup(res.text, 'lxml')
    products = soup.find_all('div', class_='catalog-product')
    for product in products:
        cod = product.find('span', class_='highlight').text
        name = product.find('span', itemprop='name').text
        price = product.find('span', class_='price').text
        dilivery = product.find('span', class_='product-delivery__item-value').text
        link = product.find('a', itemprop='url').get('href')
        list_product.append(Product(cod=cod,
                                    name=name,
                                    price=price,
                                    dilivery=dilivery,
                                    link=link))
    write_csv(list_product)


def create_csv():
    with open(f'order.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([
            'cod',
            'name',
            'price',
            'dilivery',
            'link'
        ])


def write_csv(products: list[Product]):
    with open(f'order.csv', mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for product in products:
            writer.writerow([
                product.cod,
                product.name,
                product.price,
                product.dilivery,
                product.link
            ])


if __name__ == '__main__':
    parser(url="https://poryadok.ru/catalog/nozhi_kukhonnye/?count=120")
