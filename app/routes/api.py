from flask import Blueprint, request, jsonify, session, redirect, render_template, current_app
import datetime
from app.models import User, Tag, Product, Cash, Salary, ActiveSalary, MonthlyCharge, ExpiredCharges, TempUser, ConfirmationToken
from app.db import start_db_session
from flask_mail import Message
import uuid

bp = Blueprint('api', __name__, url_prefix='/api')

today = datetime.datetime.now()
current_month = today.strftime('%m')
current_year = today.year
print('==============curr ', type(current_month), current_year)

# Sign up
@bp.route('/signup', methods=['POST'])
def signup():
    db = start_db_session()
    data = request.form
    try:
        # Make new user
        user_exists = db.query(User).filter(User.email == data['email'].strip()).first()

        if user_exists:
            db.rollback()
            return render_template('signup-fail.html', 
                error='Email is already taken.',
                username = data['username'].strip(),
                email = data['email'].strip(),
                monthly_income = data['monthly-income'].strip()
                )
    except AssertionError:
        db.rollback()
        print('assertion error')
        return render_template('signup-fail.html', 
            error='Please fill in all fields.',
            username = data['username'].strip(),
            email = data['email'].strip(),
            monthly_income = data['monthly-income'].strip()
            )
    except Exception as e:
        print(e)
        db.rollback()
        return render_template('signup-fail.html', 
            error='An error occurred. Please try again',
            username = data['username'].strip(),
            email = data['email'].strip(),
            monthly_income = data['monthly-income'].strip()
            )
    try: 
        # make unique string
        result = uuid.uuid4()
        result = str(result.hex)
        # Make new user
        newUser = TempUser(
            username = data['username'].strip(),
            username_lowercase = data['username'].lower().strip(),
            email = data['email'].strip(),
            unique_id = result,
            salary_amount = data['monthly-income']
        )
        db.add(newUser)
        db.commit()
        if newUser:
            msg = Message('Lunar: Verify Your Account', sender = 'anthony.bar.89@gmail.com', recipients = [newUser.email])
            msg.body = f"Just one more step,\nClick the link below to verify your account and take ownership of your finances!\nLink will expire in 2 minutes.\n{request.base_url.split('/')[0] + request.base_url.split('/')[1] + request.base_url.split('/')[2]}/verify/{result}\n -Lunar"
            current_app.mail.send(msg)
    except Exception as e:
        print('=====================', e)
    return render_template('signup_check_email.html')


# Sign up Verified
@bp.route('/signup_verified', methods=['POST'])
def signup_verified():
    db = start_db_session()
    data = request.form
    temp_user_id = data['temp-user-unique-id']
    user_password = data['user-password']

    try:
        # find temporary user
        temp_user = db.query(TempUser).filter(TempUser.unique_id == temp_user_id).one()

        # Make new user from temp user
        newUser = User(
            username = temp_user.username,
            username_lowercase = temp_user.username_lowercase,
            email = temp_user.email,
            password = user_password
        )
        db.add(newUser)
        db.commit()
        # create session
        session.clear()
        session['user_id'] = newUser.id
        session['loggedIn'] = True

        # Add Salary Model
        newSalary = ActiveSalary (
            salary_amount = temp_user.salary_amount,
            start_date = str(current_year) + str(current_month).rjust(2, '0'),
            user_id = newUser.id
        )
        db.add(newSalary)
        #delete temp user
        db.commit()
        db.delete(temp_user)
        db.commit()

        # Add default tags and colors
        tag_colors =[
                'rgb(255, 0, 0)', 
                'rgb(255, 140, 0)',
                'rgb(212, 255, 0)', 
                'rgb(26, 255, 0)', 
                'rgb(0, 255, 162)',  
                'rgb(0, 191, 255)',
                'rgb(0, 68, 255)',
                'rgb(38, 0, 255)',
                'rgb(153, 0, 255)',
                'rgb(255, 0, 234)',
                'rgb(255, 0, 64)'
                ]
        # give user basic categories
        tag_names = [
                'Mortgage-Rent', 
                'Dining', 
                'Groceries', 
                'Presents', 
                'Bills', 
                'Entertainment', 
                'Investments', 
                'Travel', 
                'Shopping', 
                'Alcohol', 
                'Misc.'
                ]
        for num in range(11):
            newTag = Tag(
                tag_name = tag_names[num],
                tag_color = tag_colors[num],
                user_id = newUser.id
            )
            db.add(newTag)
            db.commit()

    except Exception as e:
        print('============== making new user', e)

    return redirect('/dashboard')


