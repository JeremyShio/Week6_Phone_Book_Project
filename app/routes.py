from app import app

from flask import render_template, redirect, url_for, flash

from flask_login import login_user, login_required, logout_user, current_user

from app.forms import SignUpForm, LogInForm, ContactForm

from app.models import User, Contact


@app.route('/')
def index():
    # Reasons to use my online phone book
    reasons = ['Unlimited Storage', 'The Fastest Service', 'Always Updated', 'Add Contacts', 'View Contacts', 'Running at any time, all year round.', 'Completely FREE!']
    # Author info for author signature
    author_info = {
        'authorname': 'Jeremy Shiotani',
        # Hidden alias (ಠ.ಠ)
        'alias': 'Programming Apprentice'}
    contacts = Contact.query.all()
    # Return home page
    return render_template('index.html', author_info = author_info, reasons = reasons, contacts = contacts)


@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    form = SignUpForm()
    # Check if data for signup form is valid
    if form.validate_on_submit():
        # Get user data from the signup form
        email = form.email.data
        username = form.username.data
        password = form.password.data
        # Check if account with username/email already exists
        existing_user = User.query.filter((User.email == email) | (User.username == username)).first()
        if existing_user:
            # User feedback for unsuccessful signup
            flash("We're sorry! An account with the username or email already exists. Please try again!", 'danger')
            # Redirect user back to signup page
            return redirect(url_for('signup'))
        # User feedback for successful signup
        new_user = User(email = email, username = username, password = password)
        flash(f'{new_user.username} has been successfully created. Welcome to Phown Book Always Online™ !', 'success')
        # Redirect user back to home page
        return redirect(url_for('index'))
    # If data for the form is invalid, return signup form/page
    return render_template('signup.html', form = form)


@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LogInForm()
    # Check if data for login form is valid
    if form.validate_on_submit():
        # Get user data from the login form
        username = form.username.data
        password = form.password.data
        # Parse through the user table for a user that matches a username from the login form
        user = User.query.filter_by(username = username).first()
        # If the user exists and the password is correct
        if user is not None and user.check_password(password):
            # Log the user in with login_user from flask_login
            login_user(user)
            # User feedback for successful login
            flash(f'Welcome back to Phown Book™ {user.username}, we missed you!', 'success')
            # Redirect user back to the home page
            return redirect(url_for('index'))
        # If the user does not exist or password is incorrect
        else:
            # User feedback for unsuccessful login
            flash("We're sorry, incorrect username or password. Please try again!", 'danger')
            # Redirect user back to the login page
            return redirect(url_for('login'))
    # If form is not validated, return user to login page
    return render_template('login.html', form = form)


@app.route('/logout')
@login_required
def logout():
    # Log user out with logout_user from flask_login
    logout_user()
    # User feedback for successful logout
    flash(f'You have successfully logged out. We hope to see you again soon!', 'primary')
    # Redirect user to index page
    return redirect(url_for('index'))


@app.route('/add_contact', methods = ['GET', 'POST'])
@login_required
def add_contact():
    form = ContactForm()
    if form.validate_on_submit():
        # Get user data from the form
        firstname = form.firstname.data
        lastname = form.lastname.data
        phone = form.phone.data
        address = form.address.data
        email = form.email.data
        relationship = form.relationship.data
        other = form.other.data
        # Create new instance of Contact with form data
        new_contact = Contact(firstname = firstname, lastname = lastname, phone = phone, address = address, email = email, relationship = relationship, other = other, user_id = current_user.id)
        # User feedback for successfully added contact
        flash(f'{new_contact.firstname} {new_contact.lastname} has been successfully added to you contacts. Nice!', 'success')
        # Redirect user back to home page
        return redirect(url_for('index'))
    # If form is not validated, return user to add_contact page
    return render_template('add_contact.html', form = form)


# View single contact for user with contact id
@app.route('/view_contact/<contact_id>')
@login_required
def view_contact(contact_id):
    # Get all of user's contacts
    contact = Contact.query.get_or_404(contact_id)
    # Return render_template for contacts page
    return render_template('contact.html', contact = contact)


# Vew all contacts for user with user id
@app.route('/view_all_contacts/<user_id>')
@login_required
def view_all_contacts(user_id):
    # Get all of user's contacts
    contacts = Contact.query.filter(Contact.user_id == user_id).all()
    # Return render_template for contacts page
    return render_template('contacts.html', contacts = contacts)


@app.route('/view_contact/<contact_id>/edit', methods = ['GET', 'POST'])
@login_required
def edit_contact(contact_id):
    # Contact to edit seached (based on contact_id) through all contacts, 404 if contact is not found
    contact_to_edit = Contact.query.get_or_404(contact_id)
    # Check that contact to edit is owned by current user (2x check)
    if contact_to_edit.user_id != current_user.id:
        # User feedback in case they are trying to edit a contact they do not own
        flash("We're sorry, you are not the owner of this contact!", 'danger')
        # Redirect user back to view_contact page
        return redirect(url_for('view_contact', contact_id = contact_id))
    form = ContactForm()
    if form.validate_on_submit():
        # Get user data from the form
        firstname = form.firstname.data
        lastname = form.lastname.data
        phone = form.phone.data
        address = form.address.data
        email = form.email.data
        relationship = form.relationship.data
        other = form.other.data
        # Update the contact with user data from the form
        contact_to_edit.edit(firstname = firstname, lastname = lastname, phone = phone, address = address, email = email, relationship = relationship, other = other)
        # User feedback for successfully updated contact
        flash(f'{contact_to_edit.firstname} {contact_to_edit.lastname} has been successfully updated. Very nice!', 'info')
        # Redirect user back to updated contact page
        return redirect(url_for('view_contact', contact_id = contact_id))
    # If form is not valid, return edit_contact page
    return render_template('edit_contact.html', contact = contact_to_edit, form = form)


@app.route('/view_contact/<contact_id>/delete')
@login_required
def delete_contact(contact_id):
    # Contact to delete seached (based on contact_id) through all contacts, 404 if contact is not found
    contact_to_delete = Contact.query.get_or_404(contact_id)
    # Check that contact to edit is owned by current user (2x check)
    if contact_to_delete.user_id != current_user.id:
        # User feedback in case they are trying to delete a contact they do not own
        flash("We're sorry, you are not the owner of this contact!", 'danger')
        # Redirect user back to home page
        return redirect(url_for('index'))
    # Delete the user's desired contact
    contact_to_delete.delete()
    # User feedback for successful removal of desired contact
    flash(f'{contact_to_delete.firstname} {contact_to_delete.firstname} has been successfully deleted.', 'info')
    # Redirect user to home page
    return redirect(url_for('index'))