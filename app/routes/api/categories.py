from flask import Blueprint, request, jsonify, session, redirect
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
        return jsonify(message='Missing fields.'), 400
    except:
        db.rollback()
        return jsonify(message='Tag not added'), 500
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
        return jsonify(message='category not deleted'), 500
    return redirect(request.referrer)