# Log out
@bp.route('/logout')
def logout():
    session.clear()
    return redirect('/')

# Log In
@bp.route('/login', methods=['POST'])
def login():
    data = request.form
    db = start_db_session()

    try:
        user = db.query(User).filter(
            User.email == data['email'].strip()
        ).one()
    except:
        return render_template('login-fail.html', error='User not found.', email=data['email'].strip())

    if user.verify_password(data['password']) == False:
        return render_template('login-fail.html', error='Incorrect credentials.', email=data['email'].strip())
    
    session.clear()
    session['user_id'] = user.id
    session['loggedIn'] = True

    return redirect('/dashboard')


# Add a Category
@bp.route('/add-category', methods=['POST'])
def add_category():
    data = request.form
    db = start_db_session()
    # lower the alpha in the tag color. Make color into rgba then lower the alpha to .4
    h = data['category-color'][1:]
    colorTuple = tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
    adjust_color = f'rgb({colorTuple[0]},{colorTuple[1]},{colorTuple[2]})'

    try:
        newTag = Tag(
            tag_name = data['category-name'].strip(),
            tag_color = adjust_color,
            user_id = session['user_id']
        )
        db.add(newTag)
        db.commit()
    except AssertionError:
        db.rollback()
        return jsonify(message='Missing fields.'), 400
    except:
        db.rollback()
        return jsonify(message='Tag not added'), 500
    return redirect(request.referrer)

# Add an expense
@bp.route('/add-expense', methods=['POST'])
def add_expense():
    data = request.form
    db = start_db_session()
    start_date = data['expense-date']
    expiration_limit = int(str(start_date.split('-')[0]) + str(start_date.split('-')[1]))

    if 'monthly-bill' in data:
        try:
            newMonthly = MonthlyCharge(
                description = data['product-name'].strip(),
                tag_id = data['product-category'],
                user_id = session['user_id'],
                amount = data['product-price'].strip(),
                time_created = data['expense-date'],
                start_date = expiration_limit
            )
            db.add(newMonthly)
            db.commit()
        except AssertionError:
            db.rollback()
            return jsonify(message='Missing fields.'), 400
        except Exception as e:
            print('===========================================', e)
            db.rollback()
            return jsonify(message='Expense not added'), 500
        return redirect(request.referrer)
    else:
        try:
            newExpense = Product(
                description = data['product-name'].strip(),
                tag_id = data['product-category'],
                user_id = session['user_id'],
                amount = data['product-price'].strip(),
                time_created = data['expense-date']
            )
            db.add(newExpense)
            db.commit()
        except AssertionError:
            db.rollback()
            return jsonify(message='Missing fields.'), 400
        except Exception as e:
            print(e)
            db.rollback()
            return jsonify(message='Expense not added'), 500
    return redirect(request.referrer)

# Add Cash
@bp.route('/add-cash', methods=['POST'])
def add_cash():
    data = request.form
    db = start_db_session()
    try:
        newCash = Cash(
            description = data['money-description'].strip(),
            amount = data['amount'].strip(),
            user_id = session['user_id'],
            time_created = data['add-cash-date']
        )
        db.add(newCash)
        db.commit()
    except AssertionError:
        db.rollback()
        return jsonify(message='Missing fields.'), 400
    except:
        db.rollback()
        return jsonify(message='Cash not added'), 500
    return redirect(request.referrer)


# Update Expense
@bp.route('/update-expense', methods=['POST'])
def update_expense():
    data = request.form 
    db = start_db_session()
    start_date = data['expense-date-current']

    if 'monthly-bill' in data:
        try:
            expiration_limit = int(str(start_date.split('-')[0]) + str(start_date.split('-')[1]))
            newMonthly = MonthlyCharge(
                description = data['product-name'].strip(),
                tag_id = data['product-category'],
                user_id = session['user_id'],
                amount = data['product-price'].strip(),
                time_created = data['expense-date-current'],
                start_date = expiration_limit
            )
            db.add(newMonthly)
            db.commit()

            db.query(Product).filter(Product.id == data['product-id']).delete()
            db.commit()
        except AssertionError:
            db.rollback()
            return jsonify(message='Missing fields.'), 400
        except Exception as e:
            print(e)
            db.rollback()
            return jsonify(message='Expense not added'), 500
        return redirect(request.referrer)
    else:
        try:
            db.query(Product).filter(Product.id == data['product-id']).update({
                'description': data['product-name'].strip(),
                'tag_id': data['product-category'],
                'user_id': session['user_id'],
                'amount': data['product-price'].strip(),
                'time_created': data['expense-date-current']
            })
            db.commit()
        except AssertionError:
            db.rollback()
            return jsonify(message='Missing fields.'), 400
        except Exception as e:
            print(e)
            db.rollback()
            return jsonify(message='Expense not updated'), 500
        return redirect(request.referrer)

