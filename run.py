from flask import Flask, render_template, url_for, flash, redirect, request
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextField, TextAreaField, SelectField
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user, login_required
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_mail import Mail, Message
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ej6swibjsk6920bj14jdzej79hfssr63fgbs'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main_data.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///questions_data.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///courses_data.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///committee_data.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes_data.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///eboard_users.db'
db = SQLAlchemy(app)
main_db = SQLAlchemy(app)
questions_db = SQLAlchemy(app)
courses_db = SQLAlchemy(app)
committee_db = SQLAlchemy(app)
notes_db = SQLAlchemy(app)
eboard_db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USER_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')
mail = Mail(app)


user_list = []

class Course():
    def __init__(self, number, name, credits):
        self.number = number
        self.name = name
        self.credits = credits




@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/prospectinfo/<string:email>", methods = ['GET', 'POST'])
def prospect_info(email):
    #pass
    data_m = MainData.query.filter_by(email = email).first()
    data_q = QuestionsData.query.filter_by(email = email).first()
    data_c = CommitteeData.query.filter_by(email = email).first()
    data_co = CoursesData.query.filter_by(email = email).first()
    form = NotesForm()
    credits = 0
    if ((data_co is not None) and str(data_co.course_1_credits) is not str("")):
        credits = credits + int(data_co.course_1_credits)
    if ((data_co is not None) and str(data_co.course_2_credits) is not str("")):
        credits = credits + int(data_co.course_2_credits)
    if ((data_co is not None) and str(data_co.course_3_credits) is not str("")):
        credits = credits + int(data_co.course_3_credits)
    if ((data_co is not None) and str(data_co.course_4_credits) is not str("")):
        credits = credits + int(data_co.course_4_credits)
    if ((data_co is not None) and str(data_co.course_5_credits) is not str("")):
        credits = credits + int(data_co.course_5_credits)
    if ((data_co is not None) and str(data_co.course_6_credits) is not str("")):
        credits = credits + int(data_co.course_6_credits)
    if ((data_co is not None) and str(data_co.course_7_credits) is not str("")):
        credits = credits + int(data_co.course_7_credits)
    if ((data_co is not None) and str(data_co.course_8_credits) is not str("")):
        credits = credits + int(data_co.course_8_credits)
    if (form.validate_on_submit()):
        NotesData.query.filter_by(email = "{}{}".format(email, current_user.email)).delete()
        notes_data = NotesData(email = "{}{}".format(email, current_user.email), notes = form.notes.data)
        notes_db.session.add(notes_data)
        notes_db.session.commit()
        flash("success", "success")
        return redirect(url_for("prospects"))
    elif request.method == "GET":
        user = NotesData.query.filter_by(email = "{}{}".format(email, current_user.email)).first()
        '''
        if str(current_user.email) == str(user.writer):
            if (user is not None):
                form.notes.data = user.notes
        '''
        if (user is not None):
            form.notes.data = user.notes
    return render_template("prospectinfo.html", data_m = data_m, data_q = data_q, data_c = data_c, data_co = data_co, form = form, credits = credits)

@app.route("/prosinfo/<string:email_string>")
@login_required
def specific_prospects(email_string):
    #user_list = MainData.query.filter_by(email = email_string)
    user_list = MainData.query.filter_by(last_name = email_string)
    return render_template("specprospects.html", users = user_list)

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/d7")
@login_required
def d7():
    user_list = CommitteeData.query.all()
    #output_list = []
    first_list = []
    second_list = []
    third_list = []
    for user in user_list:
        if user.first_choice == str("D7") or user.second_choice == str("D7") or user.third_choice == str("D7"):
            digit = 0
            main_data = MainData.query.filter_by(email=user.email).first()
            committee_data = CommitteeData.query.filter_by(email=user.email).first()
            courses_data = CoursesData.query.filter_by(email=user.email).first()
            questions_data = QuestionsData.query.filter_by(email=user.email).first()
            if (user.first_choice == str("D7")):
                digit = 1
                inserted_user = Filter(user.email, "D7", digit, main_data,committee_data, courses_data, questions_data)
                first_list.append(inserted_user)
            elif (user.second_choice == str("D7")):
                digit = 2
                inserted_user = Filter(user.email, "D7", digit, main_data,committee_data, courses_data, questions_data)
                second_list.append(inserted_user)
            elif (user.third_choice == str("D7")):
                digit = 3
                inserted_user = Filter(user.email, "D7", digit, main_data,committee_data, courses_data, questions_data)
                third_list.append(inserted_user)
    return render_template("d7.html", first_list = first_list, second_list = second_list, third_list = third_list)

