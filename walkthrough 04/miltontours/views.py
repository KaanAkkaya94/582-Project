from flask import Blueprint, render_template, request, session, flash, redirect, session, url_for
from flask import redirect, url_for

from miltontours.db import add_order, get_orders, check_for_user
from miltontours.db import get_cities, get_city, get_tours_for_city
from miltontours.session import get_basket, add_to_basket, empty_basket, convert_basket_to_order
from miltontours.forms import NewCheckoutForm, LoginForm, RegisterForm
from werkzeug.security import generate_password_hash, check_password_hash
from miltontours.db import add_user
from hashlib import sha256

#groups all names under the namespace
bp = Blueprint('main', __name__)

#if homepages get visited, gets all cities
@bp.route('/')
def index():
    return render_template('index.html', cities = get_cities())

@bp.route('/tours/<int:cityid>/')
def citytours(cityid):
    citytours = get_tours_for_city(cityid)
    return render_template('citytours.html', tours = citytours, city= get_city(cityid))


@bp.route('/order/', methods = ['POST', 'GET'])
def order():

    tour_id = request.args.get('tour_id')
    # is this a new order?
    if 'order_id'not in session:
        session['order_id'] = 1 # arbitry, we could set either order 1 or order 2
    
    #retrieve correct order object
    order = get_basket()
    # are we adding an item? - will be implemented later with DB
    if tour_id:
        print('user requested to add tour id = {}'.format(tour_id))

    return render_template('order.html', order = order, totalprice = order.total_cost())

@bp.post('/basket/<int:tour_id>/')
def adding_to_basket(tour_id):
    add_to_basket(tour_id)
    return redirect(url_for('main.order'))

@bp.post('/basket/<int:tour_id>/<int:quantity>/')
def adding_to_basket_with_quantity(tour_id, quantity):
    add_to_basket(tour_id, quantity)
    return redirect(url_for('main.order'))

@bp.post('/clearbasket/')
def clear_basket():
    print('User wants to clear the basket')
    # TODO
    return redirect(url_for('main.order'))

@bp.post('/removebasketitem/<int:item_id>/')
def remove_basketitem(item_id):
    print('User wants to delete basket item with id={}'.format(item_id))
    # TODO
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
            add_order(order)
            print('Number of orders in db: {}'.format(len(get_orders())))
            return redirect(url_for('main.index'))
        else:
            flash('The provided information is missing or incorrect',
                  'error')

    return render_template('checkout.html', form = form)





# route for register and password encode
@bp.route('/register/', methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            form.password.data = sha256(form.password.data.encode()).hexdigest()
            # Check if the user already exists
            user = check_for_user(form.username.data, form.password.data)
            if user:
                flash('User already exists', 'error')
                return redirect(url_for('main.register'))

            add_user(form)
            flash('Registration successful!')
            return redirect(url_for('main.login'))

    return render_template('register.html', form=form)

# log in page route
@bp.route('/login/', methods=['POST', 'GET'])
def login():
    form = LoginForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            form.password.data = sha256(form.password.data.encode()).hexdigest()
            user = check_for_user(form.username.data, form.password.data)
            if not user:
                flash('Invalid username or password', 'error')
                return redirect(url_for('main.login'))

            # Store full user info in session
            session['user'] = {
                'user_id': user.info.id,
                'firstname': user.info.firstname,
                'surname': user.info.surname,
                'email': user.info.email,
                'phone': user.info.phone,
                # 'is_admin': is_admin(user.info.id),
            }
            session['logged_in'] = True
            flash('Login successful!')
            return redirect(url_for('main.index'))

    return render_template('login.html', form=form)
#  logout page
@bp.route('/logout/')
def logout():
    session.pop('user', None)
    session.pop('logged_in', None)
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


# @bp.route('/login/', methods = ['POST', 'GET'])
# def login():
#     form = LoginForm()
#     if request.method == 'POST':

#         if form.validate_on_submit():

#             # Check if the user exists in the database
#             user = check_for_user(
#                 form.username.data, form.password.data
#             )
#             if not user:
#                 flash('Invalid username or password', 'error')
#                 return redirect(url_for('main.login'))

#             # Store user information in the session
#             session['username'] = user.username
#             session['logged_in'] = True
#             flash('Login successful!')
#             return redirect(url_for('main.index'))

#     return render_template('login.html', form = form)




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