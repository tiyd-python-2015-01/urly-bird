from app import db

class User(db.Model):
    user = db.Column(db.String(255), nullable=False)
    password = db.column(db.String(255), nullable=False)
    email = db.column(db.String(255))
    encrypted_password = db.column()

    def __repr__(self):
        return "<User {}>".format(self.user)