#Delete Expense
@bp.route('/delete-expense', methods=['POST'])
def delete_expense():
    db = start_db_session()
    data = request.form
    try:
        db.query(Product).filter(Product.id == data['product-id']).delete()
        db.commit()
    except:
        db.rollback()
        return jsonify(message='Expense not deleted'), 500
    return redirect(request.referrer)


# Update Deposit
@bp.route('/edit-deposit', methods=['POST'])
def update_deposit():
    data = request.form 
    db = start_db_session()
    try:
        db.query(Cash).filter(Cash.id == data['cash-id']).update({
            'description': data['money-description'].strip(),
            'amount': data['amount'].strip(),
            'user_id': session['user_id'],
            'time_created': data['deposit-date']
        })
        db.commit()
    except AssertionError:
        db.rollback()
        return jsonify(message='Missing fields.'), 400
    except:
        db.rollback()
        return jsonify(message='Tag not added'), 500
    return redirect(request.referrer)


# Delete Cash deposit
@bp.route('/delete-deposit', methods=['POST'])
def delete_deposit():
    db = start_db_session()
    data = request.form
    try:
        db.query(Cash).filter(Cash.id == data['cash-id']).delete()
        db.commit()
    except:
        db.rollback()
        return jsonify(message='Deposit not deleted'), 500
    return redirect(request.referrer)


# Update Category
@bp.route('/edit-category', methods=['POST'])
def edit_category():
    data = request.form 
    db = start_db_session()

    # change hexdecimal into rgb
    h = data['category-color'][1:]
    colorTuple = tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
    adjust_color = f'rgb({colorTuple[0]},{colorTuple[1]},{colorTuple[2]})'

    try:
        current_tag = db.query(Tag).filter(Tag.id == data['category-id']).one()
        current_tag.tag_color = adjust_color
        current_tag.tag_name = data['category-name'].strip()
        db.commit()
    except AssertionError:
        db.rollback()
        return jsonify(message='Missing fields.'), 400
    except:
        db.rollback()
        return jsonify(message='Tag not updated'), 500
    return redirect(request.referrer)


# Inactivate Category
@bp.route('/inactivate-category', methods=['POST'])
def inactivate_category():
    db = start_db_session()
    data = request.form
    try:
        category = db.query(Tag).filter(Tag.id == data['category-id']).one()
        category.active = False
        db.commit()
    except:
        db.rollback()
        return jsonify(message='Deposit not deleted'), 500
    return redirect('/')

# Inactivate Category in profile
@bp.route('/inactivate-category-in-profile', methods=['POST'])
def inactivate_category_in_profile():
    db = start_db_session()
    data = request.form
    try:
        category = db.query(Tag).filter(Tag.id == data['category-id']).one()
        category.active = False
        db.commit()
    except:
        db.rollback()
        return jsonify(message='Deposit not deleted'), 500
    return redirect(request.referrer)


# Reactivate Category
@bp.route('/reactive-category', methods=['POST'])
def reactivate_category():
    db = start_db_session()
    data = request.form

    try:
        category = db.query(Tag).filter(Tag.id == data['category-id']).one()
        category.active = True
        db.commit()
    except Exception as e:
        print('========== trying to activate category', e)
    return redirect(request.referrer)


# Delete Category
@bp.route('/delete-category', methods=['POST'])
def delete_category():
    db = start_db_session()
    data = request.form
    try:
        db.query(Tag).filter(Tag.id == data['category-id']).delete()
        db.commit()
    except:
        db.rollback()
        return jsonify(message='category not deleted'), 500
    return redirect('/')

