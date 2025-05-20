from dataclasses import dataclass, field
from datetime import datetime
from typing import List
from enum import Enum

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
@dataclass
class City:
    id: str
    name: str
    description: str = 'fooobar'
    price = float
    image: str = 'foobar.png'
    


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
class Item:
    def __init__(self, id, name, description, category, price, image):
        self.id = id
        self.name = name
        self.description = description
        self.category = category
        self.price = price
        self.image = image

@dataclass
class Category:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        

    def __repr__(self):
        str = "ID: {}, Name: {}, Description: {}, Category: {}, Price: {} \n" 
        str = str.format( self.id, self.name, self.description, self.category, self.price)
        return str

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
    id: str
    tour: Tour
    quantity: int = 1

    def total_price(self):
        """Calculate the total price for this basket item."""
        return self.tour.price * self.quantity
    
    def increment_quantity(self):
        """Increment the quantity of this basket item."""
        self.quantity += 1

    def decrement_quantity(self):
        """Decrement the quantity of this basket item."""
        if self.quantity > 1:
            self.quantity -= 1

@dataclass
class Basket:
    items: List[BasketItem] = field(
        default_factory=lambda: [])

    def add_item(self, item: BasketItem):
        """Add a tour to the basket."""
        self.items.append(item)

    def remove_item(self, item: BasketItem):
        """Remove a tour from the basket by its ID."""
        self.items = [tour for tour in self.items if tour.id != item.id]

    def get_item(self, item_id: str):
        """Get a tour from the basket by its ID."""
        for item in self.items:
            if item.id == item_id:
                return item
        return None
    
    def empty(self):
        """Empty the basket."""
        self.items = []
    
    def total_cost(self):
        """Calculate the total cost of the basket."""
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