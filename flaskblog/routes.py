from flask import render_template, url_for, flash, redirect,request
from flaskblog import app,db,bcrypt
from flaskblog.forms import *
from flaskblog.models import User, Complaint
from flask_login import login_user,current_user,logout_user,login_required
from flask_datepicker import datepicker
import os

@app.route("/home")
@login_required
def home():
    return render_template('home.html')

@app.route("/", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user)
            flash(f'You are logged in','success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash(f'Login Unsuccessful. Please check email and password','danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/adminlogin", methods=['GET', 'POST'])
def adminlogin():

    form = AdminLoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user)
            if(current_user.username=='admin'):
                flash(f'You are logged in as ADMIN','success')
                return redirect(url_for('showcomplaints'))
            else:
                flash(f'You\'re not an admin,Switch to User login','danger')
        else:
            flash(f'Login Unsuccessful. Please check email and password','danger')
    return render_template('adminlogin.html', title='Login', form=form)




@app.route("/complaint",methods=['GET','POST'])
@login_required
def complaint():
    if(current_user.username=='admin'):
        flash(f'Login From a user account to register complaint','danger')
        return(redirect(url_for('showcomplaints')))

    else:

        form=ComplaintForm()
        if  form.validate_on_submit():
                complaint=Complaint(complainant = form.complainant.data,
                victim=form.victim.data,
                victph=form.victph.data,
                compph = form.compph.data,
                doc=form.doc.data,
                accused=form.accused.data,
                description=form.description.data,
                sections=form.sections.data,
                compadd=form.compadd.data,
                victadd=form.victadd.data,
                author=current_user)
                db.session.add(complaint)
                db.session.commit()
                flash(f'Your complaint has been registered. You will be contacted by our officer shortly.','success')
                return redirect(url_for('mycomplaints'))
        return render_template('complaint.html',title='Complaint Registration',form=form)



@app.route("/about")
@login_required
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash('You are already logged in', 'success')
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user=User(username=form.username.data,email=form.email.data,password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/showcomplaints',methods=['GET', 'POST'])
@login_required
def showcomplaints():
    print(current_user)
    if(current_user.username=='admin'):
            complaints=Complaint.query.all()
            if complaints==[]:
                flash(f"No Active  Complaints", "danger")

            return render_template('showcomplaints.html', title='Registered  Complaints',complaints=complaints)
    else:
        flash(f'This page is for admins only', 'danger')
        return(redirect(url_for('about')))
    
@app.route('/updatecomplaint<int:complaint_id>',methods=['GET', 'POST'])
@login_required
def updatecomplaint(complaint_id):
    if(current_user.username=='admin'):
        complaint=Complaint.query.get_or_404(complaint_id)
        form=ComplaintForm()
        if form.validate_on_submit():
            complaint.complainant=form.complainant.data
            complaint.victim=form.victim.data
            complaint.victph=form.victph.data
            complaint.compph = form.compph.data
            complaint.doc=form.doc.data
            complaint.accused=form.accused.data
            complaint.description=form.description.data
            complaint.sections=form.sections.data
            db.session.commit()
            flash('Your complaint has been updated!', 'success')
            return redirect(url_for('showcomplaints'))
        elif request.method == 'GET':
            form.complainant.data= complaint.complainant
            form.victim.data=complaint.victim
            form.victph.data=complaint.victph
            form.compph.data=complaint.compph 
            form.doc.data=complaint.doc
            form.accused.data=complaint.accused
            form.description.data=complaint.description
            form.sections.data=complaint.sections
            return render_template('updatecomplaint.html', title='Update  Complaint',form=form)
    else:
            flash(f"The page you're trying to access  is for admins only",'danger')
            return(redirect(url_for('about')))

@app.route('/deletecomplaint<int:complaint_id>',methods=['GET', 'POST'])
@login_required
def delete_complaint(complaint_id):
    
        complaint=Complaint.query.get_or_404(complaint_id)
        db.session.delete(complaint)
        db.session.commit()
        flash('Your complaint has been deleted!', 'success')
        if(current_user.username=='admin'):
            return redirect(url_for('showcomplaints'))
        else:
            return redirect(url_for('mycomplaints'))


@app.route('/mycomplaints',methods=['GET','POST'])
@login_required
def mycomplaints():
    complaints=Complaint.query.filter_by(user_id=current_user.id)
    if(current_user.username=='admin'):
         flash(f"Login from user account for this page",'success')
         return(redirect(url_for('showcomplaints')))
    elif complaints==[]:
        flash(f"No Active  Complaints", "danger")
    else:
        return render_template('mycomplaints.html', title='Registered  Complaints',complaints=complaints)