# Delete Category in Profile
@bp.route('/delete-category-in-profile', methods=['POST'])
def delete_category_in_profile():
    db = start_db_session()
    data = request.form
    try:
        db.query(Tag).filter(Tag.id == data['category-id']).delete()
        db.commit()
    except:
        db.rollback()
        return jsonify(message='category not deleted'), 500
    return redirect(request.referrer)

# Update user name
@bp.route('/update-username', methods=['POST'])
def update_user_name():
    data = request.form
    db = start_db_session()
    try:
        user_data = db.query(User).filter(User.id == session['user_id']).one()
        user_data.username = data['new_username'].strip()

        db.commit()
    except Exception as e:
        print('=========================username', e)
    return redirect(request.referrer)

# Add new Active Salary
@bp.route('/add-salary', methods=['POST'])
def add_salary():
    data = request.form
    user_id = session['user_id']
    new_salary_start_date = data['new-salary-date']
    salary_start = int(new_salary_start_date.split('-')[0] + new_salary_start_date.split('-')[1])
    db = start_db_session()
    try:
        # Check to see if they already have an active salary. 
        old_salary = db.query(ActiveSalary).filter(ActiveSalary.user_id == user_id).first()
        # If so, make a new non active salary with old data. 
        if old_salary:
        # Need to create last date which is one less than the start date of new active salary
            # the end date of the new expired charged needs to be 'salary_start' minus 1
            old_salary_end_date = salary_start - 1
            # need to check for double zeros in the end, if so, subtract year and make month 12
            if old_salary_end_date % 100 == 0:
                old_salary_end_date = int(str(int(new_salary_start_date.split('-')[0]) - 1) + '12')
            # Make new expired salary
            expired_salary = Salary(
                salary_amount = old_salary.salary_amount,
                user_id = user_id,
                start_date = old_salary.start_date,
                last_payment = old_salary_end_date
            )
            db.add(expired_salary)
            db.commit()

            # Update active salary data with form data
            old_salary.salary_amount = data['new-monthly-income']
            old_salary.start_date = salary_start
            db.commit()
        else: 
            new_active = ActiveSalary(
                salary_amount = data['new-monthly-income'],
                user_id = user_id,
                start_date = salary_start
            )
            db.add(new_active)
            db.commit()
    except Exception as e:
        print('====================== in keep history', e)
    return redirect(request.referrer)

# stop active salary
@bp.route('/stop-active-salary', methods=['POST'])
def stop_user_salary():
    data = request.form
    db = start_db_session()
    salary_id = data['salary-id']
    expiration_date = data['expiration-limit-date']
    salary_end_date = int(expiration_date.split('-')[0] + expiration_date.split('-')[1])

    try:
        old_salary = db.query(ActiveSalary).filter(ActiveSalary.id == salary_id).one()
        new_expired_salary = Salary (
            salary_amount = old_salary.salary_amount,
            start_date = old_salary.start_date,
            last_payment = salary_end_date,
            user_id = session['user_id']
        )
        db.add(new_expired_salary)
        db.delete(old_salary)
        db.commit()
    except Exception as e:
        print('========== stopping salary', e)
    
    return redirect(request.referrer)


# Delete Salary
@bp.route('/delete-user-salary', methods=['POST'])
def delete_user_salary():
    data = request.form
    db = start_db_session()
    salary_id = data['salary-id']
    try:
        if 'salary-is-active-delete' in data:
            db.query(ActiveSalary).filter(ActiveSalary.id == salary_id).delete()
            db.commit()
        else:
            db.query(Salary).filter(Salary.id == salary_id).delete()
            db.commit()
    except Exception as e:
        print('deleting ====== salary', e)
    return redirect(request.referrer)


# Update Active user salary
@bp.route('/edit-user-active-salary', methods=['POST'])
def edit_user_active_salary():
    data = request.form
    db = start_db_session()
    user_id = session['user_id']
    new_salary_start = int(data['active-salary-start-date-edit'].split('-')[0] + data['active-salary-start-date-edit'].split('-')[1])
    new_monthly_income = data['new-active-monthly-income']

    try:
        salary_to_update = db.query(ActiveSalary).filter(ActiveSalary.user_id == user_id).one()
        salary_to_update.start_date = new_salary_start
        salary_to_update.salary_amount = new_monthly_income
        db.commit()

    except Exception as e:
        print('====================== in keep history', e)
    return redirect(request.referrer)
    
