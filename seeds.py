from app.models import User, Product, Tag
from app.db import Session, Base, engine

# drop and rebuild tables
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)


# add users to database
db = Session()

# insert users
db.add_all([
  User(id="1", username='Tony', email='tony@gmail.com', password='123456', monthly_income=4492.32),
])

# insert tags
db.add_all([
    Tag(id="1", tag_name='Mortgage', tag_color='red', user_id=1), #1
    Tag(id="2", tag_name='rent', tag_color='blue', user_id=1), #2
    Tag(id="3", tag_name='music', tag_color='green', user_id=1), #3
    Tag(id="4", tag_name='bills', tag_color='orange', user_id=1), #4
    Tag(id="5", tag_name='Hobby Lobby', tag_color='yellow', user_id=1), #5
    Tag(id="6", tag_name='car stuff', tag_color='black', user_id=1) #6
])

# insert products
db.add_all([
  #1
  Product(id="1", description='Costco', amount=339.32, user_id=1, tag_id=1),
  Product(id="2", description='Vons', amount=132, user_id=1, tag_id=1),
  Product(id="3", description='Costco', amount=329.32, user_id=1, tag_id=1),

  #2
  Product(id="4", description='Mortgage', amount=3299.32, monthly_bill=True, user_id=1, tag_id=2),
  Product(id="5", description='HOA', amount=389.32, monthly_bill=True, user_id=1, tag_id=2),


  #3
  Product(id="6", description='CDs', amount=19.32, user_id=1, tag_id=3),
  Product(id="7", description='Drum Set', amount=932, user_id=1, tag_id=3),
  Product(id="8", description='Concert', amount=129.32, user_id=1, tag_id=3),

  #4
  Product(id="9", description='electricity (October 2012)', amount=42.32, user_id=1, tag_id=4),
  Product(id="10", description='property taxes', amount=1632, user_id=1, tag_id=4),
  Product(id="11", description='Hulu ', amount=89.32, monthly_bill=True, user_id=1, tag_id=4),

  #5
  Product(id="12", description='frames', amount=9.32, user_id=1, tag_id=5),
  Product(id="13", description='candies', amount=12, user_id=1, tag_id=5),
  Product(id="14", description='fall center piece set', amount=16.32, monthly_bill=True, user_id=1, tag_id=5),
  Product(id="15", description='calendar and stickers', amount=21.21, user_id=1, tag_id=5),
  Product(id="16", description='Christmas Tree', amount=89.32, monthly_bill=True, user_id=1, tag_id=5),
  Product(id="17", description='Craft supplies for school project', amount=13.41, user_id=1, tag_id=5),
  Product(id="18", description='Dish towels and pillows', amount=29.32, monthly_bill=True, user_id=1, tag_id=5)

])


db.commit()
db.close()