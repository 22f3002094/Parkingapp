from flask import current_app as app
from flask import render_template , request , redirect , flash
from .models import db , User , ServiceCategory,Professional , Admin ,Package
from flask_login import login_user , login_required , current_user , logout_user

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
                    login_user(cust)
                    return redirect("/dashboard/customer")
                else:
                    return "incorrect password"
            else:
                return "Customer DOes not exist"
        elif role =="Admin":
            admin = db.session.query(Admin).filter_by(email=email).first()
            if admin :
               
                if admin.password==password:
                    login_user(admin)
                    return redirect("/dashboard/admin")
                else:
                    return "incorrect password"
            else:
                return "Admin DOes not exist"
        elif role =="Professional":
            prof = db.session.query(Professional).filter_by(email=email).first()
            
            if prof :
                if prof.password==password:
                    login_user(prof)
                    return redirect("/dashboard/professional")
                else:
                    return "incorrect password"
            else:
                return "professional DOes not exist"
            


@app.route("/dashboard/<u_type>"  , methods=["GET" , "POST"])
@login_required
def dashboard(u_type):
    if isinstance(current_user , User) and u_type=="customer":
        return f"welcome User"
    elif isinstance(current_user , Admin) and u_type=="admin":
        all_cats = db.session.query(ServiceCategory).all()
        active_prof = db.session.query(Professional).filter_by(status = "Active").all()
        requested_prof = db.session.query(Professional).filter_by(status = "Requested").all()
        flagged_prof = db.session.query(Professional).filter_by(status = "Flagged").all()
        active_cust = db.session.query(User).filter_by(status = "Active").all()
        flagged_cust = db.session.query(User).filter_by(status = "Flagged").all()
        return render_template("/admin/dashboard.html" , page="dashboard", cu = current_user, cats = all_cats , active_prof = active_prof , requested_prof=requested_prof, flagged_prof=flagged_prof , active_cust=active_cust , flagged_cust = flagged_cust)
    elif isinstance(current_user,Professional) and u_type == "professional":
        
        return render_template("/professional/dashboard.html" , page="dashboard" , cu = current_user    )
    else : 
        return "you are not authorised to access this route"


@app.route("/category" , methods=["POST"])
def category():
    if request.args.get("action") == "create":
        data  = request.form
        cat = db.session.query(ServiceCategory).filter_by(name = data.get("cat_name")).first()
        if not cat:
            cat = ServiceCategory(name = data.get("cat_name") , desc = data.get("cat_desc") , base_price = data.get("cat_base_price"))
            db.session.add(cat)
            db.session.commit()
            flash("Category is Created." , "success")
            return redirect("/dashboard/admin")
        else: 
            flash("Category already Exists." , "warning")
            return redirect("/dashboard/admin")
    elif request.args.get("action") == "edit":
        data  = request.form
        cat = db.session.query(ServiceCategory).filter_by(id = request.args.get("id")).first()
        if cat:
            if data.get("cat_name"):
                if db.session.query(ServiceCategory).filter_by(name=data.get("cat_name")).count() == 0 :
                    cat.name = data.get("cat_name")
            
            cat.desc = data.get("cat_desc")
            if data.get("cat_base_price"):
                cat.base_price = data.get("cat_base_price")
            db.session.commit()
            flash("Category is Updated." , "success")
            
            return redirect("/dashboard/admin")
        else:
            flash("Category is not found." , "danger")
            return redirect("/dashboard/admin")
    


@app.route("/professional" , methods=["POST"])
def professional():
    if request.args.get("action") == "Accept":
        prof = db.session.query(Professional).filter_by(id = request.args.get("id")).first()
        if prof:
            prof.status="Active"
            db.session.commit()
            flash(f"{prof.name}'s request is Accepted." , "success")
            return redirect("/dashboard/admin")
        else: 
            flash(f"Professional doesn't exist." , "danger")
            return redirect("/dashboard/admin")
    
    elif request.args.get("action") == "Reject":
        prof = db.session.query(Professional).filter_by(id = request.args.get("id")).first()
        if prof:
            prof.status="Rejected"
            db.session.commit()
            flash(f"{prof.name}'s request is Rejected." , "success")
            return redirect("/dashboard/admin")
        else: 
            flash(f"Professional doesn't exist." , "danger")
            return redirect("/dashboard/admin")
    elif request.args.get("action") == "Flag":
        prof = db.session.query(Professional).filter_by(id = request.args.get("id")).first()
        if prof:
            prof.status="Flagged"
            db.session.commit()
            flash(f"{prof.name} is flagged", "success")
            return redirect("/dashboard/admin")
        else: 
            flash(f"Professional doesn't exist.", "danger")
            return redirect("/dashboard/admin")
    elif request.args.get("action") == "Unflag":
        prof = db.session.query(Professional).filter_by(id = request.args.get("id")).first()
        if prof:
            prof.status="Active"
            db.session.commit()
            flash(f"{prof.name} is unflagged." , "success")
            return redirect("/dashboard/admin")
        else: 
            flash(f"Professional doesn't exist." , "danger")
            return redirect("/dashboard/admin")
        

@app.route("/customer" , methods=["POST"])
def customer():
    if request.args.get("action") == "Flag":
        cust = db.session.query(User).filter_by(id = request.args.get("id")).first()
        if cust:
            cust.status="Flagged"
            db.session.commit()
            flash(f"{cust.name} is Flagged." ,"success")
            return redirect("/dashboard/admin")
        else: 
            flash(f"Customer doesn't exist.", "danger")
            return redirect("/dashboard/admin")
    elif request.args.get("action") == "Unflag":
        cust = db.session.query(User).filter_by(id = request.args.get("id")).first()
        if cust:
            cust.status="Active"
            db.session.commit()
            flash(f"{cust.name} is unflagged." ,"success")
            return redirect("/dashboard/admin")
        else: 
            flash(f"Customer doesn't exist." , "danger")
            return redirect("/dashboard/admin")
        


@app.route("/package" , methods=["POST"])
def package():
    if request.args.get("action") == "create":
        data  = request.form
        cat = db.session.query(ServiceCategory).filter_by(id = current_user.servicecategory_id).first()
        if cat:
            pack = Package(name=data.get("pack_name") , desc = data.get("pack_desc") ,price=data.get("pack_price") , servicecategory_id= current_user.servicecategory_id , professional_id = current_user.id)
            db.session.add(pack)
            db.session.commit()
            flash("Package is Created." , "success")
            return redirect("/dashboard/professional")
        else: 
            flash("Catgory doesn't Exists." , "warning")
            return redirect("/dashboard/admin")
    elif request.args.get("action") == "edit":
        data  = request.form
        pack = db.session.query(Package).filter_by(id = request.args.get("id")).first()
        if pack:
            
            if data.get("pack_name"):
                pack.name = data.get("pack_name")
            if data.get("pack_desc"):
                pack.desc = data.get("pack_desc")
            if data.get("pack_price"):
                pack.price = data.get("pack_price")
            
            db.session.commit()
            flash("Package is Updated." , "success")
            return redirect("/dashboard/professional")
        else: 
            flash("Package doesn't Exists." , "warning")
            return redirect("/dashboard/admin")    


@app.route("/logout")
@login_required
def log_out():
    logout_user()
    return redirect("/login")

    


@app.route("/search/admin" , methods=["GET" , "POST"])
def search_admin():
    return render_template("/admin/search.html" ,page="search", cu = current_user)