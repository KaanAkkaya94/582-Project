
from miltontours.models import Item, Category, Order, OrderStatus, UserInfo, City, Tour
from miltontours.models import UserAccount
from datetime import datetime
from . import mysql

DummyCity = City('0', 'Dummy', 'Dummy city for testing', 'dummy.jpg')

Cities = [
    City('1', 'Sydney', 
        'City in New South Wales with largest population', 
        'sydney.jpg'),
    City('2', 'Brisbane', 
        'City in Queensland with a good weather', 
        'brisbane.jpg'),
    City('3', 'Melbourne',
        'Visit a city in Melbourne and experience all four seasons in a day!',
        'melbourne.jpg')
]

DummyTour = Tour('0', 'Dummy Tour', 'Dummy tour for testing',
                 DummyCity, 'dummy.jpg', 25.25, datetime.now())

Tours = [
    Tour('1', 'Kangaroo point walk',
         'Gentle stroll but be careful of cliffs. Hand feed the kangaroos',
          Cities[1], 't_hand.jpg', 99.00, datetime(2023, 7, 23)),
    Tour('2', 'West End markets',
         'Tour the boutique goods and food and ride the wheel',
         Cities[1], 't_ride.jpg', 20.00,  datetime(2023, 10, 30)),
    Tour('3', 'Whale spotting',
         'Visit the incredible Sydney coast line and see the whales migrating',
         Cities[0], 't_whale.jpg', 129.00,  datetime(2023, 10, 30))
]

DummyUserInfo = UserInfo(
    '0', 'Dummy', 'Foobar', 'dummy@foobar.com', '1234567890'
)

Orders = [
    Order('1', OrderStatus.PENDING, DummyUserInfo, 149.99,
          []),  
    Order('2', OrderStatus.CONFIRMED, DummyUserInfo, 1000.00,
          []) 
]

Users = [
    UserAccount('admin', 'admin', 'foobar@mail.com', 
                UserInfo('1', 'Admin', 'User', 'foobar@mail.com', 
                         '1234567890')
    ),
]

#function to get all items from the db
def get_cities():
    cur = mysql.connection.cursor()
    cur.execute("SELECT itemID, itemName, itemDescription, itemCategory, itemPrice, itemPicture FROM cities")
    results = cur.fetchall()
    cur.close()
    return [Item(str(row['itemID']), row['itemName'], row['itemDescription'], row['itemCategory'], row['itemPrice'], row['itemPicture']) for row in results]

def get_city(itemID):
    cur = mysql.connection.cursor()
    cur.execute("SELECT itemID, itemName, itemDescription, itemCategory, itemPrice, itemPicture FROM cities WHERE itemID = %s", (itemID))
    row = cur.fetchone()
    cur.close()
    return Item(str(row['itemID']), row['itemName'], row['itemDescription'], row['itemCategory'], row['itemPrice'], row['itemPicture']) if row else None


#Function to get all categories from the db
def get_categories():
    """Get all categories."""
    cur = mysql.connection.cursor()
    cur.execute("""SELECT categoryID, categoryName FROM categories
                   JOIN items ON categories.categoryID = items.itemCategory
                   """)
    results = cur.fetchall()
    cur.close()
    return [Category(str(row['categoryID']), row['categoryName'],
                    [Item(str(row['itemID']), row['itemName'], row['itemDescription'],
                           row['itemCategory'], row['itemPrice'])]) for row in results]

#Function to get all categories from the db
def get_category(categoryID):
    """Get a category by its specific ID."""
    cur = mysql.connection.cursor()
    cur.execute("""SELECT categoryID, categoryName FROM categories 
                    JOIN items ON categories.categoryID = items.itemCategory
                    WHERE categories.categoryID = %s
                """, (categoryID))
    row = cur.fetchone()
    cur.close()
    return Category(str(row['categoryID']), row['categoryName']) if row else None

def get_items_for_category(categoryID):
    """Get all items for a given category ID."""
    cur = mysql.connection.cursor()
    cur.executef("""SELECT i.itemID, i.itemName, i.itemDescription, i.itemCategory, i.itemPrice, i.itemPicture
                    FROM items i
                    JOIN categories c ON i.categoryID = c.categoryID
                    WHERE c.categoryID = %s""", (categoryID))
    results = cur.fetchall()
    cur.close()
    return [
            Item(str(row['itemID']), row['itemName'], row['itemDescription'],
                 row['itemCategory'], row['itemPrice'],
                 Category(str(row['categoryID']), row['categoryName']),
                 row['itemPicture'], float(row['itemPrice'])) for row in results
            ]




#Commented out as it is not used in the current implementation

def get_tours():
    """Get all tours."""
    return Tours

def get_tour(tour_id):
    """Get a tour by its ID."""
    tour_id = str(tour_id)
    for tour in Tours:
        if tour.id == tour_id:
            return tour
    return DummyTour