# Update old user salary
@bp.route('/edit-user-old-salary', methods=['POST'])
def edit_user_old_salary():

    data = request.form
    db = start_db_session()
    new_salary_start = int(data['salary-start-date-edit'].split('-')[0] + data['salary-start-date-edit'].split('-')[1])
    new_salary_end = int(data['salary-end-date-edit'].split('-')[0] + data['salary-end-date-edit'].split('-')[1])
    salary_id = data['salary-id-edit']
    new_monthly_income = data['edit-salary-income']

    try:
        salary_to_update = db.query(Salary).filter(Salary.id == salary_id).one()
        salary_to_update.start_date = new_salary_start
        salary_to_update.last_payment = new_salary_end
        salary_to_update.salary_amount = new_monthly_income
        db.commit()

    except Exception as e:
        print('====================== in keep history', e)
    return redirect(request.referrer)


# Update Monthly Bill (completely change history)
@bp.route('/complete-edit-monthly-charge', methods=['POST'])
def edit_monthly_charge():
    data = request.form
    db = start_db_session()
    monthly_id = data['monthly-id']
    monthly_tag = data['monthly-category']
    monthly_price = data['monthly-price']
    monthly_description = data['monthly-name']
    monthly_start_date = data['monthly-date']
    start_date = int(str(monthly_start_date.split('-')[0]) + str(monthly_start_date.split('-')[1]))

    try:
        db.query(MonthlyCharge).filter(MonthlyCharge.id == monthly_id).update({
            'description': monthly_description.strip(),
            'amount': monthly_price.strip(),
            'user_id': session['user_id'],
            'tag_id': monthly_tag,
            'start_date': start_date,
        })
        db.commit()
    except Exception as e:
        print('===============', e)
    return redirect(request.referrer)


# Update Monthly Charge (update moving forward)
@bp.route('/update-edit-monthly-charge', methods=['POST'])
def update_monthly_charge():
    data = request.form
    db = start_db_session()
    monthly_id = data['monthly-id']
    monthly_tag = data['monthly-category']
    monthly_price = data['monthly-price'].strip()
    monthly_description = data['monthly-name'].strip()
    monthly_start_date = data['monthly-date']

    # This is the limit that will be placed on the expired charge. Only query less than this in history
    # This will also be the start date of the new monthly charge. From this date forward. greater than or equal to
    new_charge_start_date = int(str(monthly_start_date.split('-')[0]) + str(monthly_start_date.split('-')[1]))

    # the end date of the new expired charged needs to be 'new_charge_start_date' minus 1
    new_expired_end_date = new_charge_start_date - 1
    # need to check for double zeros in the end, if so, subtract year and make month 12
    if new_expired_end_date % 100 == 0:
        new_expired_end_date = int(str(int(monthly_start_date.split('-')[0]) - 1) + '12')

    try:
        # get the data from the old monthly charge to make an expired charge
        expired_monthly = db.query(MonthlyCharge).filter(MonthlyCharge.id == monthly_id).one()
        expiration_date = int(str(expired_monthly.start_date)[:3] + str(expired_monthly.start_date)[3:])
        

        # create new expired monthly based on old monthly charge
        new_expired_monthly = ExpiredCharges(
            description = expired_monthly.description,
            amount = expired_monthly.amount,
            tag_id = expired_monthly.tag_id,
            user_id = session['user_id'],
            expiration_limit = new_expired_end_date,
            start_date = expiration_date
        )
        db.add(new_expired_monthly)
        # delete old monthly charge from table. 
        db.delete(expired_monthly)
        db.commit()

        # create new current monthly charge
        newMonthly = MonthlyCharge(
            description = monthly_description,
            tag_id = monthly_tag,
            user_id = session['user_id'],
            amount = monthly_price,
            start_date = new_charge_start_date
            )
        db.add(newMonthly)
        db.commit()
    except Exception as e:
        print('===============eeee', e)
    return redirect(request.referrer)



