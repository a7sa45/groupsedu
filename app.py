#from crypt import methods
import email
from email.policy import default
import numbers
from tokenize import group
from flask import Flask, flash, render_template, request, redirect, url_for, Response
from werkzeug.exceptions import HTTPException
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
#from flask_admin import Admin, AdminIndexView
#from flask_admin.contrib.sqla import ModelView
from webargs import flaskparser, fields
from webargs.flaskparser import use_args, use_kwargs, parser, abort
import gladiator as gl
from flask_basicauth import BasicAuth
from datetime import datetime
from os import environ
import os



app = Flask(__name__)
#dir = os.path.dirname(os.path.abspath(__file__))
#database_file = "sqlite:///{}".format(os.path.join(dir, "groupsedu.db"))
#app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/flask'
app.config["SECRET_KEY"] = 'secret'
db = SQLAlchemy(app)



app.config['BASIC_AUTH_USERNAME'] = 'a7sa45'
app.config['BASIC_AUTH_PASSWORD'] = 'Groups://a7sa45.com'
basic_auth = BasicAuth(app)
app.config['ADMIN_CREDENTIALS'] = ('a7sa45', 'Groups://a7sa45.com')

#MySQL
#app.config['MYSQL_HOST'] = 'localhost'
#app.config['MYSQL_USER'] = 'root'
#app.config['MYSQL_PASSWORD'] = ''
#app.config['MYSQL_DB'] = 'flask'
#mysql = MySQL(app)

#Model
class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.Text, nullable=False)
    universityid = db.Column(db.Text, nullable = False)
    subject = db.Column(db.Text, nullable = False)
    code = db.Column(db.Text, nullable = False)
    university = db.Column(db.Text, nullable = False)
    section = db.Column(db.Text, nullable = False)
    url = db.Column(db.Text, nullable = False)
    created_at = db.Column(db.DateTime, default=datetime.now())



#admin page
#admin = Admin(app)
#admin.add_view(ModelView(Group, db.session))


#CRUD Achins
def create_group(email, universityid, subject, code, university, section, url):
    group = Group(email=email, universityid=universityid, subject=subject, code=code, university=university, section=section, url=url)
    db.session.add(group)
    db.session.commit()
    db.session.refresh(group)

def update_group(group_id, email, universityid, subject, code, university, section, url):
    #group = Group(email=email, universityid=universityid, subject=subject, code=code, university=university, section=section, url=url)
    db.session.query(Group).filter_by(id=group_id).update({
        "email": email,
        "universityid": universityid,
        "subject": subject,
        "code": code,
        "university": university,
        "section": section,
        "url": url
    })
    db.session.commit()

def read():
    return db.session.query(Group).all()

def delete_group(group_id):
    db.session.query(Group).filter_by(id=group_id).delete()
    db.session.commit()


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html")


# assigning validations
field_validations = (
    ('email', gl.required, gl.format_email),
    ('universityid', gl.required),
    ('subject', gl.required),
    ('code', gl.required),
    ('university', gl.required),
    ('section', gl.required),
    ('url', gl.required),
)




@app.route('/')
def index():
    return render_template('home.html', groups = read())

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/myadmin')
@basic_auth.required
def myadmin():
    return render_template('myadmin.html', groups = read())

@app.route('/add')
def add():
    return render_template('add.html')

@app.route('/add', methods=["POST", "GET"])
def adds():
    if request.method == "POST":
        # input test data
        valid_data = {
            'email': request.form['email'],
            'universityid': request.form['universityid'],
            'subject': request.form['subject'],
            'code': request.form['code'],
            'university': request.form['university'],
            'section': request.form['section'],
            'url': request.form['url']
        }
        result = gl.validate(field_validations, valid_data)
        print("Is data valid ? : " + str(bool(result)))
        print(result)
        if result:
            create_group(request.form['email'], request.form['universityid'], request.form['subject'], request.form['code'], request.form['university'], request.form['section'], request.form['url'])
            flash('تم اضافة القروب')
        else:
            return redirect(url_for('add'))
            
        
    return redirect(url_for('index'))

@app.route('/delete/<group_id>', methods=["POST", "GET"])
@basic_auth.required
def delete(group_id):
    delete_group(group_id)
    return redirect(url_for('myadmin'))

@app.route('/edit/<group_id>', methods=["POST", "GET"])
@basic_auth.required
def edit(group_id):
    group = db.session.query(Group).filter_by(id=group_id).one()
    db.session.commit()
    return render_template('edit.html', group = group)

@app.route('/update', methods=["POST", "GET"])
@basic_auth.required
def update():
    if request.method == "POST":
        update_group(request.form['group_id'], request.form['email'], request.form['universityid'], request.form['subject'], request.form['code'], request.form['university'], request.form['section'], request.form['url'])
    return redirect(url_for('myadmin'))







if __name__ == '__main__':
    db.create_all()
    app.run(debug =True)