from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Admin(db.Model):
    __tablename__ = "admin"
    id  = db.Column(db.Integer, primary_key=True ,autoincrement = True )
    email = db.Column(db.String, unique = True , nullable = False)
    password = db.Column(db.String, unique = True , nullable = False)

class User(db.Model):
    __tablename__ = "user"
    id  = db.Column(db.Integer, primary_key=True ,autoincrement = True)
    name = db.Column(db.String, nullable = False)
    email = db.Column(db.String, unique = True , nullable = False)
    password = db.Column(db.String, unique = True , nullable = False)
    city  = db.Column(db.String , nullable = False)
    address  = db.Column(db.String , nullable = False)
    phone = db.Column(db.String, nullable = False)
    status = db.Column(db.String , nullable = False)
    bookings= db.relationship("Bookings", backref='user', lazy=True)




class ServiceCategory(db.Model):
    __tablename__ = "servicecategory"
    id  = db.Column(db.Integer, primary_key=True ,autoincrement = True)
    name = db.Column(db.String, unique = True ,  nullable = False)
    base_price = db.Column(db.Integer , nullable = False)
    desc = db.Column(db.String)
    professionals= db.relationship('Professional', backref='category', lazy=True)
    packages= db.relationship('Package', backref='category', lazy=True)



class Professional(db.Model):
    __tablename__ = "serviceprofessional"
    id  = db.Column(db.Integer, primary_key=True ,autoincrement = True)
    name = db.Column(db.String, nullable = False)
    email = db.Column(db.String, unique = True , nullable = False)
    password = db.Column(db.String , nullable = False)
    experience = db.Column(db.String, nullable = False)
    city = db.Column(db.String , nullable = False)
    phone = db.Column(db.String, nullable = False)
    status = db.Column(db.String , nullable = False)
    servicecategory_id = db.Column(db.Integer , db.ForeignKey("servicecategory.id") , nullable = False )
    packages= db.relationship('Package', backref='professional', lazy=True)
    recived_bookings = db.relationship('Bookings', backref='professional', lazy=True)



class Package(db.Model):
    __tablename__ = "package"
    id  = db.Column(db.Integer, primary_key=True ,autoincrement = True)
    name = db.Column(db.String, nullable = False)
    price = db.Column(db.Integer , nullable = False)
    desc = db.Column(db.String)
    servicecategory_id = db.Column(db.Integer , db.ForeignKey("servicecategory.id") , nullable = False )
    professional_id = db.Column(db.Integer , db.ForeignKey("serviceprofessional.id") , nullable = False )



class Bookings(db.Model):
    __tablename__ = "bookings"
    id  = db.Column(db.Integer, primary_key=True ,autoincrement = True)
    user_id = db.Column(db.Integer , db.ForeignKey("user.id") , nullable = False )
    package_id = db.Column(db.Integer , db.ForeignKey("package.id") , nullable = False )
    professional_id = db.Column(db.Integer , db.ForeignKey("serviceprofessional.id") , nullable = False )
    status = db.Column(db.String , nullable = False)
    time = db.Column(db.String , nullable=False )
    date = db.Column(db.String , nullable = False )