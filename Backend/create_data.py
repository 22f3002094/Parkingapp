from .models import db , Admin , ServiceCategory ,Professional , User
from flask import current_app as app

with app.app_context():
    db.create_all()

    if db.session.query(Admin).count() == 0:
        admin = Admin( email = "admin@gmail.com" , password = "pass" )
        db.session.add(admin)
        db.session.commit()
    if db.session.query(ServiceCategory).count() == 0:
        home = ServiceCategory( name = "Home Cleaning" ,base_price = 500 )
        db.session.add(home)
        db.session.commit()

        hd = ServiceCategory( name = "Home Decor" ,base_price = 500 )
        db.session.add(hd)
        db.session.commit()

    if db.session.query(Professional).count() ==0 :
        prof1 = Professional(name = "Prof1" , email = "prof1@gmail.com" , password = "pass" , city= "Delhi" , phone= "9999999999" , experience = "10" , status = "Requested" , servicecategory_id = 1 )
        db.session.add(prof1)
        db.session.commit()
        prof2 = Professional(name = "Prof2" , email = "prof2@gmail.com" , password = "pass" , city= "Delhi" , phone= "9999999999" , experience = "10" , status = "Requested" , servicecategory_id = 1 )
        db.session.add(prof2)
        db.session.commit()
    pro1 = db.session.query(Professional).filter_by(id = 1 ).first()
    print("the service name of this prof is" , pro1.category.base_price)
