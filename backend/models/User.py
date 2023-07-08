from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "profile"

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    username = db.Column(db.String(), nullable=False, unique=True)
    email = db.Column(db.String(), nullable=False)
    password = db.Column(db.Text(), nullable=False)
    firstname = db.Column(db.String())
    lastname = db.Column(db.String())
    age = db.Column(db.Integer())    
    gender = db.Column(db.String())
    height = db.Column(db.Integer())   
    weight = db.Column(db.Integer())   
    illness = db.Column(db.String())

    def __init__(self, username, email, password, firstname, lastname, age, gender, height, weight, illness):
        self.username = username
        self.email = email
        self.password = password
        self.firstname = firstname
        self.lastname = lastname
        self.age = age
        self.gender = gender
        self.height = height
        self.weight = weight
        self.illness = illness

    def __repr__(self):
        return f"User {self.username}: Age: {self.age}"

    @classmethod
    def fetch_by_id(self, id):
       return User.query.filter_by(id=id).first()
    
    @classmethod
    def fetch_by_username(self, username):
        return User.query.filter_by(username=username).first()
    
    def save(self):
        db.session.add(self)
        db.session.commit()
        return self.id
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()