from flask import render_template, Blueprint, redirect, url_for, request, flash

from website import db
from website.models import Student, Admin, Sponsorship, Grant , Bursary

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
import smtplib


auth = Blueprint('auth', __name__)

@auth.route('/sign-up', methods = ['GET', 'POST'])
def signUp():
    if request.method =='POST':
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        studentEmail = request.form.get('studentEmail')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        department = request.form.get('department')

        student = Student.query.filter_by(studentEmail=studentEmail).first()
        if student:
            flash(message='user already exists', category='error')
        elif len(firstName) <2:
            flash(message='Invalid First Name', category='error')
        elif len(lastName) <2:
            flash(message='Invalid Last Name', category='error')
        elif len(studentEmail) <8:
            flash(message='Student number must be 8 digits', category='error')
        elif password != password2:
            flash(message='passwords do not match', category='error')
        elif len(department) <2:
            flash(message='please select a department', category='error')
        else:
            new_user = Student(studentEmail=studentEmail, firstName=firstName, lastName=lastName,password=generate_password_hash(password,  method='pbkdf2:sha256'), department=department)
            db.session.add(new_user)
            db.session.commit()
            new_user2 = Admin(AdminEmail='admin@gmail.com', firstName='caldon', lastName='jainarayan', password=generate_password_hash('12345678', method='pbkdf2:sha256'))
            db.session.add(new_user2)
            db.session.commit()
            """
            sponsor_data=Sponsorship(AcompanyName="Absa",BOpeningDate="23 Match 2024",CclosingDate="24 October 2024",Ddepartment="Accountin and Informatics",EApplicationLink="https://www.twitch.tv/")
            db.session.add(sponsor_data)
            sponsor_data=Sponsorship(AcompanyName="HBO",BOpeningDate="14 May 2024",CclosingDate="23 November 2024",Ddepartment="Accountin and Informatics",EApplicationLink="https://www.twitch.tv/")
            db.session.add(sponsor_data)
            sponsor_data=Sponsorship(AcompanyName="PnP",BOpeningDate="18 April 2024",CclosingDate="18 June 2024",Ddepartment="Accountin and Informatics",EApplicationLink="https://www.twitch.tv/")
            db.session.add(sponsor_data)
            sponsor_data=Sponsorship(AcompanyName="Tokyo Toys",BOpeningDate="20 Feburary 2024",CclosingDate="30 October 2024",Ddepartment="Accountin and Informatics",EApplicationLink="https://www.twitch.tv/")
            db.session.add(sponsor_data)
            sponsor_data=Sponsorship(AcompanyName="Dell",BOpeningDate="23 Janurary 2024",CclosingDate="15 December 2024",Ddepartment="Accountin and Informatics",EApplicationLink="https://www.twitch.tv/")
            db.session.add(sponsor_data)
            sponsor_data=Sponsorship(AcompanyName="Microsoft",BOpeningDate="30 April 2024",CclosingDate="20 July 2024",Ddepartment="Accountin and Informatics",EApplicationLink="https://www.twitch.tv/")
            db.session.add(sponsor_data)
            grant_data=Grant(GAcompanyName="Apple",GBOpeningDate="28 March 2024",GCclosingDate="24 October 2024",GDdepartment="Accountin and Informatics",GEApplicationLink="https://www.twitch.tv/")
            db.session.add(grant_data)
            bursary_data=Bursary(BAcompanyName="Dell",BBOpeningDate="28 March 2024",BCclosingDate="24 October 2024",BDdepartment="Accountin and Informatics",BEApplicationLink="https://www.twitch.tv/")
            db.session.add(bursary_data)
            bursary_data=Bursary(BAcompanyName="Lenovo",BBOpeningDate="28 March 2024",BCclosingDate="24 October 2024",BDdepartment="Accountin and Informatics",BEApplicationLink="https://www.twitch.tv/")
            db.session.add(bursary_data)    
            db.session.commit()
            """
        flash(message='Account created successfully!', category='success')
        """
        email="fundingfinderproject@gmail.com" #input("SENDER EMAIL: ")
            

        subject= "DUT Funding Finder Email Conformation"#input("SUBJECT: ")
        message = "Whazzup boi You have successfully signed up to the DUT Finding Finder....This is definitely not spam."#input("MESSAGE: ")

        text = f"Subject: {subject}\n\n{message}"

        server = smtplib.SMTP("smtp.gmail.com",587)
        server.starttls()

        server.login(email, "ewyv ipbu qrla gqpy")

        server.sendmail(email, studentEmail, text)
        """

        flash( message="email sent to "+ studentEmail, category="success")
        return redirect(url_for('auth.login'))
    return render_template('sign_up.html', user=current_user)


