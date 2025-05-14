from flask import current_app as app
from flask import render_template , request , redirect
from .models import db , User , ServiceCategory,Professional , Admin

@app.route("/")
def index():
    return render_template("home.html")


@app.route("/register" ,methods=["GET" ,"POST"] )
def welcome():
    if request.method == "GET":
        if request.args.get("utype") =="customer":
            return render_template("/customer/signup.html")
        elif request.args.get("utype") =="professional":
            cats = db.session.query(ServiceCategory).all()
            print(cats)
            return render_template("/professional/signup.html" , all_cats= cats)
    elif request.method=="POST":
        if request.args.get("utype") == "customer":
            name = request.form.get("cust_name")
            email =request.form.get("cust_email")
            address =request.form.get("cust_address")
            city =request.form.get("cust_city")
            phone =request.form.get("cust_phone")
            password = request.form.get("cust_password")
            print(email)
            print(name)
            print(address)
            print(city)
            print(phone)
            print(password)
            cust = db.session.query(User).filter_by(email = email).first()
            if cust:
                return redirect("/register?utype=customer")
            else:

                newcust = User(email = email , name = name,password = password , phone=phone , address = address , city=city , status="Active")
                db.session.add(newcust)
                db.session.commit()
                return redirect("/login")
        elif request.args.get("utype") == "professional":
            name = request.form.get("prof_name")
            email =request.form.get("prof_email")
            exp =request.form.get("prof_exp")
            city =request.form.get("prof_city")
            phone =request.form.get("prof_phone")
            password = request.form.get("prof_password")
            cat_id = request.form.get("prof_cat_id")
            print(email)
            print(name)
            print(exp)
            print(city)
            print(phone)
            print(password)
            print(cat_id)
            prof = db.session.query(Professional).filter_by(email=email).first()
            if prof:
                return redirect("/register?utype=professional")
            else:
                newprof = Professional(name = name , email=email , password = password,experience = exp , city = city , phone = phone ,servicecategory_id =  cat_id , status="Requested")
                db.session.add(newprof)
                db.session.commit()
                return redirect("/login")

       
    


@app.route("/login" ,methods=["GET" , "POST"])
def login():
    if request.method=="GET":
        return render_template("login.html")
    elif request.method=="POST":
        email = request.form.get("email")
        password = request.form.get("password")
        role = request.form.get("role")
        if role =="Customer":
            cust = db.session.query(User).filter_by(email=email).first()
            if cust :
                if cust.password==password:
                    return redirect("/dashboard/customer")
                else:
                    return "incorrect password"
            else:
                return "Customer DOes not exist"
        elif role =="Admin":
            admin = db.session.query(Admin).filter_by(email=email).first()
            if admin :
                if admin.password==password:
                    return redirect("/dashboard/admin")
                else:
                    return "incorrect password"
            else:
                return "Admin DOes not exist"
        elif role =="Professional":
            admin = db.session.query(Professional).filter_by(email=email).first()
            if admin :
                if admin.password==password:
                    return redirect("/dashboard/professional")
                else:
                    return "incorrect password"
            else:
                return "professional DOes not exist"
            


@app.route("/dashboard/<u_type>"  , methods=["GET" , "POST"])
def dashboard(u_type):
    return f"welcome {u_type}"