@app.route("/fundraising")
@login_required
def fundraising():
    user_list = CommitteeData.query.all()
    # output_list = []
    first_list = []
    second_list = []
    third_list = []
    for user in user_list:
        if user.first_choice == str("Fundraising") or user.second_choice == str("Fundraising") or user.third_choice == str("Fundraising"):
            digit = 0
            main_data = MainData.query.filter_by(email=user.email).first()
            committee_data = CommitteeData.query.filter_by(email=user.email).first()
            courses_data = CoursesData.query.filter_by(email=user.email).first()
            questions_data = QuestionsData.query.filter_by(email=user.email).first()
            if (user.first_choice == str("Fundraising")):
                digit = 1
                inserted_user = Filter(user.email, "Fundraising", digit, main_data, committee_data, courses_data, questions_data)
                first_list.append(inserted_user)
            elif (user.second_choice == str("Fundraising")):
                digit = 2
                inserted_user = Filter(user.email, "Fundraising", digit, main_data, committee_data, courses_data, questions_data)
                second_list.append(inserted_user)
            elif (user.third_choice == str("Fundraising")):
                digit = 3
                inserted_user = Filter(user.email, "Fundraising", digit, main_data, committee_data, courses_data, questions_data)
                third_list.append(inserted_user)
    return render_template("fundraising.html", first_list=first_list, second_list=second_list, third_list=third_list)

@app.route("/events")
@login_required
def events():
    user_list = CommitteeData.query.all()
    # output_list = []
    first_list = []
    second_list = []
    third_list = []
    for user in user_list:
        if user.first_choice == str("Events") or user.second_choice == str(
                "Events") or user.third_choice == str("Events"):
            digit = 0
            main_data = MainData.query.filter_by(email=user.email).first()
            committee_data = CommitteeData.query.filter_by(email=user.email).first()
            courses_data = CoursesData.query.filter_by(email=user.email).first()
            questions_data = QuestionsData.query.filter_by(email=user.email).first()
            if (user.first_choice == str("Events")):
                digit = 1
                inserted_user = Filter(user.email, "Events", digit, main_data, committee_data, courses_data,
                                       questions_data)
                first_list.append(inserted_user)
            elif (user.second_choice == str("Events")):
                digit = 2
                inserted_user = Filter(user.email, "Events", digit, main_data, committee_data, courses_data,
                                       questions_data)
                second_list.append(inserted_user)
            elif (user.third_choice == str("Events")):
                digit = 3
                inserted_user = Filter(user.email, "Events", digit, main_data, committee_data, courses_data,
                                       questions_data)
                third_list.append(inserted_user)
    return render_template("events.html", first_list=first_list, second_list=second_list, third_list=third_list)

@app.route("/web")
@login_required
def web():
    user_list = CommitteeData.query.all()
    # output_list = []
    first_list = []
    second_list = []
    third_list = []
    for user in user_list:
        if user.first_choice == str("Web") or user.second_choice == str(
                "Web") or user.third_choice == str("Web"):
            digit = 0
            main_data = MainData.query.filter_by(email=user.email).first()
            committee_data = CommitteeData.query.filter_by(email=user.email).first()
            courses_data = CoursesData.query.filter_by(email=user.email).first()
            questions_data = QuestionsData.query.filter_by(email=user.email).first()
            if (user.first_choice == str("Web")):
                digit = 1
                inserted_user = Filter(user.email, "Web", digit, main_data, committee_data, courses_data,
                                       questions_data)
                first_list.append(inserted_user)
            elif (user.second_choice == str("Web")):
                digit = 2
                inserted_user = Filter(user.email, "Web", digit, main_data, committee_data, courses_data,
                                       questions_data)
                second_list.append(inserted_user)
            elif (user.third_choice == str("Web")):
                digit = 3
                inserted_user = Filter(user.email, "Web", digit, main_data, committee_data, courses_data,
                                       questions_data)
                third_list.append(inserted_user)
    return render_template("web.html", first_list=first_list, second_list=second_list, third_list=third_list)

@app.route("/culture")
@login_required
def culture():
    user_list = CommitteeData.query.all()
    # output_list = []
    first_list = []
    second_list = []
    third_list = []
    for user in user_list:
        if user.first_choice == str("Culture") or user.second_choice == str(
                "Culture") or user.third_choice == str("Culture"):
            digit = 0
            main_data = MainData.query.filter_by(email=user.email).first()
            committee_data = CommitteeData.query.filter_by(email=user.email).first()
            courses_data = CoursesData.query.filter_by(email=user.email).first()
            questions_data = QuestionsData.query.filter_by(email=user.email).first()
            if (user.first_choice == str("Culture")):
                digit = 1
                inserted_user = Filter(user.email, "Culture", digit, main_data, committee_data, courses_data,
                                       questions_data)
                first_list.append(inserted_user)
            elif (user.second_choice == str("Culture")):
                digit = 2
                inserted_user = Filter(user.email, "Culture", digit, main_data, committee_data, courses_data,
                                       questions_data)
                second_list.append(inserted_user)
            elif (user.third_choice == str("Culture")):
                digit = 3
                inserted_user = Filter(user.email, "Culture", digit, main_data, committee_data, courses_data,
                                       questions_data)
                third_list.append(inserted_user)
    return render_template("culture.html", first_list=first_list, second_list=second_list, third_list=third_list)


