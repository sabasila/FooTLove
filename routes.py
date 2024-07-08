from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from ext import app, db
from forms import RegisterForm, LoginForm, ContactForm, EditItemForm
from models import Item, User
from flask_wtf.csrf import CSRFProtect
import uuid
import os



if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/')
def home():
    items = Item.query.all()
    return render_template('Home.html', items=items, )

@app.route('/products')
def products():
    items = Item.query.all()
    return render_template('Product.html', items=items)

@app.route('/item/<int:item_id>')
def item(item_id):
    item = Item.query.get_or_404(item_id)
    return render_template('Item.html', item=item)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            flash('Username already exists. Please choose a different one.', 'danger')
            return redirect(url_for('sign_in'))

        user = User( username = form.username.data, birthday=form.birthday.data, gender=form.gender.data, country=form.country.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        flash('Registration successful!', 'success')
        return redirect(url_for('sign_in'))
    return render_template('authorization.html', form=form)

@app.route('/sign-in', methods=['GET', 'POST'])
def sign_in():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'danger')
            return redirect(url_for('register'))
        login_user(user)
        return redirect(url_for('home'))
    return render_template('Cart.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/item/new', methods=['GET', 'POST'] )
@login_required
def new_item():

    if current_user.username == 'admin' and current_user.check_password('adminpass'):
        form = EditItemForm()
    if not form.validate_on_submit():
        return render_template('edit_item.html', form=form)
    image = form.images.data
    if image:
        filename = str(uuid.uuid4()) + os.path.splitext(image.filename)[1]
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image.save(filepath)
        item = Item(title=form.title.data, description=form.description.data, images=filename)
    else:
        item = Item(title=form.title.data, description=form.description.data, images=None)
    db.session.add(item)
    db.session.commit()
    flash('Item created successfully!', 'success')
    return redirect(url_for('home'))


@app.route('/item/edit/<int:item_id>', methods=['GET', 'POST'])
@login_required
def edit_item(item_id):
    if current_user.username == 'admin' and current_user.check_password('adminpass'):
      item = Item.query.get_or_404(item_id)
    form = EditItemForm(obj=item)
    if form.validate_on_submit():
        item.title = form.title.data
        item.description = form.description.data
        image = form.images.data
        if image:
            filename = str(uuid.uuid4()) + os.path.splitext(image.filename)[1]
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(filepath)
            item.images = filename
        db.session.commit()
        flash('Item updated successfully!', 'success')
        return redirect(url_for('home'))
    return render_template('edit_item.html', form=form, item=item)

@app.route('/item/<int:item_id>/delete', methods=['POST'])
@login_required
def delete_item(item_id):
    if current_user.username == 'admin' and current_user.check_password('adminpass'):
      item = Item.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    flash('Item deleted successfully!', 'success')
    return redirect(url_for('home'))

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        flash('Your message has been sent successfully!', 'success')
        return redirect(url_for('home'))
    return render_template('contact.html', form=form)
