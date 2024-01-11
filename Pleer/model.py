from dataclasses import dataclass


@dataclass
class Product:
    cod: str
    name: str
    price: float
    link: str