def get_tours_for_city(city_id):
    """Get all tours for a given city ID."""
    city_id = str(city_id)
    return [tour for tour in Tours if tour.city.id == city_id]


def add_to_basket(itemID, quantity=1):
    cur = mysql.connection.cursor()
    cur.execute("SELECT itemID, itemName, itemDescription, itemCategory, itemPrice, itemPicture FROM items WHERE itemID = %s", (itemID))
    row = cur.fetchone()
    cur.close() 
    


#SQL connection to add item to the basket
def add_item_to_basket(basket):
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO basket (itemID, quantity, basketPrice) VALUES (%s, %s, %s)", (basket.user.id, basket.total_cost))
    basket_id = cur.lastrowid
    for item in basket.items:
        cur.execute("INSERT INTO basket_items (basketID, itemID, quantity) VALUES (%s, %s, %s)", (basket_id, item.id, item.quantity))
    mysql.connection.commit()
    cur.close()

#Remove single item from the basket
def remove_item_from_basket(basket, itemID):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM basket_items WHERE basketID = %s AND itemID = %s", (basket.user.id, itemID))
    mysql.connection.commit()
    cur.close()

#Remove all items from the basket
def remove_all_items_from_basket(basket):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM basket WHERE userID = %s", (basket.user.id))
    mysql.connection.commit()
    cur.close()


#SQL query to add a new category to the database
def add_city(category):
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO categories(categoryName) VALUES (%s)", (category.name))
    mysql.connection.commit()
    cur.close()

#SQL query to add a new tour to the database
def add_tour(item):
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO items(itemName, itemDescription, itemCategory, itemPrice, itemPicture) VALUES (%s, %s, %s, %s, %s)", (item.name, item.description, item.category.name, item.price, item.picture))
    mysql.connection.commit()
    cur.close()






#function to add item to the basket of the user
def add_to_basket(itemID, quantity = 1):
    basket = get_basket()
    basket.add_item(BasketItem(item=get_item(itemID), quantity=quantity))
    _save_basket_to_session(basket)

#fucntion to remove item from the basket of the user
def remove_from_basket(itemID, quantitiy=1):
    basket = get_basket()
    basket.remove_item(basket_item_id)
    _save_basket_to_session(basket)


#mine
def add_tour(tour):
    """Add a new tour."""
    Tours.append(tour)

# SQL query to get the basket of the user
def get_order(basketID):
    cur = mysql.connection.cursor()
    cur.execute("SELECT orderID, userID, basketPrice, userName, userEmail, userPhoneNumber FROM basket WHERE orderID = %s", (basketID))
    row = cur.fetchone()
    cur.close()
    return Basket[str(row('basketID')), 
                     UserInfo(str(row['userID']), row['userName'], row['userEmail'], row['userPhoneNumber']),
                     float(row['basketPrice']) if row else None ]

# SQL query to get all orders of the user
def get_orders():
    cur = mysql.connection.cursor()
    cur.execute("SELECT orderID, userID, basketPrice, userName, userEmail, userPhoneNumber FROM basket")
    row = cur.fetchall()
    cur.close()
    return Basket[str(row('basketID')), 
                     UserInfo(str(row['userID']), row['userName'], row['userEmail'], row['userPhoneNumber']),
                     float(row['basketPrice']) if row else None ]



def get_orders():
    """Get all orders."""
    return Orders

def get_order(order_id):
    """Get an order by its ID."""
    order_id = str(order_id)
    for order in Orders:
        if order.id == order_id:
            return order
    return None  # or raise an exception if preferred


def check_for_user(username, password):
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT userID,userName, userPassword, userFirstName, userLastName, userEmail, userPhoneNumber, userAdress, userState, userPostcode,
        FROM users
        WHERE userName = %s AND user_password = %s
    """, (username, password))
    row = cur.fetchone()
    cur.close()
    if row:
        return UserAccount(row['userName'], row['userPassword'], row['userEmail'],
                           UserInfo(str(row['userID']), row['userFirstName'], row['userLastName'],
                                    row['userEmail'], row['userPhoneNumber']))
    return None

def is_admin(userID):
    """Check if a user is an admin."""
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM admins WHERE user_id = %s", (userID,))
    row = cur.fetchone()
    cur.close()
    return True if row else False

def add_user(form):
    cur = mysql.connection.cursor()
    cur.execute("""
        INSERT INTO users (userName, userPassword, userEmail, userFirstName, userLastName, userPhoneNumber, userAdress, userState, userPostcode)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (form.username.data, form.password.data, form.email.data,
          form.firstname.data, form.surname.data, form.phone.data, form.address.data,
          form.state.data, form.postcode.data))
    mysql.connection.commit()
    cur.close()

