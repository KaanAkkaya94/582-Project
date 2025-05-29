
from miltontours.models import Item, Category, Order, OrderStatus, UserInfo, City, Tour
from miltontours.models import UserAccount, Basket
from datetime import datetime
from . import mysql

DummyUserInfo = UserInfo(
    '0', 'Dummy', 'Foobar', 'dummy@foobar.com', '1234567890'
)

Users = [
    UserAccount('admin', 'admin', 'foobar@mail.com',
                UserInfo('1', 'Admin', 'User', 'foobar@mail.com',
                         '1234567890')
    ),
]

#function to get all items from the db
def get_cities():
    cur = mysql.connection.cursor()
    cur.execute("SELECT itemID, itemName, itemDescription, itemCategory, itemPrice FROM cities")
    results = cur.fetchall()
    cur.close()
    return [Item(str(row['itemID']), row['itemName'], row['itemDescription'], row['itemCategory'], row['itemPrice']) for row in results]

# def get_product(itemID):
#     cur = mysql.connection.cursor()
#     cur.execute("SELECT itemID, itemName, itemDescription, itemCategory, itemPrice, itemPicture FROM cities WHERE itemID = %s", (itemID,))
#     row = cur.fetchone()
#     cur.close()
#     return Item(str(row['itemID']), row['itemName'], row['itemDescription'], row['itemCategory'], row['itemPrice']) if row else None

def get_product(itemID):
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT p.itemID, p.itemName, p.itemDescription, p.itemPrice, p.itemPicture,
               c.categoryID, c.categoryName
        FROM cities p
        JOIN categories c ON p.itemCategory = c.categoryID
        WHERE p.itemID = %s
    """, (itemID,))
    row = cur.fetchone()
    cur.close()
    return Item(str(row['itemID']), row['itemName'], row['itemDescription'],
                Category(str(row['categoryID']), row['categoryName']), float(row['itemPrice']) ) if row else None

#Function to get all categories from the db
def get_categories():
    cur = mysql.connection.cursor()
    cur.execute("SELECT categoryID, categoryName FROM categories")
    results = cur.fetchall()
    cur.close()
    return [Category(str(row['categoryID']), row['categoryName']) for row in results]

def get_category(categoryID):
    """Get a category by its specific ID."""
    cur = mysql.connection.cursor()
    cur.execute("""SELECT categoryID, categoryName FROM categories 
                   WHERE categoryID = %s""", (categoryID,))
    row = cur.fetchone()
    cur.close()
    return Category(str(row['categoryID']), row['categoryName']) if row else None

def get_items_for_category(categoryID):
    """Get all items for a given category ID."""
    cur = mysql.connection.cursor()
    cur.execute("""SELECT i.itemID, i.itemName, i.itemDescription, i.itemCategory,
                          i.itemPrice, i.itemPicture,
                          c.categoryID, c.categoryName
                   FROM cities i
                   JOIN categories c ON i.itemCategory = c.categoryID
                   WHERE c.categoryID = %s""", (categoryID,))

    results = cur.fetchall()
    cur.close()

    return [
        Item(str(row['itemID']), row['itemName'], row['itemDescription'],
             row['itemCategory'], row['itemPrice'])
        for row in results
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




# from miltontours.models import Basket, BasketItem, get_item
# from miltontours.session import get_basket, _save_basket_to_session
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
    cur.execute("SELECT basketID, userID, basketPrice FROM basket WHERE basketID = %s", (basketID))
    row = cur.fetchone()
    cur.close()
    if row:
        # row[0] = basketID, row[1] = userID, row[2] = basketPrice
        return Basket(str(row[0]), UserInfo(str(row[1])), float(row[2]))
    return None
    # return Basket[str(row['basketID']), 
    #                  UserInfo(str(row['userID'])), 
    #                  float(row['basketPrice']) if row else None ]

# SQL query to get all orders of the user
def get_orders():
    cur = mysql.connection.cursor()
    cur.execute("SELECT basketID, userID, basketPrice FROM basket")
    rows = cur.fetchall()
    cur.close()
    return [
        Basket(str(row[0]), UserInfo(str(row[1])), float(row[2]))
        for row in rows
    ]
    # return Basket[str(row['basketID']), 
    #                  UserInfo(str(row['userID'])), 
    #                  float(row['basketPrice']) if row else None ]

def search_items(query):
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT i.itemID, i.itemName, i.itemDescription, i.itemCategory, i.itemPrice, i.itemPicture,
               c.categoryID, c.categoryName
        FROM cities i
        JOIN categories c ON i.itemCategory = c.categoryID
        WHERE i.itemName LIKE %s OR i.itemDescription LIKE %s
    """, (query + '%', query + '%'))
    rows = cur.fetchall()
    cur.close()

    return [
        Item(
            str(row['itemID']),
            row['itemName'],
            row['itemDescription'],
            Category(str(row['categoryID']), row['categoryName']),
            float(row['itemPrice'])
        )
        for row in rows
    ]



# def get_orders():
#     """Get all orders."""
#     return Orders

# def get_order(order_id):
#     """Get an order by its ID."""
#     order_id = str(order_id)
#     for order in Orders:
#         if order.id == order_id:
#             return order
#     return None  # or raise an exception if preferred


def check_for_user(username, password):
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT userID,userName, userPassword, userFirstName, userLastName, userEmail, userPhoneNumber, userAdress, userState, userPostcode
        FROM users WHERE userName = %s AND userPassword = %s
    """, (username, password))
    row = cur.fetchone()
    cur.close()
    if row:
        return UserAccount(row['userName'], row['userPassword'], row['userEmail'],
                           UserInfo(str(row['userID']), row['userFirstName'], row['userLastName'],
                                    row['userEmail'], row['userPhoneNumber']))
    return None

def is_admin(user_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM admins WHERE userID = %s", (user_id,))
    row = cur.fetchone()
    cur.close()
    return True if row else False

def add_user(form):
    try:    
        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO users (userName, userPassword, userEmail, userFirstName, userLastName, userPhoneNumber, userAdress, userState, userPostcode)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (form.username.data, form.password.data, form.email.data,
            form.firstname.data, form.surname.data, form.phone.data, form.address.data,
            form.state.data, form.postcode.data))
        mysql.connection.commit()
        cur.close()
        return True
    except Exception as e:
        print(e)
        return False

def user_already_exists(username, useremail):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE userName = %s OR userEmail = %s", (username, useremail))
    row = cur.fetchone()
    cur.close()
    return True if row else False

def add_category(category):
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO categories (categoryName) VALUES (%s)",
                (category.name, ))
    mysql.connection.commit()
    cur.close()

def add_product(product):
    cur = mysql.connection.cursor()
    cur.execute("""
        INSERT INTO cities (itemCategory, itemName, itemDescription, , itemPrice)
        VALUES (%s, %s, %s, %s)
    """, (int(product.category.id), product.name, product.description, float(product.price) ))
    mysql.connection.commit()
    cur.close()
