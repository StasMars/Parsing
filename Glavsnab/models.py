from dataclasses import dataclass


@dataclass
class Product:
    sku: int
    name: str
    price: str
    link: str
