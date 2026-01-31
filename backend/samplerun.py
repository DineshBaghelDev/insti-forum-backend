#Only for test runs with sample data

from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.community import Community 

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    user1 = User(username='testuser', password_hash='hashedpassword')
    db.session.add(user1)
    db.session.commit()
    
    com1 = Community(name='Test Community', description='A community for testing', creator_id=user1.id)
    db.session.add(com1)
    db.session.commit()

if __name__ == "__main__":
    app.run(debug=True)