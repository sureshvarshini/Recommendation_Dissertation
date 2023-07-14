from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'profile'

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


class Food(db.Model):
    __tablename__ = 'food'
    __bind_key__ = 'food'

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.String(), nullable=False)
    calories = db.Column(db.Float())
    cholesterol = db.Column(db.Float())
    folic_acid = db.Column(db.Float())
    vitamin_c = db.Column(db.Float())
    vitamin_d = db.Column(db.Float())
    calcium = db.Column(db.Float())
    iron = db.Column(db.Float())
    protein = db.Column(db.Float())
    carbohydrate = db.Column(db.Float())
    fiber = db.Column(db.Float())
    sugars = db.Column(db.Float())
    fat = db.Column(db.Float())

    def __init__(self, name, calories, cholesterol, folic_acid, vitamin_c, vitamin_d, calcium, iron, protein, carbohydrate, fiber, sugars, fat):
        self.name = name
        self.calories = calories
        self.cholesterol = cholesterol
        self.folic_acid = folic_acid
        self.vitamin_c = vitamin_c
        self.vitamin_d = vitamin_d
        self.calcium = calcium
        self.iron = iron
        self.protein = protein
        self.carbohydrate = carbohydrate
        self.fiber = fiber
        self.sugars = sugars
        self.fat = fat

    def __repr__(self):
        return f"Name of the food: {self.name}: Calories: {self.calories}"

    @classmethod
    def fetch_by_id(self, id):
        return Food.query.filter_by(id=id).first()
    

class Rating(db.Model):
    __tablename__ = 'rating'
    __bind_key__ = 'rating'

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer(), nullable=False)
    food_id = db.Column(db.Integer(), nullable=False)
    rating = db.Column(db.Integer(), nullable=False)

    def as_dictionary(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

    @classmethod
    def fetch_by_user_id(self, id):
        return Rating.query.filter_by(user_id=id).all()
    
    def fetch_all_ratings():
        return [each_rating.as_dictionary() for each_rating in Rating.query.all()]
    
    def fetch_distinct_user():
        return db.session.query(Rating.user_id).distinct().all()
    
    def fetch_distinct_food():
        return db.session.query(Rating.food_id).distinct().all()
    
    def save(self):
        db.session.add(self)
        db.session.commit()