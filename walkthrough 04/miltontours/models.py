from dataclasses import dataclass, field
from datetime import datetime
from typing import List
from enum import Enum
from uuid import uuid4

#KILL
class OldCity:
    def __init__(self, id, name, description, image, price):
        self.id = id
        self.name = name
        self.description = description
        self.image = image
        self.price = price

    def get_city_details(self):
        return str(self)

    def __repr__(self):
        str = "ID: {}, Name: {}, Description: {}, Image: {} \n"
        str = str.format( self.id, self.name, self.description, self.image)
        return str

# we can save ourselves some time by using the dataclass decorator
# to create the class and its methods
# this will create the __init__ and __repr__ methods for us
# and we can add our own methods as needed

#KILL
@dataclass
class City:
    id: str
    name: str
    description: str = 'fooobar'
    price = float
    image: str = 'foobar.png'


#KILL
@dataclass
class Tour:
    id: str
    name: str
    description: str
    city: City
    image: str = 'foobar.png'
    price: float = 10.00
    date: datetime = field(
        default_factory=lambda: datetime.now()
    )

@dataclass
class Category:
    id: str
    name: str

@dataclass
class Item:
    id: str
    name: str
    description: str
    category: Category
    price: float


class OrderStatus(Enum):
    PENDING = 'Pending'
    CONFIRMED = 'Confirmed'
    CANCELLED = 'Cancelled'

@dataclass
class UserInfo:
    id: str
    firstname: str
    surname: str
    email: str
    phone: str

@dataclass 
class BasketItem:
    product: Item
    quantity: int = 1
    id: str = field(default_factory=lambda: str(uuid4()))

    def total_price(self):
        return self.product.price * self.quantity

    def increment_quantity(self):
        self.quantity += 1

    def decrement_quantity(self):
        if self.quantity > 1:
            self.quantity -= 1

@dataclass
class Basket:
    userID: int
    items: List[BasketItem] = field(default_factory=lambda: [])

    def add_item(self, item: BasketItem):
        self.items.append(item)

    def remove_item(self, item_id: str):
        self.items = [item for item in self.items if item.id != item_id]

    def get_item(self, item_id: str):
        for item in self.items:
            if item.id == item_id:
                return item
        return None

    def empty(self):
        self.items = []

    def total_cost(self):
        return sum(item.total_price() for item in self.items)


@dataclass
class Order:
    id: str
    status: OrderStatus
    user: UserInfo
    total_cost: float = 0.0
    items: List[BasketItem] = field(
        default_factory=list,
        init=True)
    date: datetime = field(
        default_factory=lambda: datetime.now(),
        init=True)
    

@dataclass
class UserAccount:
    username: str
    password: str
    email: str
    info: UserInfo


    