@app.route("/hospitality")
@login_required
def hospitality():
    user_list = CommitteeData.query.all()
    # output_list = []
    first_list = []
    second_list = []
    third_list = []
    for user in user_list:
        if user.first_choice == str("Hospitality") or user.second_choice == str(
                "Hospitality") or user.third_choice == str("Hospitality"):
            digit = 0
            main_data = MainData.query.filter_by(email=user.email).first()
            committee_data = CommitteeData.query.filter_by(email=user.email).first()
            courses_data = CoursesData.query.filter_by(email=user.email).first()
            questions_data = QuestionsData.query.filter_by(email=user.email).first()
            if (user.first_choice == str("Hospitality")):
                digit = 1
                inserted_user = Filter(user.email, "Hospitality", digit, main_data, committee_data, courses_data,
                                       questions_data)
                first_list.append(inserted_user)
            elif (user.second_choice == str("Hospitality")):
                digit = 2
                inserted_user = Filter(user.email, "Hospitality", digit, main_data, committee_data, courses_data,
                                       questions_data)
                second_list.append(inserted_user)
            elif (user.third_choice == str("Hospitality")):
                digit = 3
                inserted_user = Filter(user.email, "Hospitality", digit, main_data, committee_data, courses_data,
                                       questions_data)
                third_list.append(inserted_user)
    return render_template("hospitality.html", first_list=first_list, second_list=second_list, third_list=third_list)

@app.route("/service")
@login_required
def service():
    user_list = CommitteeData.query.all()
    # output_list = []
    first_list = []
    second_list = []
    third_list = []
    for user in user_list:
        if user.first_choice == str("Service") or user.second_choice == str(
                "Service") or user.third_choice == str("Service"):
            digit = 0
            main_data = MainData.query.filter_by(email=user.email).first()
            committee_data = CommitteeData.query.filter_by(email=user.email).first()
            courses_data = CoursesData.query.filter_by(email=user.email).first()
            questions_data = QuestionsData.query.filter_by(email=user.email).first()
            if (user.first_choice == str("Service")):
                digit = 1
                inserted_user = Filter(user.email, "Service", digit, main_data, committee_data, courses_data,
                                       questions_data)
                first_list.append(inserted_user)
            elif (user.second_choice == str("Service")):
                digit = 2
                inserted_user = Filter(user.email, "Service", digit, main_data, committee_data, courses_data,
                                       questions_data)
                second_list.append(inserted_user)
            elif (user.third_choice == str("Service")):
                digit = 3
                inserted_user = Filter(user.email, "Service", digit, main_data, committee_data, courses_data,
                                       questions_data)
                third_list.append(inserted_user)
    return render_template("service.html", first_list=first_list, second_list=second_list, third_list=third_list)

@app.route("/promo")
@login_required
def promo():
    user_list = CommitteeData.query.all()
    # output_list = []
    first_list = []
    second_list = []
    third_list = []
    for user in user_list:
        if user.first_choice == str("Promo") or user.second_choice == str(
                "Promo") or user.third_choice == str("Promo"):
            digit = 0
            main_data = MainData.query.filter_by(email=user.email).first()
            committee_data = CommitteeData.query.filter_by(email=user.email).first()
            courses_data = CoursesData.query.filter_by(email=user.email).first()
            questions_data = QuestionsData.query.filter_by(email=user.email).first()
            if (user.first_choice == str("Promo")):
                digit = 1
                inserted_user = Filter(user.email, "Promo", digit, main_data, committee_data, courses_data,
                                       questions_data)
                first_list.append(inserted_user)
            elif (user.second_choice == str("Promo")):
                digit = 2
                inserted_user = Filter(user.email, "Promo", digit, main_data, committee_data, courses_data,
                                       questions_data)
                second_list.append(inserted_user)
            elif (user.third_choice == str("Promo")):
                digit = 3
                inserted_user = Filter(user.email, "Promo", digit, main_data, committee_data, courses_data,
                                       questions_data)
                third_list.append(inserted_user)
    return render_template("promo.html", first_list=first_list, second_list=second_list, third_list=third_list)


@app.route("/sports")
@login_required
def sports():
    user_list = CommitteeData.query.all()
    # output_list = []
    first_list = []
    second_list = []
    third_list = []
    for user in user_list:
        if user.first_choice == str("Service") or user.second_choice == str(
                "Service") or user.third_choice == str("Service"):
            digit = 0
            main_data = MainData.query.filter_by(email=user.email).first()
            committee_data = CommitteeData.query.filter_by(email=user.email).first()
            courses_data = CoursesData.query.filter_by(email=user.email).first()
            questions_data = QuestionsData.query.filter_by(email=user.email).first()
            if (user.first_choice == str("Service")):
                digit = 1
                inserted_user = Filter(user.email, "Service", digit, main_data, committee_data, courses_data,
                                       questions_data)
                first_list.append(inserted_user)
            elif (user.second_choice == str("Service")):
                digit = 2
                inserted_user = Filter(user.email, "Service", digit, main_data, committee_data, courses_data,
                                       questions_data)
                second_list.append(inserted_user)
            elif (user.third_choice == str("Service")):
                digit = 3
                inserted_user = Filter(user.email, "Service", digit, main_data, committee_data, courses_data,
                                       questions_data)
                third_list.append(inserted_user)
    return render_template("sports.html", first_list=first_list, second_list=second_list, third_list=third_list)




