from flask import Blueprint, render_template, request, session, flash
from flask import redirect, url_for

from miltontours.db import add_order, get_orders, check_for_user
from miltontours.db import get_cities, get_city, get_tours_for_city
from miltontours.session import get_basket, add_to_basket, empty_basket, convert_basket_to_order
from miltontours.forms import CheckoutForm, LoginForm

bp = Blueprint('main', __name__)


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


@bp.route('/checkout/', methods = ['POST', 'GET'])
def checkout():
    form = CheckoutForm() 
    if request.method == 'POST':
        
        #retrieve correct order object
        order = get_basket()
       
        if form.validate_on_submit():
            order.status = True
            order.firstname = form.firstname.data
            order.surname = form.surname.data
            order.email = form.email.data
            order.phone = form.phone.data
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


@bp.route('/login/', methods = ['POST', 'GET'])
def login():
    form = LoginForm()
    if request.method == 'POST':

        if form.validate_on_submit():

            # Check if the user exists in the database
            user = check_for_user(
                form.username.data, form.password.data
            )
            if not user:
                flash('Invalid username or password', 'error')
                return redirect(url_for('main.login'))

            # Store user information in the session
            session['username'] = user.username
            session['logged_in'] = True
            flash('Login successful!')
            return redirect(url_for('main.index'))

    return render_template('login.html', form = form)
