from app.models import User, Product, Tag
from app.db import Session, Base, engine

# drop and rebuild tables
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)


# add users to database
db = Session()

# insert users
db.add_all([
  User(username='alesmonde0', email='nwestnedge0@cbc.ca', password='password123', monthly_income=3492.32),
  User(username='jwilloughway1', email='rmebes1@sogou.com', password='password123', monthly_income=492.32),
  User(username='iboddam2', email='cstoneman2@last.fm', password='password123', monthly_income=5212.32),
  User(username='dstanmer3', email='ihellier3@goo.ne.jp', password='password123', monthly_income=32.32),
  User(username='djiri4', email='gmidgley4@weather.com', password='password123', monthly_income=13492)
])

# insert tags
db.add_all([
    Tag(tag_name='groceries', tag_color='red', user_id=1),
    Tag(tag_name='cars', tag_color='blue', user_id=1)
])

# insert products
db.add_all([
  Product(product_name='shoes', price=19.32, user_id=1, tag_id=1),
  Product(product_name='car', price=1932, user_id=1, tag_id=2),
  Product(product_name='car payment', price=129.32, monthly_bill=True, user_id=1, tag_id=2)
])


db.commit()
db.close()