class Filter:
    def __init__(self, email, committee, digit, main_data, committee_data, courses_data, questions_data):
        self.email = email
        self.committee = committee
        self.digit = digit
        self.main_data = main_data
        self.committee_data = committee_data
        self.courses_data = courses_data
        self.questions_data = questions_data

@app.route("/cleardata", methods = ['GET', 'POST'])
@login_required
def delete():
    form = DeleteForm()
    if (form.validate_on_submit and "20202021" == str(form.password.data)):
        db.drop_all()
        db.create_all()
        main_db.drop_all()
        main_db.create_all()
        questions_db.drop_all()
        questions_db.create_all()
        courses_db.drop_all()
        courses_db.create_all()
        committee_db.drop_all()
        committee_db.create_all()
        notes_db.drop_all()
        notes_db.create_all()
        eboard_db.drop_all()
        eboard_db.create_all()
        return redirect(url_for("login"))
    return render_template("delete.html", form = form)

@app.route("/prospects", methods = ['GET', 'POST'])
@login_required
def prospects():
    user_list = MainData.query.all()
    form = SearchForm()
    if form.validate_on_submit():
        email_string = form.entry.data
        return redirect(url_for('specific_prospects', email_string = email_string))
    return render_template("prospects.html", user_list = user_list, form = form)

@app.route("/")
@app.route("/home")
def hello():
    return render_template('home.html', title = "home")

@app.route("/about")
def about():
    return render_template('about.html', title = "about")

