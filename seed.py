from models import User, Post, db
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


post1 = Post(title="What does everybody knows?", content="That the the bird bird bird that the bird is the word", user_id=3)
post2 = Post(title="Entirely different post", content="Everybody knows that the bird is the word", user_id=3)
post3 = Post(title="Giggity", content="Allright!", user_id=4)

db.session.add(post1)
db.session.add(post2)
db.session.add(post3)
db.session.commit()
