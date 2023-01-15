from flask import Blueprint, request, jsonify, session, redirect, render_template
from app.models import Tag
from app.db import start_db_session

bp = Blueprint('api/categories', __name__, url_prefix='/api')

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
        return render_template('error-page.html', message="Missing fields. Please try again")
    except:
        db.rollback()
        return render_template('error-page.html', message="Tag not added.")
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
        return render_template('error-page.html', message="Missing fields. Please try again")
    except:
        db.rollback()
        return render_template('error-page.html', message="Tag not added.")
    
    # if they edited the name in categories, the url will need to change dynamically to avoid error
    if 'redirect-url' in data:
        currentURL = request.referrer
        currentURL = currentURL.split('/')
        currentURL[len(currentURL) - 1] = data['category-name']
        newURL = '/'.join(currentURL)
        return redirect(newURL)
    else:
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
        return render_template('error-page.html', message="Oops, something happened. Please try again.")
    return redirect('/')

# Inactivate Category from profile page(different set up)
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
        return render_template('error-page.html', message="Oops, something happened. Please try again.")
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
        db.rollback()
        return render_template('error-page.html', message="Oops, something happened. Please try again.")
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
        return render_template('error-page.html', message="Oops, something happened. Please try again.")
    return redirect('/')

# Delete Category in PROFILE (different setup)
@bp.route('/delete-category-in-profile', methods=['POST'])
def delete_category_in_profile():
    db = start_db_session()
    data = request.form
    try:
        db.query(Tag).filter(Tag.id == data['category-id']).delete()
        db.commit()
    except:
        db.rollback()
        return render_template('error-page.html', message="Oops, something happened. Please try again.")
    return redirect(request.referrer)