@app.route("/registration", methods = ['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        input_user = User(first_name = form.first_name.data, last_name = form.last_name.data, email = form.email.data, username = form.username.data, password = hashed)
        db.session.add(input_user)
        db.session.commit()
        user_list.append(input_user)
        flash("Account Created for {}".format(form.username.data), 'success')
        return redirect(url_for('login'))
    else:
        return render_template('registration.html', title = "Register", form = form)

@app.route("/eboardregistration", methods = ['GET', 'POST'])
def eboard_register():
    form = RegistrationForm()
    if (form.validate_on_submit()):
        hashed = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        input_user = User(first_name = form.first_name.data, last_name = form.last_name.data, email = form.email.data, username = form.username.data, password = hashed)
        db.session.add(input_user)
        db.session.commit()
        flash("Account Created for {}".format(form.username.data), 'success')
        return redirect(url_for("eboard_login"))
    return render_template("eboardregistration.html", title = "Executive Board Registration", form = form)

@app.route("/eboardlogin", methods = ['GET', 'POST'])
def eboard_login():
    if current_user.is_authenticated:
        return redirect(url_for("prospects"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if (user and bcrypt.check_password_hash(user.password, form.password.data)):
            login_user(user, remember = form.remember.data)
            flash("Login Successful for Executive Board Member", category = "success")
            return redirect(url_for('prospects'))
        else:
            flash("Login Unsuccessful. Check Password or Email", category = "danger")
            return redirect(url_for("eboard_login"))
    else:
        return render_template("eboardlogin.html", title = "Executive Board Login", form = form)


@app.route("/login", methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('hello'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if (("fasa_eboard@vt.edu" == str(form.email.data)) and ("20202021" == str(form.password.data))):
            flash("Confirmed Executive Board Member", "success")
            return redirect(url_for("eboard_register"))
        if (user and bcrypt.check_password_hash(user.password, form.password.data)):
            login_user(user, remember = form.remember.data)
            flash('Login Successful', category = "success")
            return redirect(url_for('hello'))
        else:
            flash('Login Unsuccessful', category = "danger")
            return redirect(url_for('login'))
    else:
        return render_template('login2.html', title = "Login", form = form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Successfully logged out", "success")
    return redirect(url_for('hello'))

@app.route("/account")
@login_required
def account():
    main_user = MainData.query.filter_by(email = current_user.email).first()
    questions_user = QuestionsData.query.filter_by(email = current_user.email).first()
    courses_user = CoursesData.query.filter_by(email = current_user.email).first()
    committees_user = CommitteeData.query.filter_by(email = current_user.email).first()
    #credits = int(courses_user.course_1_credits + courses_user.course_2_credits + courses_user.course_3_credits + courses_user.course_4_credits + courses_user.course_5_credits + courses_user.course_6_credits + courses_user.course_7_credits + courses_user.course_8_credits)
    #credits = int(courses_user.course_1_credits) + int(courses_user.course_2_credits) + int(courses_user.course_3_credits) + int(courses_user.course_4_credits) + int(courses_user.course_5_credits) + int(courses_user.course_6_credits) + int(courses_user.course_7_credits) + int(courses_user.course_8_credits)
    credits = 0
    if ((courses_user is not None) and str(courses_user.course_1_credits) is not str("")):
        credits = credits + int(courses_user.course_1_credits)
    if ((courses_user is not None) and str(courses_user.course_2_credits) is not str("")):
        credits = credits + int(courses_user.course_2_credits)
    if ((courses_user is not None) and str(courses_user.course_3_credits) is not str("")):
        credits = credits + int(courses_user.course_3_credits)
    if ((courses_user is not None) and str(courses_user.course_4_credits) is not str("")):
        credits = credits + int(courses_user.course_4_credits)
    if ((courses_user is not None) and str(courses_user.course_5_credits) is not str("")):
        credits = credits + int(courses_user.course_5_credits)
    if ((courses_user is not None) and str(courses_user.course_6_credits) is not str("")):
        credits = credits + int(courses_user.course_6_credits)
    if ((courses_user is not None) and str(courses_user.course_7_credits) is not str("")):
        credits = credits + int(courses_user.course_7_credits)
    if ((courses_user is not None) and str(courses_user.course_8_credits) is not str("")):
        credits = credits + int(courses_user.course_8_credits)
    return render_template("account.html", main_user = main_user, questions_user = questions_user,
                           courses_user = courses_user, committees_user = committees_user, credits = credits)

@app.route("/apply", methods = ['GET', 'POST'])
@login_required
def apply():
    form = MainForm()
    if form.validate_on_submit():
        MainData.query.filter_by(email = current_user.email).delete()
        data_main = MainData(first_name = form.first_name.data, last_name = form.last_name.data, username = form.username.data,
                             email = form.email.data, address = form.address.data, major = form.major.data,
                             year = form.year.data, phone_number = form.phone_number.data)
        main_db.session.add(data_main)
        main_db.session.commit()
        flash("Success", "success")
        return redirect(url_for('hello'))
    elif request.method == "GET":
        user = MainData.query.filter_by(email = current_user.email).first()
        if (user is not None):
            form.first_name.data = user.first_name
            form.last_name.data = user.last_name
            form.username.data = user.username
            form.email.data = user.email
            form.address.data = user.address
            form.major.data = user.major
            form.year.data = user.year
            form.phone_number.data = user.phone_number
    return render_template("apply.html", main_form = form)

@app.route("/questions", methods = ['GET', 'POST'])
@login_required
def questions():
    form = QuestionForm()
    if form.validate_on_submit():
        QuestionsData.query.filter_by(email = current_user.email).delete()
        data_question = QuestionsData(email = current_user.email, question_1 = form.question_1.data,
                                 question_2 = form.question_2.data, question_3 = form.question_3.data,
                                 question_4 = form.question_4.data)
        questions_db.session.add(data_question)
        questions_db.session.commit()
        flash("Success", "success")
        return redirect(url_for('hello'))

    elif request.method == 'GET':
        user = QuestionsData.query.filter_by(email = current_user.email).first()
        if (user is not None):
            form.question_1.data = user.question_1
            form.question_2.data = user.question_2
            form.question_3.data = user.question_3
            form.question_4.data = user.question_4
    return render_template("questions.html", form = form)

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender = 'noreply@demo.com', recipients = [user.email])
    msg.body = '''To reset your password, visit the following link:
        {} If you did not make this request, ignore this email and 
        no changes will be made'''.format(url_for('reset_token', token = token), _external = True)
    mail.send(msg)


@app.route("/reset_password", methods = ['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for("hello"))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        send_reset_email(user)
        flash("An email has been sent with instructions to reset your password", "info")
        return redirect(url_for("login"))
    return render_template("reset_request.html", title = "Reset Password", form = form)

@app.route("/reset_password/<token>", methods = ['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for("hello"))
    user = User.verify_reset_token(token)
    if user is None:
        flash("Invalid or Expired token", "warning")
        return redirect(url_for("reset_request"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        # flash("Account Created for {}".format(form.username.data), 'success')
        flash("success", "success")
        return redirect(url_for('login'))

    return render_template("reset_token.html", title = "Reset Password", form = form)

@app.route("/courses", methods = ['GET', 'POST'])
@login_required
def courses():
    form = CourseForm()
    if form.validate_on_submit():
        CoursesData.query.filter_by(email = current_user.email).delete()

        data_courses = CoursesData(email = current_user.email, course_1_number = form.course_1_number.data, course_1_name = form.course_1_name.data, course_1_credits = form.course_1_credits.data,
                                   course_2_number = form.course_2_number.data, course_2_name = form.course_2_name.data, course_2_credits = form.course_2_credits.data,
                                   course_3_number = form.course_3_number.data, course_3_name = form.course_3_name.data, course_3_credits = form.course_3_credits.data,
                                   course_4_number = form.course_4_number.data, course_4_name = form.course_4_name.data, course_4_credits = form.course_4_credits.data,
                                   course_5_number = form.course_5_number.data, course_5_name = form.course_5_name.data, course_5_credits = form.course_5_credits.data,
                                   course_6_number = form.course_6_number.data, course_6_name = form.course_6_name.data, course_6_credits = form.course_6_credits.data,
                                   course_7_number = form.course_7_number.data, course_7_name = form.course_7_name.data, course_7_credits = form.course_7_credits.data,
                                   course_8_number = form.course_8_number.data, course_8_name = form.course_8_name.data, course_8_credits = form.course_8_credits.data)
        courses_db.session.add(data_courses)
        courses_db.session.commit()
        flash("Success", "success")
        return redirect(url_for("courses"))
    elif request.method == "GET":
        user = CoursesData.query.filter_by(email = current_user.email).first()

        if (user is not None):
            form.course_1_number.data = user.course_1_number
            form.course_1_name.data = user.course_1_name
            form.course_1_credits.data = user.course_1_credits

            form.course_2_number.data = user.course_2_number
            form.course_2_name.data = user.course_2_name
            form.course_2_credits.data = user.course_2_credits

            form.course_3_number.data = user.course_3_number
            form.course_3_name.data = user.course_3_name
            form.course_3_credits.data = user.course_3_credits

            form.course_4_number.data = user.course_4_number
            form.course_4_name.data = user.course_4_name
            form.course_4_credits.data = user.course_4_credits

            form.course_5_number.data = user.course_5_number
            form.course_5_name.data = user.course_5_name
            form.course_5_credits.data = user.course_5_credits

            form.course_6_number.data = user.course_6_number
            form.course_6_name.data = user.course_6_name
            form.course_6_credits.data = user.course_6_credits

            form.course_7_number.data = user.course_7_number
            form.course_7_name.data = user.course_7_name
            form.course_7_credits.data = user.course_7_credits

            form.course_8_number.data = user.course_8_number
            form.course_8_name.data = user.course_8_name
            form.course_8_credits.data = user.course_8_credits

    return render_template("courses.html", form = form)

@app.route("/committees", methods = ['GET', 'POST'])
@login_required
def committees():
    form = CommitteesForm()
    if form.validate_on_submit():
        CommitteeData.query.filter_by(email = current_user.email).delete()
        data_committee = CommitteeData(email = current_user.email, first_choice = form.first_choice.data, second_choice = form.second_choice.data, third_choice = form.third_choice.data)
        committee_db.session.add(data_committee)
        committee_db.session.commit()
        flash("Success", "success")
        return redirect(url_for("hello"))
    elif request.method == "GET":
        user = CommitteeData.query.filter_by(email = current_user.email).first()
        if (user is not None):
            form.first_choice.data = user.first_choice
            form.second_choice.data = user.second_choice
            form.third_choice.data = user.third_choice
    return render_template("committees.html", form = form)

class RegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators = [DataRequired(), Length(min = 2, max = 30)])
    last_name = StringField('Last Name', validators = [DataRequired(), Length(min = 2, max = 30)])
    username = StringField('Username', validators = [DataRequired(), Length(min = 2, max = 30)])
    email = StringField('Email', validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators = [DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators = [DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        email_string = User.query.filter_by(email = email.data).first()
        if email_string:
            raise ValidationError('That email is taken. Please choose a different one.')



class NotesForm(FlaskForm):
    notes = TextAreaField("Notes", render_kw={"rows": 5, "cols": 0})
    submit = SubmitField("Save")

class DeleteForm(FlaskForm):
    password = PasswordField("Enter Eboard Password", validators = [DataRequired()])
    delete = SubmitField("Delete")

class LoginForm(FlaskForm):
    email = StringField('Email', validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators = [DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class RequestResetForm(FlaskForm):
    email = StringField('Email', validators = [DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        email_string = User.query.filter_by(email = email.data).first()
        if email_string is None:
            raise ValidationError('There is no account with that email. You must register first')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')


class MainForm(FlaskForm):
    first_name = StringField('First Name', validators = [DataRequired(), Length(min = 2, max = 30)])
    last_name = StringField('Last Name', validators = [DataRequired(), Length(min = 2, max = 30)])
    username = StringField('Username', validators = [DataRequired(), Length(min = 2, max = 60)])
    email = StringField('Email', validators = [DataRequired(), Email()])
    address = StringField('Address', validators = [DataRequired(), Length(min = 2, max = 200)])
    major = StringField('Major', validators = [DataRequired(), Length(min = 2, max = 100)])
    year = StringField('Year', validators = [DataRequired(), Length(min = 0, max = 10)])
    phone_number = StringField('Phone Number', validators = [DataRequired(), Length(min = 2, max = 15)])
    submit = SubmitField('Submit')



class QuestionForm(FlaskForm):
    question_1 = TextAreaField('Question 1', validators = [Length(min = 2, max = 1000)], render_kw={"rows": 5, "cols": 0})
    question_2 = TextAreaField('Question 2', validators = [Length(min = 2, max = 1000)], render_kw={"rows": 5, "cols": 0})
    question_3 = TextAreaField('Question 3', validators = [Length(min = 2, max = 1000)], render_kw={"rows": 5, "cols": 0})
    question_4 = TextAreaField('Question 4', validators = [Length(min = 2, max = 1000)], render_kw={"rows": 5, "cols": 0})
    submit = SubmitField('Submit')

class SearchForm(FlaskForm):
    entry = StringField('Enter Last Name', validators = [DataRequired()])
    submit = SubmitField("Find")

class CommitteesForm(FlaskForm):
    first_choice = SelectField('First Choice', choices = [("First Choice", "First Choice"), ("Fundraising", "Fundraising"), ("Hospitality", "Hospitality"), ("D7", "D7"), ("Promo", "Promo"), ("Events", "Events"), ("Web", "Web"), ("Service", "Service"), ("Culture", "Culture"), ("Sports", "Sports"), ("None", "None")])
    second_choice = SelectField('Second Choice', choices = [("Second Choice", "Second Choice"), ("Fundraising", "Fundraising"), ("Hospitality", "Hospitality"), ("D7", "D7"), ("Promo", "Promo"), ("Events", "Events"), ("Web", "Web"), ("Service", "Service"), ("Culture", "Culture"), ("Sports", "Sports"), ("None", "None")])
    third_choice = SelectField('Third Choice', choices = [("Third Choice", "Third Choice"), ("Fundraising", "Fundraising"), ("Hospitality", "Hospitality"), ("D7", "D7"), ("Promo", "Promo"), ("Events", "Events"), ("Web", "Web"), ("Service", "Service"), ("Culture", "Culture"), ("Sports", "Sports"), ("None", "None")])
    submit = SubmitField('Submit')

class CourseForm(FlaskForm):
    course_1_number = StringField("Course Number", validators = [Length(min = 0, max = 10)])
    course_1_name = StringField("Course Name", validators = [Length(min = 0, max = 100)])
    course_1_credits = StringField("Course Credits", validators = [Length(min = 0, max = 5)])

    course_2_number = StringField("Course Number", validators=[Length(min=0, max=10)])
    course_2_name = StringField("Course Name", validators=[Length(min=0, max=100)])
    course_2_credits = StringField("Course Credits", validators=[Length(min=0, max=5)])

    course_3_number = StringField("Course Number", validators=[Length(min=0, max=10)])
    course_3_name = StringField("Course Name", validators=[Length(min=0, max=100)])
    course_3_credits = StringField("Course Credits", validators=[Length(min=0, max=5)])

    course_4_number = StringField("Course Number", validators=[Length(min=0, max=10)])
    course_4_name = StringField("Course Name", validators=[Length(min=0, max=100)])
    course_4_credits = StringField("Course Credits", validators=[Length(min=0, max=5)])

    course_5_number = StringField("Course Number", validators=[Length(min=0, max=10)])
    course_5_name = StringField("Course Name", validators=[Length(min=0, max=100)])
    course_5_credits = StringField("Course Credits", validators=[Length(min=0, max=5)])

    course_6_number = StringField("Course Number", validators=[Length(min=0, max=10)])
    course_6_name = StringField("Course Name", validators=[Length(min=0, max=100)])
    course_6_credits = StringField("Course Credits", validators=[Length(min=0, max=5)])

    course_7_number = StringField("Course Number", validators=[Length(min=0, max=10)])
    course_7_name = StringField("Course Name", validators=[Length(min=0, max=100)])
    course_7_credits = StringField("Course Credits", validators=[Length(min=0, max=5)])

    course_8_number = StringField("Course Number", validators=[Length(min=0, max=10)])
    course_8_name = StringField("Course Name", validators=[Length(min=0, max=100)])
    course_8_credits = StringField("Course Credits", validators=[Length(min=0, max=5)])

    submit = SubmitField("Submit")


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(30), unique = False, nullable = False)
    last_name = db.Column(db.String(30), unique = False, nullable = False)
    username = db.Column(db.String(20), unique = True, nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    password = db.Column(db.String(60), nullable = False)

    def __repr__(self):
        return "User({}, {}, {}, {})".format(self.first_name, self.last_name, self.username, self.email)

    '''new'''
    def get_reset_token(self, expires_sec = 3600):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

class EboardUser(eboard_db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(30), unique = False, nullable = False)
    last_name = db.Column(db.String(30), unique = False, nullable = False)
    username = db.Column(db.String(20), unique = True, nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    password = db.Column(db.String(60), nullable = False)

    def __repr__(self):
        return "User({}, {}, {}, {})".format(self.first_name, self.last_name, self.username, self.email)

    '''new'''
    def get_reset_token(self, expires_sec = 3600):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return EboardUser.query.get(user_id)


class MainData(main_db.Model):
    id = main_db.Column(main_db.Integer, primary_key = True)
    first_name = main_db.Column(main_db.String(30), unique = False, nullable = False)
    last_name = main_db.Column(main_db.String(30), unique = False, nullable = False)
    username = main_db.Column(main_db.String(30), unique = False, nullable = False)
    email = main_db.Column(main_db.String(120), unique = True, nullable = False)
    address = main_db.Column(main_db.String(200), unique = False, nullable = False)
    major = main_db.Column(main_db.String(100), unique = False, nullable = False)
    year = main_db.Column(main_db.String(30), unique = False, nullable = False)
    phone_number = main_db.Column(db.String(20), unique = False, nullable = False)

    def __repr__(self):
        return "Main({}, {}, {})".format(self.email, self.first_name, self.last_name)


class QuestionsData(questions_db.Model):
    id = questions_db.Column(questions_db.Integer, primary_key = True)
    email = questions_db.Column(questions_db.String(100), nullable = False, unique = True)
    question_1 = questions_db.Column(questions_db.String(1000), nullable = True, unique = False)
    question_2 = questions_db.Column(questions_db.String(1000), nullable = True, unique = False)
    question_3 = questions_db.Column(questions_db.String(1000), nullable = True, unique = False)
    question_4 = questions_db.Column(questions_db.String(1000), nullable = True, unique = False)

    def __repr__(self):
        return "Question({}, {}, {})".format(self.id, self.email, self.question_1)

class CommitteeData(committee_db.Model):
    id = committee_db.Column(committee_db.Integer, primary_key = True)
    email = committee_db.Column(committee_db.String(100), nullable = False, unique = True)
    first_choice = committee_db.Column(committee_db.String(100))
    second_choice = committee_db.Column(committee_db.String(100))
    third_choice = committee_db.Column(committee_db.String(100))

    def __repr__(self):
        return "Committee User({} {} {} {})".format(self.email, self.first_choice, self.second_choice, self.third_choice)

class NotesData(notes_db.Model):
    id = notes_db.Column(notes_db.Integer, primary_key = True)
  #  writer = notes_db.Column(notes_db.String(100))
    email = notes_db.Column(notes_db.String(100))
    notes = notes_db.Column(notes_db.String(2000))


class CoursesData(courses_db.Model):
    id = courses_db.Column(courses_db.Integer, primary_key = True)
    email = courses_db.Column(courses_db.String(100), nullable = False, unique = True)
    course_1_number = courses_db.Column(courses_db.String(100), nullable = True, unique = False)
    course_1_name = courses_db.Column(courses_db.String(100), nullable = True, unique = False)
    course_1_credits = courses_db.Column(courses_db.String(100), nullable = True, unique = False)

    course_2_number = courses_db.Column(courses_db.String(100), nullable=True, unique=False)
    course_2_name = courses_db.Column(courses_db.String(100), nullable=True, unique=False)
    course_2_credits = courses_db.Column(courses_db.String(100), nullable=True, unique=False)

    course_3_number = courses_db.Column(courses_db.String(100), nullable=True, unique=False)
    course_3_name = courses_db.Column(courses_db.String(100), nullable=True, unique=False)
    course_3_credits = courses_db.Column(courses_db.String(100), nullable=True, unique=False)

    course_4_number = courses_db.Column(courses_db.String(100), nullable=True, unique=False)
    course_4_name = courses_db.Column(courses_db.String(100), nullable=True, unique=False)
    course_4_credits = courses_db.Column(courses_db.String(100), nullable=True, unique=False)

    course_5_number = courses_db.Column(courses_db.String(100), nullable=True, unique=False)
    course_5_name = courses_db.Column(courses_db.String(100), nullable=True, unique=False)
    course_5_credits = courses_db.Column(courses_db.String(100), nullable=True, unique=False)

    course_6_number = courses_db.Column(courses_db.String(100), nullable=True, unique=False)
    course_6_name = courses_db.Column(courses_db.String(100), nullable=True, unique=False)
    course_6_credits = courses_db.Column(courses_db.String(100), nullable=True, unique=False)

    course_7_number = courses_db.Column(courses_db.String(100), nullable=True, unique=False)
    course_7_name = courses_db.Column(courses_db.String(100), nullable=True, unique=False)
    course_7_credits = courses_db.Column(courses_db.String(100), nullable=True, unique=False)

    course_8_number = courses_db.Column(courses_db.String(100), nullable=True, unique=False)
    course_8_name = courses_db.Column(courses_db.String(100), nullable=True, unique=False)
    course_8_credits = courses_db.Column(courses_db.String(100), nullable=True, unique=False)

    def __repr__(self):
        return "Course User({}, {}, {})".format(self.id, self.email, self.course_1_number)









if __name__ == '__main__':
    app.run(debug = True)

