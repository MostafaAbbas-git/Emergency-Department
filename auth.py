from flask import Blueprint, render_template, redirect, url_for, request, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, Role, contactForm, FileModel, PatientModel, EventModel
from db import db
from flask_login import login_user, logout_user, login_required, current_user
from flask_user import login_required, roles_required, roles_accepted
import pickle
import os

auth = Blueprint('auth', __name__)


@auth.route('/')
def home():
    # Create 'admin@example.com' user with 'Admin' and 'Agent' roles
    if not User.query.filter(User.email == 'admin@emergency.com').first():
        user = User(
            email='admin@emergency.com', active=True,
            password=generate_password_hash("admin", method='sha256'), name='Creator',
            secret_key = "ADMIN"
        )
        user.roles.append(Role(name='Admin'))
        db.session.add(user)
        db.session.commit()

    return render_template('index.html')


@auth.route('/index')
def index():
    return render_template('index.html')


@auth.route('/aboutus')
def aboutus():
    return render_template('about-us.html')


@auth.route('/contactus')
def contactus():
    return render_template('contact-us.html')


@auth.route('/contactus', methods=['POST', 'GET'])
def contactus_post():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        subject = request.form.get('subject')
        message = request.form.get('message')

        user_msg = contactForm(email=email, name=name,
                               subject=subject, message=message)
        db.session.add(user_msg)
        db.session.commit()
        flash("Admins will contact you back ASAP.")
        return redirect(url_for('auth.contactus'))
    else:
        flash("Your message is empty. Please fill all the fields.")
    return redirect(url_for('auth.contactus'))


@auth.route('/login')
def login():
    return render_template('login.html')


@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')  # done
        # if the user doesn't exist or password is wrong, reload the page
        return redirect(url_for('auth.login'))

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for('auth.index'))


@auth.route('/signup')
def signup():
    return render_template('signup.html')


