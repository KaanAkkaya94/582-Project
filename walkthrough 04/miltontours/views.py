from flask import Blueprint, render_template, request, session, flash, redirect, session, url_for
from flask import redirect, url_for

from hashlib import sha256

from miltontours.db import get_orders, check_for_user

from miltontours.db import get_categories, get_items_for_category, get_category

from miltontours.session import get_basket, add_to_basket, remove_from_basket, empty_basket, convert_basket_to_order
from miltontours.forms import NewCheckoutForm, LoginForm, RegisterForm
from werkzeug.security import generate_password_hash, check_password_hash

#groups all names under the namespace
bp = Blueprint('main', __name__)

#if homepages get visited, gets all cities
@bp.route('/')
def index():
    return render_template('index.html', categories = get_categories())

@bp.route('/tours/<int:categoryid>/')
def products(categoryid):
    products = get_items_for_category(categoryid)
    return render_template('products.html', products = products, category= get_category(categoryid))


@bp.route('/order/', methods = ['POST', 'GET'])
def order():

    product_id = request.args.get('product_id')
    # is this a new order?
    if 'order_id'not in session:
        session['order_id'] = 1 # arbitry, we could set either order 1 or order 2
    
    #retrieve correct order object
    order = get_basket()
    # are we adding an item? - will be implemented later with DB
    if product_id:
        print('user requested to add product id = {}'.format(product_id))

    return render_template('order.html', order = order, totalprice = order.total_cost())

@bp.post('/basket/<int:product_id>/')
def adding_to_basket(product_id):
    add_to_basket(product_id)
    return redirect(url_for('main.order'))

@bp.post('/basket/<int:tour_id>/<int:quantity>/')
def adding_to_basket_with_quantity(tour_id, quantity):
    add_to_basket(tour_id, quantity)
    return redirect(url_for('main.order'))

@bp.post('/clearbasket/')
def clear_basket():
    empty_basket()
    flash('Basket cleared.')
    return redirect(url_for('main.order'))

@bp.post('/removebasketitem/<string:item_id>/')
def remove_basketitem(item_id):
    basket = get_basket()
    item = basket.get_item(item_id)

    if item:
        flash(f"Removed '{item.product.name}' from basket.")
        remove_from_basket(item_id)
    else:
        flash("Item not found in basket.", "warning")

    return redirect(url_for('main.order'))

# This is to checkout the order with updated information
@bp.route('/checkout/', methods = ['POST', 'GET'])
def checkout():
    form = NewCheckoutForm() 
    if request.method == 'POST':
        
        #retrieve correct order object
        order = get_basket()
       
        if form.validate_on_submit():
            order.status = True
            order.firstname = form.firstname.data
            order.surname = form.surname.data
            order.email = form.email.data
            order.phone = form.phone.data
            order.address = form.address.data
            order.city = form.city.data
            order.postcode = form.postcode.data
            order.state = form.state.data
            order.delivery = form.delivery.data
            order.payment = form.payment.data

            flash('Thank you for your information, your order is being processed!',)
            order = convert_basket_to_order(get_basket())
            empty_basket()
            # add_order(order)
            print('Number of orders in db: {}'.format(len(get_orders())))
            return redirect(url_for('main.index'))
        else:
            flash('The provided information is missing or incorrect',
                  'error')

    return render_template('checkout.html', form = form)


@bp.route('/login/', methods = ['POST', 'GET'])
def login():
    form = LoginForm()
    if request.method == 'POST':

        if form.validate_on_submit():
            form.password.data = sha256(form.password.data.encode()).hexdigest()
            # Check if the user exists in the database
            user = check_for_user(
                form.username.data, form.password.data
            )
            if not user:
                flash('Invalid username or password', 'error')
                return redirect(url_for('main.login'))

            #Store user information in the session
            session['user'] = {                
                'user_id': user.id,
                'userName' : user.username,
                'userPassword' : user.userpassword,
                'firstname': user.firstname,
                'surname': user.surname,
                'phone': user.phone
                # 'is_admin': is_admin(user.info.id),
            }
            #session['username']=user.username
            #session['userpassword']=user.userpassword

            session['logged_in'] = True
            flash('Login successful!')
            return redirect(url_for('main.index'))

    return render_template('login.html', form = form)




# For registering a new user and logging out, we will use the RegisterForm class
#Keeping it commented out for now, as we are not using it yet


# # This is to logout the user
# @bp.route('/logout')
# def logout():
#     session.clear()
#     flash('Logged out.')
#     return redirect(url_for('auth.login'))


# # This is to register a new user
# bp.route('/register', methods=['GET', 'POST'])
# def register():
#     form = RegisterForm()
#     if form.validate_on_submit():
#         username = form.username.data
#         email = form.email.data
#         password = generate_password_hash(form.password.data)

#         cursor = mysql.connection.cursor()
#         cursor.execute("INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)",
#                        (username, email, password))
#         mysql.connection.commit()
#         cursor.close()
#         flash('Registration successful! Please login.')
#         return redirect(url_for('auth.login'))
#     return render_template('register.html', form=form)
