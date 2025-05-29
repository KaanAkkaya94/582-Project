DROP database Fastmeds;
create database Fastmeds;
use Fastmeds;

create table categories(
	categoryID int auto_increment primary key, 
    categoryName varchar(20) not null unique
);

insert into categories (categoryName) values
('Analgesics'),
('Antibacterials'),
('Antibiotics'),
('Cough Supressants'),
('Hormones'),
('Laxatives'),
('Sedatives'),
('Sleeping Drugs'),
('Vitamins');


create table cities(
	itemID int auto_increment not null primary key,
    itemName varchar(50) not null,
    itemDescription varchar(250) not null,
    itemCategory int,
    itemPrice float,
    itemPicture varchar(255) not null default 'default.jpg',
    foreign key (itemCategory) references categories(categoryID)
);

insert into cities (itemName, itemDescription, itemCategory, itemPrice) values
# Analgesics
('Paramol 500mg', 'Generic description for medicine.', 1, 4.99),
('Irofen 200mg', 'Generic description for medicine.', 1, 4.99),
# Antibacterials
('Pemacillin 100mg', 'Generic description for medicine.', 2, 4.99),
('Pernocyillin 50mg', 'Generic description for medicine.', 2, 4.99),
# Antibiotics
('Axillin', 'Generic description for medicine.', 3, 4.99),
('Azromycin 250mg', 'Generic description for medicine.', 3, 4.99),
# Cough Suppressants
('Dexthorphan Syrup', 'Generic description for medicine.', 4, 4.99),
('Benaryl Cough Liquid', 'Generic description for medicine.', 4, 4.99),
# Hormones
('Traxine 100mcg', 'Generic description for medicine.', 5, 4.99),
('Meraxine 200mcg', 'Generic description for medicine.', 5, 4.99),
# Laxatives
('Ena Laxative Tablets', 'Generic description for medicine.', 6, 4.99),
('Latulose Solution', 'Generic description for medicine.', 6, 4.99),
# Sedatives
('Dizepam 5mg', 'Generic description for medicine.', 7, 4.99),
('Limozepam 1mg', 'Generic description for medicine.', 7, 4.99),
# Sleeping Drugs
('Metonin 3mg', 'Generic description for medicine.', 8, 4.99),
('Zolone 7.5mg', 'Generic description for medicine.', 8, 4.99),
# Vitamins
('Vitamin C 1000mg', 'Generic description for medicine.', 9, 4.99),
('Multivitamin Daily', 'Generic description for medicine.', 9, 4.99);





select i.itemName as city, c.categoryName as categories, i.itemDescription AS description, i.itemPrice AS price
from cities i
join categories c on i.itemCategory = c.categoryID
order by c.categoryName;


create table paymentOptions(
	paymentID int auto_increment primary key, 
    PaymentOption varchar(20) not null unique
);
create table deliveryOptions(
	deliveryID int auto_increment primary key, 
    deliveryOption varchar(25) not null unique
);


create table basket(
		basketID int auto_increment not null primary key,
        userID int,
        paymentOptionID int not null,
        deliveryOptionID int not null,
        createdAt timestamp default current_timestamp,
        basketPrice float not null,
        foreign key (paymentOptionID) references paymentOptions (paymentID),
        foreign key (deliveryOptionID) references deliveryOptions (deliveryID)
);


create table users(
	userID int auto_increment not null primary key,
    basketID int,
    userName varchar(50) unique not null,
    userPassword varchar(255) not null,
    userFirstName varchar(20) not null,
    userLastName varchar(20) not null,
    userEmail varchar(50) unique not null,
    userPhoneNumber varchar(20) not null,
    userAdress varchar(50) not null,
    userState varchar(10) not null,
    userPostcode int not null,
    foreign key (basketID) references basket(basketID)
);

create table admins(
	userID int auto_increment not null primary key
);

insert into admins (userID) values
(1),
(2);

CREATE TABLE orders (
    orderID INT AUTO_INCREMENT PRIMARY KEY,
    userID int,
    order_status ENUM('Pending', 'Confirmed', 'Cancelled') DEFAULT 'Confirmed',
    order_delivery_type varchar(50) not null,
    total_cost DECIMAL(10,2),
    order_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    userFirstName varchar(20) not null,
    userLastName varchar(20) not null,
    userEmail varchar(50) unique not null,
    userPhoneNumber varchar(20) not null,
    FOREIGN KEY (userID) REFERENCES users(userID) ON DELETE SET NULL
);

CREATE TABLE order_items (
    order_item_id INT AUTO_INCREMENT PRIMARY KEY,
    orderID INT,
    itemID INT,
    quantity INT DEFAULT 1,
    FOREIGN KEY (orderID) REFERENCES orders(orderID) ON DELETE CASCADE,
    FOREIGN KEY (itemID) REFERENCES cities(itemID)
);



#changed basket(paymentOption) to paymentOptions(paymentoption)
insert into  paymentOptions (paymentOption) values
('Credit Card'),
('Bank Transfer'),
('Paypal'),
('Wise');


insert into deliveryOptions (deliveryOption) values
('Normal Delivery'),
('Express Delivery'),
('Eco-Friendly Delivery'),
('Store Pick-Up');

-- Orders (linked to user)
-- INSERT INTO orders (userID, order_status, total_cost, userFirstName, userLastName, userEmail, userPhoneNumber)
-- VALUES
-- (1, 'Pending', 149.99, 'Dummy', 'Foobar', 'dummy@foobar.com', '1234567890'),
-- (1, 'Confirmed', 1000.00, 'Dummy', 'Foobar', 'dummy@foobar.com', '1234567890');

-- Order items
-- INSERT INTO order_items (orderID, itemID, quantity) VALUES
-- (1, 1, 1),
-- (1, 3, 1),
-- (2, 2, 2);