@auth.route('/login', methods=['GET','POST'])
def login():
    """    if request.method == 'POST':
        loginEmail = request.form.get('studentEmail')
        password = request.form.get('password')

        student = Student.query.filter_by(studentEmail=loginEmail).first()
        if student:
            if check_password_hash(student.password, password):
                login_user(student, remember=True)
                flash(message='Logged in successfully!', category='error')
                return render_template('sponsorships.html', user=current_user)
            else:
                flash(message='incorrect password', category='error')
        else:
            flash(message='user does not exist', category='error')"""
    if request.method == 'POST':
        loginEmail = request.form.get('studentEmail')
        password = request.form.get('password')

        student = Student.query.filter_by(studentEmail=loginEmail).first()
        if student:
            if check_password_hash(student.password, password):
                flash(message='Logged in successfully!', category='success')
                login_user(student, remember=True)
                return redirect(url_for('auth.sponsorshipsStudent', user=current_user))
            else:
                flash(message='incorrect password', category='error')
        else:
            flash(message='user does not exist', category='error')
    return render_template('loginStudent.html', user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/adminPage',methods=['GET','POST'])
def adminPage():
    all_data =  Sponsorship.query.all()

    return render_template('adminPage.html',sponsors=all_data, user=current_user)

@auth.route('/adminLoginPage', methods=['GET', 'POST'])
def adminLoginPage():
    if request.method == 'POST':
        loginEmail = request.form.get('AdminEmail')
        password = request.form.get('password')

        admin = Admin.query.filter_by(AdminEmail=loginEmail).first()
        if admin:
            if check_password_hash(admin.password, password):
                flash(message='Logged in successfully!', category='success')
                login_user(admin, remember=True)
                return redirect(url_for ('auth.adminPage'))
                #return render_template('adminPage.html', user=current_user)
            else:
                flash(message='incorrect password', category='error')
        else:
            flash(message='user does not exist', category='error')
    return render_template('adminLoginPage.html', user=current_user)


@auth.route('/sponsor')
def get_sponsors():
    sponsors = Sponsorship.query.all()

    output = []
    for sponsor in sponsors:
        sponsor_data={'id':sponsor.id,'CompanyName':sponsor.AcompanyName,'OpeningDate':sponsor.BOpeningDate,'ClosingDate':sponsor.CclosingDate,'ApplicationEmail':sponsor.companyEmail,'Department':sponsor.Ddepartment,'Extra Requirements':sponsor.add_req}

        output.append(sponsor_data)

    return{"sponsor":output}

@auth.route('/sponsors/<id>')
def get_sponsor(id):
    sponsor = Sponsorship.query.get_or_404(id)
    return {"Company":sponsor.companyName,"Opening Date":sponsor.OpeningDate,"Closing Date":sponsor.closingDate, "ApplicationLink":sponsor.ApplicationLink  ,"Department":sponsor.department, "Type":sponsor.type  }

@auth.route('/sponsor/',methods=['POST'])
def add_sponsor():
    sponsor = Sponsorship(AcompanyName=request.json['companyName'], BOpeningDate= request.json['OpeningDate'], CclosingDate= request.json['closingDate'],EApplicationLink=request.json['ApplicationLink'],Ddepartment=request.json['department'], FType=request.json['type'])
    db.session.add(sponsor)
    db.session.commit()
    return {'id':sponsor.id}

@auth.route('/sponsor/<id>',methods=['DELETE' , 'GET'])
def delete_sponsor(id):
    sponsor_id = request.form.get('id')
    sponsor = Sponsorship.query.get(id)
    if sponsor is None:
        return {"error":"not found"}
    db.session.delete(sponsor)
    db.session.commit()
    return {"message":"Deleted"}

@auth.route('/createSponsor', methods=['GET','POST'])
def createSponsor():
 if request.method == 'POST':
     companyName=request.form.get('companyName')
     openingDate=request.form.get('oDate')
     openingDate=str(openingDate)
     closingDate=request.form.get('cDate')
     closingDate=str(closingDate)
     applicationLink=request.form.get('applicationLink')
     department=request.form.get('department')
     type=request.form.get('type')
     if type == "Ftype":
        new_record= Sponsorship(AcompanyName=companyName, BOpeningDate=openingDate, CclosingDate=closingDate,EApplicationLink=applicationLink ,Ddepartment=department,FType=type)
        db.session.add(new_record)
        db.session.commit()
     elif type == "GFtype":
        new_record= Grant(GAcompanyName=companyName, GBOpeningDate=openingDate, GCclosingDate=closingDate,GEApplicationLink=applicationLink ,GDdepartment=department, GFtype=type)
        db.session.add(new_record)
        db.session.commit()
     else:
        new_record= Bursary(BAcompanyName=companyName, BBOpeningDate=openingDate, BCclosingDate=closingDate,BEApplicationLink=applicationLink ,BDdepartment=department, BFtype=type)
        db.session.add(new_record)
        db.session.commit()
         
        
         
     if len(companyName) > 0 :
         flash(message="Record submitted successfully" , category='success')
 else:
     flash(message="Record not submitted " , category='error')
 return render_template('createSponsor.html', user=current_user)
    
    
@auth.route('/addAdmin', methods=['GET' , 'POST'])
def createAdmin():
    if request.method =='POST':
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        adminEmail = request.form.get('adminEmail')
        password = request.form.get('password')
        password2 = request.form.get('password2')

        admin = Admin.query.filter_by(AdminEmail=adminEmail).first()
        if admin:
            flash(message='user already exists', category='error')
        elif len(firstName) <2:
            flash(message='Invalid First Name', category='error')
        elif len(lastName) <2:
            flash(message='Invalid Last Name', category='error')
        elif len(adminEmail) <8:
            flash(message='Student number must be 8 digits', category='error')
        elif password != password2:
            flash(message='passwords do not match', category='error')
        else:
            new_user = Admin(AdminEmail=adminEmail, firstName=firstName, lastName=lastName,password=generate_password_hash(password,  method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()         
            
            flash(message='Account created successfully!', category='success')
            return redirect(url_for('auth.adminLoginPage'))

    return render_template('addAdmin.html', user = current_user) 


"""

email="fundingfinderproject@gmail.com" #input("SENDER EMAIL: ")
receiver_email = input("RECIEVER EMAIL: ") #getting reciever email from sign up

subject= "DUT Funding Finder Email Conformation"#input("SUBJECT: ")
message = "You have successfully signed up to the DUT Finding Finder"#input("MESSAGE: ")

text = f"Subject: {subject}\n\n{message}"

server = smtplib.SMTP("smtp.gmail.com",587)
server.starttls()

server.login(email, "ewyv ipbu qrla gqpy")

server.sendmail(email, receiver_email, text)

print("email sent to "+ receiver_email)"""



@auth.route('/grants')
def get_grants():
    grants = Grant.query.all()

    output = []
    for grant in grants:
        grant_data={'id':grant.id,'CompanyName':grant.GAcompanyName,'OpeningDate':grant.GBOpeningDate,'ClosingDate':grant.GCclosingDate,'ApplicationLink':grant.GEApplicationLink,'Department':grant.GDdepartment, 'Type': grant.GFtype}

        output.append(grant_data)

    return{"grant":output}

@auth.route('/grants/<id>')
def get_grant(id):
    grant = Grant.query.get_or_404(id)
    return {"Company":grant.GAcompanyName,"Opening Date":grant.GBOpeningDate,"Closing Date":grant.GCclosingDate, "ApplicationLink":grant.GEApplicationLink  ,"Department":grant.GDdepartment, "Type":grant.GFtype}

@auth.route('/grant/',methods=['POST'])
def add_grant():
    grant = Grant(GAcompanyName=request.json['companyName'], GBOpeningDate= request.json['OpeningDate'], GCclosingDate= request.json['closingDate'],GEApplicationLink=request.json['ApplicationLink'],GDdepartment=request.json['department'], GFtype=request.json['type'])
    db.session.add(grant)
    db.session.commit()
    return {'id':grant.id}

@auth.route('/grant/<id>',methods=['DELETE' , 'GET'])
def delete_grant(id):
    grant_id = request.form.get('id')
    grant = Grant.query.get(id)
    if grant is None:
        return {"error":"not found"}
    db.session.delete(grant)
    db.session.commit()
    return {"message":"Deleted"}

@auth.route('/createGrant', methods=['GET','POST'])
def createGrant():
 if request.method == 'POST':
     companyName=request.form.get('companyName')
     openingDate=request.form.get('oDate')
     openingDate=str(openingDate)
     closingDate=request.form.get('cDate')
     closingDate=str(closingDate)
     applicationLink=request.form.get('applicationLink')
     department=request.form.get('department')
     type=request.form.get('type')
     new_record= Grant(GAcompanyName=companyName, GBOpeningDate=openingDate, GCclosingDate=closingDate,GEApplicationLink=applicationLink ,GDdepartment=department, GFtype=type)
     db.session.add(new_record)
     db.session.commit()
     if len(companyName) > 0 :
         flash(message="Record submitted successfully" , category='success')
 else:
     flash(message="Record not submitted " , category='error')
 return render_template('createSponsor.html', user=current_user)
    


@auth.route('/bursaries')
def get_bursarys():
    bursaries = Bursary.query.all()

    output = []
    for bursary in bursaries:
        bursaries_data={'id':bursary.id,'CompanyName':bursary.BAcompanyName,'OpeningDate':bursary.BBOpeningDate,'ClosingDate':bursary.BCclosingDate,'ApplicationLink':bursary.BEApplicationLink,'Department':bursary.BDdepartment, 'Type': bursary.BFtype}

        output.append(bursaries_data)

    return{"bursary":output}

@auth.route('/bursaries/<id>')
def get_bursary(id):
    bursary = Bursary.query.get_or_404(id)
    return {"Company":bursary.BAcompanyName,"Opening Date":bursary.BBOpeningDate,"Closing Date":bursary.BCclosingDate, "ApplicationLink":bursary.BEApplicationLink  ,"Department":bursary.BDdepartment, "Type":bursary.BFtype}

@auth.route('/bursary/',methods=['POST'])
def add_bursary():
    bursary = Bursary(BAcompanyName=request.json['companyName'], BBOpeningDate= request.json['OpeningDate'], BCclosingDate= request.json['closingDate'],BEApplicationLink=request.json['ApplicationLink'],BDdepartment=request.json['department'], BFtype=request.json['type'])
    db.session.add(bursary)
    db.session.commit()
    return {'id':bursary.id}

@auth.route('/bursary/<id>',methods=['DELETE' , 'GET'])
def delete_bursary(id):
    bursary_id = request.form.get('id')
    bursary = Bursary.query.get(id)
    if bursary is None:
        return {"error":"not found"}
    db.session.delete(bursary)
    db.session.commit()
    return {"message":"Deleted"}

@auth.route('/createBursary', methods=['GET','POST'])
def createBursary():
 if request.method == 'POST':
     companyName=request.form.get('companyName')
     openingDate=request.form.get('oDate')
     openingDate=str(openingDate)
     closingDate=request.form.get('cDate')
     closingDate=str(closingDate)
     applicationLink=request.form.get('applicationLink')
     department=request.form.get('department')
     type=request.form.get('type')
     new_record= Bursary(BAcompanyName=companyName, BBOpeningDate=openingDate, BCclosingDate=closingDate,BEApplicationLink=applicationLink ,BDdepartment=department, BFtype=type)
     db.session.add(new_record)
     db.session.commit()
     if len(companyName) > 0 :
         flash(message="Record submitted successfully" , category='success')
 else:
     flash(message="Record not submitted " , category='error')
 return render_template('createSponsor.html', user=current_user)
    

@auth.route('/edit/<int:id>', methods=['GET','POST'])
def edit(id):
    
    update_record = Sponsorship.query.get_or_404(id)
    if request.method == 'POST':
        update_record.AcompanyName=request.form.get['companyName']
        update_record.BOpeningDate=request.form.get['oDate']
        update_record.CclosingDate=request.form.get['cDate']
        update_record.Ddepartment=request.form.get['department']
        update_record.EApplicationLink=request.form.get['applicationLink']

        try:
            db.session.commit()
            flash(message="User is updated",category="success")
            return render_template("edit.html",user=current_user)
        except:
            flash(message="Looks like a nathan",category="error")
            return render_template("edit.html",user=current_user)
    else:
        return render_template("edit.html",user=current_user)
    return render_template('edit.html', user=current_user)
#adminPage table
@auth.route('/insert', methods=['POST'])
def insert():
    if request.method == 'POST':
        AcompanyName=request.form['companyName']
        BOpeningDate=request.form['OpeningDate']
        CclosingDate=request.form['closingDate']
        Ddepartment=request.form['department']
        add_req=request.form['add_req']
        companyEmail=request.form['companyEmail']


        my_data = Sponsorship(AcompanyName,BOpeningDate,CclosingDate,Ddepartment,companyEmail, add_req)
        db.session.add(my_data)
        db.session.commit()

        flash(message="Sponsor Added!", category='success')

        return redirect(url_for('auth.adminPage'))
    
@auth.route('/update',methods = ['GET','POST'])
def update():
    if request.method=='POST':
        my_data = Sponsorship.query.get(request.form.get('id'))

        my_data.AcompanyName=request.form['companyName']
        my_data.BOpeningDate=request.form['OpeningDate']
        my_data.CclosingDate=request.form['closingDate']
        my_data.Ddepartment=request.form['department']
        my_data.companyEmail=request.form['companyEmail']
        
        db.session.commit()
        flash("Sponsor Updated!")

        return redirect(url_for('auth.adminPage'))
    
@auth.route('/delete/<id>/', methods=['GET', 'POST'])
def delete(id):
    my_data = Sponsorship.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Sponsor Deleted Successfully!")
 
    return redirect(url_for('auth.adminPage'))
#bursary Table
@auth.route('/insertBursary', methods=['POST'])
def insertBursary():
    if request.method == 'POST':
        BAcompanyName=request.form['companyName']
        BBOpeningDate=request.form['OpeningDate']
        BCclosingDate=request.form['closingDate']
        BDdepartment=request.form['department']
        companyEmail=request.form['companyEmail']
        add_req=request.form['add_req']

        my_data = Bursary(BAcompanyName,BBOpeningDate,BCclosingDate,BDdepartment,companyEmail,add_req)
        db.session.add(my_data)
        db.session.commit()

        flash("Bursary Added!")

        return redirect(url_for('auth.bursaryPage'))
    
@auth.route('/updateBursary',methods = ['GET','POST'])
def updateBursary():
    if request.method=='POST':
        my_data = Bursary.query.get(request.form.get('id'))

        my_data.BAcompanyName=request.form['companyName']
        my_data.BBOpeningDate=request.form['OpeningDate']
        my_data.BCclosingDate=request.form['closingDate']
        my_data.BDdepartment=request.form['department']
        my_data.companyEmail=request.form['companyEmail']
        my_data.add_req = request.form['add_req']

        db.session.commit()
        flash(message="Bursary Updated!",category='success')

        return redirect(url_for('auth.bursaryPage'))
    
@auth.route('/deleteBursary/<id>/', methods=['GET', 'POST'])
def deleteBursary(id):
    my_data = Bursary.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Bursary Deleted Successfully!")
 
    return redirect(url_for('auth.bursaryPage'))

@auth.route('/bursaryPage',methods=['GET','POST'])
def bursaryPage():
    all_data =  Bursary.query.all()
    return render_template('bursary.html',sponsors=all_data, user=current_user)

#grants table
@auth.route('/insertGrants', methods=['POST'])
def insertGrants():
    if request.method == 'POST':
        GAcompanyName=request.form['companyName']
        GBOpeningDate=request.form['OpeningDate']
        GCclosingDate=request.form['closingDate']
        GDdepartment=request.form['department']
        companyEmail=request.form['companyEmail']
        add_req=request.form['add_req']

        my_data = Grant(GAcompanyName,GBOpeningDate,GCclosingDate,GDdepartment,companyEmail,add_req)
        db.session.add(my_data)
        db.session.commit()

        flash("Grant Added!")

        return redirect(url_for('auth.grantsPage'))
    
@auth.route('/updateGrant',methods = ['GET','POST'])
def updateGrant():
    if request.method=='POST':
        my_data = Grant.query.get(request.form.get('id'))

        my_data.GAcompanyName=request.form['companyName']
        my_data.GBOpeningDate=request.form['OpeningDate']
        my_data.GCclosingDate=request.form['closingDate']
        my_data.GDdepartment=request.form['department']
        my_data.companyEmail=request.form['companyEmail']
        my_data.add_req=request.form['add_req']
        
        db.session.commit()
        flash("Grant Updated!")

        return redirect(url_for('auth.grantsPage'))
    
@auth.route('/deleteGrant/<id>/', methods=['GET', 'POST'])
def deleteGrant(id):
    my_data = Grant.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Grant Deleted Successfully!")
 
    return redirect(url_for('auth.grantsPage'))

@auth.route('/grantsPage',methods=['GET','POST'])
def grantsPage():
    all_data =  Grant.query.all()
    return render_template('grants.html',sponsors=all_data, user=current_user)

@auth.route('/sponsorshipsStudent')
def sponsorshipsStudent():
     all_data =  Sponsorship.query.all()
     return render_template('sponsorships.html',sponsors=all_data,user=current_user)

@auth.route('/grantsStudent' )
def grants():
    all_data =  Grant.query.all()
    return render_template('studentGrantPage.html',sponsors=all_data,user=current_user)

@auth.route('/bursaryStudent')
def bursary():
    all_data =  Bursary.query.all()
    return render_template('studentBursaryPage.html',sponsors=all_data,user=current_user)


@auth.route('/adminBursaryPage')
def aBursaryPage():
    return render_template('adminBursaryPage.html')

@auth.route('/adminGrantPage')
def aGrantPage():
    return render_template('adminGrantPage.html')