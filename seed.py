from models import User, db
from app import app

db.drop_all()
db.create_all()

User.query.delete()

bob = User(first_name="Bob", last_name="Cunningham")
anna = User(first_name="Anna", last_name="Smith")
peter = User(first_name="Peter", last_name="Griffin", image_url="/static/images/p_griffin.png")
glenn = User(first_name="Glenn", last_name="Quagmire", image_url="/static/images/g_quagmire.png")

db.session.add(bob)
db.session.add(anna)
db.session.add(peter)
db.session.add(glenn)

db.session.commit()
