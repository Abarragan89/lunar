from flask import Blueprint, request, jsonify, session, redirect, render_template
import sqlalchemy
from app.models import User, Tag, Product, Cash, Salary, MonthlyCharge, ExpiredCharges
from app.db import start_db_session

bp = Blueprint('api', __name__, url_prefix='/api')

# Sign up 
@bp.route('/signup', methods=['POST'])
def signup():
    db = start_db_session()
    data = request.form
    try:
        # Make new user
        newUser = User(
            username = data['username'].strip(),
            username_lowercase = data['username'].lower().strip(),
            email = data['email'].strip(),
            password = data['password'].strip(),
        )
        db.add(newUser)
        db.commit()

        # Add Salary Model
        newSalary = Salary (
            salary_amount = data['monthly-income'].strip(),
            user_id = newUser.id
        )
        db.add(newSalary)
        db.commit()

        # Add default tags and colors
        tag_colors =[
                'rgba(255, 0, 0, 0.407)', 
                'rgba(255, 140, 0, 0.407)',
                'rgba(212, 255, 0, 0.407)', 
                'rgba(26, 255, 0, 0.407)', 
                'rgba(0, 255, 162, 0.407)',  
                'rgba(0, 191, 255, 0.407)',
                'rgba(0, 68, 255, 0.407)',
                'rgba(38, 0, 255, 0.407)',
                'rgba(153, 0, 255, 0.407)',
                'rgba(255, 0, 234, 0.407)',
                'rgba(255, 0, 64, 0.407)'
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
    except AssertionError:
        db.rollback()
        print('assertion error')
        return render_template('signup-fail.html', 
            error='Please fill in all fields.',
            username = data['username'].strip(),
            email = data['email'].strip(),
            monthly_income = data['monthly-income'].strip()
            )
    except sqlalchemy.exc.IntegrityError:
        db.rollback()
        return render_template('signup-fail.html', 
            error='Email is already taken.',
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

    # create session
    session.clear()
    session['user_id'] = newUser.id
    session['loggedIn'] = True

    return redirect('/dashboard')


# Log out
@bp.route('/logout')
def logout():
    session.clear()
    return render_template('index.html')

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
    adjust_color = f'rgba({colorTuple[0]},{colorTuple[1]},{colorTuple[2]}, .3)'

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

    if 'monthly-bill' in data:
        try:
            newMonthly = MonthlyCharge(
                description = data['product-name'].strip(),
                tag_id = data['product-category'],
                user_id = session['user_id'],
                amount = data['product-price'].strip(),
                time_created = data['expense-date']
            )
            db.add(newMonthly)
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
    if 'monthly-bill' in data:
        try:
            newMonthly = MonthlyCharge(
                description = data['product-name'].strip(),
                tag_id = data['product-category'],
                user_id = session['user_id'],
                amount = data['product-price'].strip(),
                time_created = data['expense-date-current']
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

    # lower the alpha in the tag color. Make color into rgba then lower the alpha to .4
    h = data['category-color'][1:]
    colorTuple = tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
    adjust_color = f'rgba({colorTuple[0]},{colorTuple[1]},{colorTuple[2]}, .3)'

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
    return redirect(f"/categories/{data['category-name']}")


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
        return jsonify(message='Deposit not deleted'), 500
    return redirect('/')

# Update user name
@bp.route('/update-user-name', methods=['POST'])
def update_user_name():
    data = request.form
    db = start_db_session()
    try:
        user_data = db.query(User).filter(User.id == session['user_id']).one()
        user_data.username = data['new_username'].strip()

        db.commit()
    except:
        pass
    return redirect(request.referrer)




# Update user salary
@bp.route('/update-user-salary', methods=['POST'])
def update_user():
    data = request.form
    db = start_db_session()

    # check to see if a salary in that month and year is already present. If it is, override it.
    # extract the month and year from the salary date
    month = data['new_salary_date'].split('-')[1]
    year = data['new_salary_date'].split('-')[0]

    try:
        salaryExists = db.query(Salary
            ).filter(Salary.user_id == session['user_id']
            ).filter(sqlalchemy.extract('month', Salary.time_created) == month
            ).filter(sqlalchemy.extract('year', Salary.time_created) == year
            ).one()
        salaryExists.salary_amount = data['new_salary']
        db.commit()
        return redirect(request.referrer)
    except Exception as e:
        print('============================================',e)

    # This try will only run if the other one fails
    try:
        newSalary = Salary (
            salary_amount = data['new_salary'].strip(),
            user_id = session['user_id'],
            # I need '-1' since the date back is only Year and month. '-1' makes it the first
            time_created = data['new_salary_date'] + '-1'
        )
        db.add(newSalary)
        # Delete current salary if user wants to erase history
        if 'erase_history' in data:
            db.query(Salary).filter(Salary.id == data['current-salary-id']).delete()
        
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
    try:
        db.query(MonthlyCharge).filter(MonthlyCharge.id == monthly_id).update({
            'description': monthly_description.strip(),
            'amount': monthly_price.strip(),
            'user_id': session['user_id'],
            'tag_id': monthly_tag,
            'time_created': monthly_start_date
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

    try:
        # get the year and month to create a number that will be used to query in history
        expired_monthly = db.query(MonthlyCharge).filter(MonthlyCharge.id == monthly_id).one()

        expired_year = str(expired_monthly.time_created.year)
        expired_month = str(expired_monthly.time_created.month)
        expiration_limit_string = expired_year + expired_month

        # create new expired monthly based on old monthly charge
        new_expired_monthly = ExpiredCharges(
            description = expired_monthly.description,
            amount = expired_monthly.amount,
            tag_id = expired_monthly.tag_id,
            user_id = session['user_id'],
            expiration_limit = int(expiration_limit_string)
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
            time_created = monthly_start_date
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

    try:
        # get the year and month to create a number that will be used to query in history
        expired_monthly = db.query(MonthlyCharge).filter(MonthlyCharge.id == monthly_id).one()

        expired_year = str(expired_monthly.time_created.year)
        expired_month = str(expired_monthly.time_created.month)
        expiration_limit_string = expired_year + expired_month

        # create new expired monthly based on old monthly charge
        new_expired_charge = ExpiredCharges(
            description = expired_monthly.description,
            amount = expired_monthly.amount,
            tag_id = expired_monthly.tag_id,
            user_id = session['user_id'],
            expiration_limit = int(expiration_limit_string)
        )
        db.add(new_expired_charge)
        db.commit()

        # delete old monthly charge from table. 
        db.delete(expired_monthly)
        db.commit()

    except Exception as e:
        print('============================23', e)
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

    