# Stop Monthly Bill
@bp.route('/stop-monthly-charge', methods=['POST'])
def stop_monthly_charge():
    data = request.form
    db = start_db_session()
    monthly_id = data['monthly-id']
    expiration_limit = data['expiration-limit-date']
    expiration_limit = int(expiration_limit.split('-')[0] + expiration_limit.split('-')[1])

    try:
        expired_monthly = db.query(MonthlyCharge).filter(MonthlyCharge.id == monthly_id).one()
        start_date = int(str(expired_monthly.time_created.year) + str(expired_monthly.time_created.strftime('%m')))

        # create new expired monthly based on old monthly charge
        new_expired_charge = ExpiredCharges(
            description = expired_monthly.description,
            amount = expired_monthly.amount,
            tag_id = expired_monthly.tag_id,
            user_id = session['user_id'],
            expiration_limit = expiration_limit,
            start_date = start_date
        )
        db.add(new_expired_charge)
        db.commit()

        # delete old monthly charge from table. 
        db.delete(expired_monthly)
        db.commit()
    except Exception as e:
        print('============================23232323323223', e)
    return redirect(request.referrer)


# Delete Monthly Bill
@bp.route('/delete-monthly-charge', methods=['POST'])
def delete_monthly_charge():
    data = request.form
    db = start_db_session()
    try:
        db.query(MonthlyCharge).filter(MonthlyCharge.id == data['monthly-id']).delete()
        db.commit()
    except Exception as e:
        print(e)
        db.rollback()
        return jsonify(message='Expense not deleted'), 500
    return redirect(request.referrer)

# Update Expired Charges
@bp.route('/update-expired-charge', methods=['POST'])
def update_expired_charge():
    data = request.form
    db = start_db_session()

    category_id = data['monthly-category']
    expired_price = data['monthly-price']
    expired_description = data['monthly-name']
    expired_id = data['expired-id']
    start_date = data['start-date']
    end_date = data['end-date']
    # need to change the dates to an integer so we can query easier
    start_date = int(start_date.split('-')[0] + start_date.split('-')[1])
    end_date = int(end_date.split('-')[0] + end_date.split('-')[1])

    try:
        db.query(ExpiredCharges).filter(ExpiredCharges.id == expired_id).update({
            'description': expired_description,
            'amount': expired_price,
            'user_id': session['user_id'],
            'tag_id': category_id,
            'expiration_limit': end_date,
            'start_date': start_date
        })
        db.commit()
    except Exception as e:
        print('======================= updating expired charge', e)
    return redirect(request.referrer)
    
# Delete Expired Charge
@bp.route('/delete-expired-charge', methods=['POST'])
def delete_expired_charge():
    data = request.form
    db = start_db_session()
    print('=================== delete expire', data['expired-id'])
    try:
        db.query(ExpiredCharges).filter(ExpiredCharges.id == data['expired-id']).delete()
        db.commit()
    except Exception as e:
        print(e)
        db.rollback()
        return jsonify(message='Expense not deleted'), 500
    return redirect(request.referrer)


# Forgot password
@bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    data = request.form
    user_email = data['email']
    db =start_db_session()

    result = uuid.uuid4()
    result = str(result.hex)
    user_exists = False
    try:
        user = db.query(User).filter(User.email == user_email).first()
        if user:
            user_exists=True
            try: 
                new_token = ConfirmationToken(
                    unique_string = result,
                    email = user_email
                )
                db.add(new_token)
                db.commit()

                msg = Message('Lunar: Verify Your Account', sender = 'anthony.bar.89@gmail.com', recipients = [user_email])
                # wanted to get rid of the 'api/forgot-password' in the request url
                msg.body = f"Looks like you forgot something,\nClick the link below to reset your password.\n{request.base_url.split('/')[0] + request.base_url.split('/')[1] + request.base_url.split('/')[2]}/reset-password/{new_token.unique_string}\n -Lunar"
                current_app.mail.send(msg)

                return render_template('forgot_password_message.html', user_exists=user_exists)
            except Exception as e:
                print('=============================== maing token',e)
    except Exception as e:
        print(e)
    return render_template('forgot_password_message.html', user_exists=user_exists)

# Reset Password
@bp.route('/reset-password', methods=['POST'])
def reset_password_change():
    data = request.form
    db =start_db_session()

    valid_token = data['validation-token']
    print('validation-token', valid_token)
    try:
        find_token = db.query(ConfirmationToken).filter(ConfirmationToken.unique_string == valid_token).first()
        if find_token:
            find_user = db.query(User).filter(User.email == find_token.email).one()
            find_user.password = data['new-password-confirm']
            db.commit()        
    except Exception as e:
        print('========================',e)
        return render_template('reset-password.html', success=False)
    
    return render_template('login.html')