@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    national_id = request.form.get('national_id')
    department = request.form.get('department')
    nationality = request.form.get('nationality')
    phone_num = request.form.get('phone_num')

    # if this returns a user, then the email already exists in database
    user = User.query.filter_by(email=email).first()

    if user:  # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists')  # done
        return redirect(url_for('auth.signup'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(email=email, name=name,
                    password=generate_password_hash(password, method='sha256'),
                    phone_num=phone_num, nationality=nationality,
                    national_id=national_id, department=department, active=True)

    new_user.roles.append(Role(name='Doctor'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))


# dashboard page

@auth.route('/dashboard')
@roles_accepted('Admin')
def dashboard_form():
    return render_template('dashboard.html')


########

# "dashboard-control page"-
# (ACCESSED BY ADMINS ONLY)
# contains ADD and REMOVE patient funcs, EDIT and REMOVE doctor from db


@auth.route('/dashboard-control')
@roles_accepted('Admin')
def dashboard_control_form():
    return render_template('dashboard-control.html')


@auth.route('/dashboard-add-patient', methods=['POST', 'GET'])
@roles_accepted('Admin')
def dashboard_add_patient():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        age = request.form.get('age')
        national_id = request.form.get('national_id')
        medical_history = request.form.get('medical_history')
        phone_num = request.form.get('phone_num')
        Address = request.form.get('Address')
        gender = request.form.get('gender')
        imagesList = request.files.getlist("inputFile")

        check = PatientModel.query.filter_by(national_id=national_id).first()

        if check:  # if a patient already exists by its id, we flash a msg that he is already in the database.
            flash('Patient with same ID already exists.')
            return redirect(url_for('auth.dashboard_control_form'))

        patient = PatientModel(name=name, email=email, age=age,
                               national_id=national_id, medical_history=medical_history,
                               phone_num=phone_num, Address=Address, gender=gender, action="No Action added yet.")

        db.session.add(patient)
        db.session.commit()
        folder_path = os.path.join("static", "images", str(patient.id))
        os.mkdir(folder_path)

        for image in imagesList:
            newFile = FileModel(name=os.path.join(
                folder_path, image.filename), patient_id=patient.id)
            image.save(os.path.join(folder_path, image.filename))
            db.session.add(newFile)

        db.session.commit()
        flash(f"{patient.name} has been successfully added to the system!")

        return render_template('dashboard-control.html')

    else:

        return render_template('dashboard-control.html')


@auth.route('/dashboard-add-admin', methods=['POST', 'GET'])
@roles_accepted('Admin')
def dashboard_add_admin():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        name = request.form.get('name')
        secret_key = request.form.get('secret_key')
        # if this returns a user, then the email already exists in database
        user = User.query.filter_by(email=email).first()

        if user:  # if a user is found, we want to redirect back to signup admin page so user can try again
            flash('Email address of this admin already exists')
            return redirect(url_for('auth.dashboard_control_form'))

        if secret_key == "ADMIN":
            # create a new user with the form data. Hash the password so the plaintext version isn't saved.
            new_user = User(email=email, name=name,
                            password=generate_password_hash(password, method='sha256'),
                            secret_key=secret_key, active=True)
            new_user.roles.append(Role(name='Admin'))

            # add the new user to the database
            db.session.add(new_user)
            db.session.commit()
            # after creating new admin, you get flash msg and redirected to the same page again.
            flash('New admin was created successfully!')
        else:
            flash("Secret key isn't correct.")

        return redirect(url_for('auth.dashboard_control_form'))
    else:
        return render_template('dashboard-control.html')


@auth.route('/dashboard-add-event', methods=['POST', 'GET'])
@roles_accepted('Admin')
def dashboard_add_event():
    if request.method == 'POST':
        national_id = request.form.get('national_id')
        title = request.form.get('title')
        start = request.form.get('start')
        end = request.form.get('end')
        description = request.form.get('description')

        doctor = User.query.filter_by(national_id=national_id).first()
        if not doctor:
            flash('Not valid National ID')
        else:
            event = EventModel(start=start, end=end, title=title,
                               description=description, doctor_id=doctor.id)
            db.session.add(event)
            db.session.commit()
            flash('New event was created successfully!')

        return redirect(url_for('auth.dashboard_control_form'))
    else:
        return render_template('dashboard-control.html')


@auth.route('/dashboard-edit-event', methods=['POST', 'GET'])
@roles_accepted('Admin')
def dashboard_edit_event():
    if request.method == 'POST':
        national_id = request.form.get('national_id')
        event_id = request.form.get('event_id')
        title = request.form.get('title')
        start = request.form.get('start')
        end = request.form.get('end')
        description = request.form.get('description')

        doctor = User.query.filter_by(national_id=national_id).first()
        event = EventModel.query.filter_by(id=event_id).first()
        if not doctor and event:
            flash('Not valid National ID')
        elif not event and doctor:
            flash('Not valid Event ID')
        else:
            event.title = title
            event.start = start
            event.end = end
            event.description = description
            db.session.commit()
            flash('Event Updated successfully!')

        return redirect(url_for('auth.dashboard_control_form'))
    else:
        return render_template('dashboard-control.html')


@auth.route('/dashboard-delete-event', methods=['POST', 'GET'])
@roles_accepted('Admin')
def dashboard_delete_event():
    if request.method == 'POST':
        event_id = request.form.get('event_id')
        event = EventModel.query.filter_by(id=event_id).first()
        if not event:
            flash('No Event on the system with ID you entered')
        else:
            db.session.delete(event)
            db.session.commit()
            flash('Event deleted successfully')
        return redirect(url_for('auth.dashboard_control_form'))
    else:
        return render_template('dashboard-control.html')


@auth.route('/dashboard-delete-patient', methods=['POST', 'GET'])
@roles_accepted('Admin')
def dashboard_delete_patient():
    if request.method == 'POST':
        national_id = request.form.get('national_id')
        patient = PatientModel.query.filter_by(national_id=national_id).first()
        if patient:
            db.session.delete(patient)
            db.session.commit()

            flash("patient has been successfully deleted from the system!")
            return redirect(url_for('auth.dashboard_control_form'))
        else:
            flash("patient doesn't exist on the system!")
            return redirect(url_for('auth.dashboard_control_form'))

    return redirect(url_for('auth.dashboard_control_form'))


@auth.route('/dashboard-delete-doctor', methods=['POST', 'GET'])
@roles_accepted('Admin')
def dashboard_delete_doctor():
    if request.method == 'POST':
        national_id = request.form.get('national_id')
        doctor = User.query.filter_by(national_id=national_id).first()
        if doctor:
            db.session.delete(doctor)
            db.session.commit()

            flash("doctor has been successfully deleted from the system!")
            return redirect(url_for('auth.dashboard_control_form'))
        else:
            flash("doctor doesn't exist on the system!")
            return redirect(url_for('auth.dashboard_control_form'))

    return redirect(url_for('auth.dashboard_control_form'))


@auth.route('/dashboard-delete-admin', methods=['POST', 'GET'])
@roles_accepted('Admin')
def dashboard_delete_admin():
    if request.method == 'POST':
        email = request.form.get('email')
        admin = User.query.filter_by(email=email).first()
        if admin:
            db.session.delete(admin)
            db.session.commit()

            flash("admin has been successfully deleted from the system!")
            return redirect(url_for('auth.dashboard_control_form'))
        else:
            flash("doctor doesn't exist on the system!")
            return redirect(url_for('auth.dashboard_control_form'))

    return redirect(url_for('auth.dashboard_control_form'))


@auth.route('/dashboard-edit-doctor', methods=['POST', 'GET'])
@roles_accepted('Admin')
def dashboard_edit_doctor():
    if request.method == 'POST':  # check if there is post data
        national_id = request.form.get('national_id')
        new_email = request.form.get('new_email')
        new_department = request.form.get('new_department')
        new_phone_num = request.form.get('new_phone_num')

        doctor = User.query.filter_by(national_id=national_id).first()
        if doctor:
            doctor.email = new_email
            doctor.department = new_department
            doctor.phone_num = new_phone_num
            db.session.commit()
            flash(f"{doctor.name} has been successfully Updated!")
        else:
            flash("There's no Doctor on the database with the national_id you entered. Please try again with correct inputs.")
        return redirect(url_for('auth.dashboard_control_form'))

    return render_template('dashboard-control.html')

# simple error: you cant update only one column, you have to fill all the field, otherwise it will return NULL
# which will replace the original value.


@auth.route('/dashboard-edit-patient', methods=['POST', 'GET'])
@roles_accepted('Admin')
def dashboard_edit_patient():
    if request.method == 'POST':  # check if there is post data
        national_id = request.form.get('national_id')
        new_email = request.form.get('new_email')
        new_phone_num = request.form.get('new_phone_num')
        new_medical_history = request.form.get('new_medical_history')
        new_Address = request.form.get('new_Address')
        new_file = request.files["inputFile"]

        patient = PatientModel.query.filter_by(national_id=national_id).first()

        newFile = FileModel(
            name=new_file.filename, data=new_file.read(), patient_id=patient.id)
        if patient:
            patient.medical_history = new_medical_history
            patient.email = new_email
            patient.Address = new_Address
            patient.phone_num = new_phone_num
            db.session.add(newFile)
            db.session.commit()
            flash(f"{patient.name} has been successfully Updated!")
        else:
            flash("There's no patient on the database with the national_id you entered. Please try again with correct inputs.")
        return redirect(url_for('auth.dashboard_control_form'))

    return render_template('dashboard-control.html')

########

# dashboard-report page(ACCESSED BY DOCTORS), contains all reports about patients in db and posting new report.

# if this method didnt work properly, you may add new button to show the reports on the database,
# and connect it with another auth.route with a post method and leave the default method that shows the dasboard-report alone.


@auth.route('/dashboard-report')
@roles_accepted('Doctor')
def dashboard_report_form():
    patient_rows = PatientModel.query.all()
    event_rows = EventModel.query.filter_by(doctor_id=current_user.id).all()
    return render_template('dashboard-report.html', patient_rows=patient_rows, event_rows=event_rows)


# To create a new report about specific patient (stored in patientModel.action)
@auth.route('/dashboard-report-post', methods=['POST', 'GET'])
@roles_accepted('Doctor')
def dashboard_report_post():
    if request.method == 'POST':
        national_id = request.form.get('national_id')
        action = request.form.get('action')

        patient = PatientModel.query.filter_by(national_id=national_id).first()
        if patient:
            patient.action = action
            db.session.commit()
            flash(
                f"A report about {patient.name} was successfully added to the database")
        else:
            flash("There's no patient on the database with the national_id you entered.")
        return redirect(url_for('auth.dashboard_report_form'))

    return render_template('dashboard-report.html')

########
# dashboard-DATABASE page(ACCESSED BY ADMINS), contains all Tables of the DATABASE.


@auth.route('/dashboard-database')
@roles_accepted('Admin')
def dashboard_database_form():

    patient_rows = PatientModel.query.all()
    doctor_rows = User.query.filter_by(secret_key=None).all()
    admin_rows = User.query.filter_by(secret_key="ADMIN").all()
    # admin_rows = User.query.filter(User.name.startswith('Admin')).all()
    contact_rows = contactForm.query.all()
    events_rows = EventModel.query.all()
    return render_template('dashboard-database.html',
                           patient_rows=patient_rows,
                           doctor_rows=doctor_rows,
                           admin_rows=admin_rows,
                           contact_rows=contact_rows,
                           events_rows=events_rows
                           )

# Showing images related to each patient


@auth.route('/<national_id>')
@roles_accepted('Admin')
def return_image(national_id):
    patient = PatientModel.query.filter_by(national_id=national_id).first()
    if patient:
        data = FileModel.query.filter_by(patient_id=patient.id)
    else:
        data = None
    return render_template('images.html', data=data, patient=patient)
########


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out!')  # done
    return redirect(url_for('auth.index'))

# date = datetime.now().strftime("%Y/%m/%dT%H:%M:%S") ll calender
