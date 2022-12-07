from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, flash, abort, session
from flaskext.mysql import MySQL
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_user, logout_user,login_required

# third part
from flask_moment import Moment

from config import config

# models
from models.ModelUser import ModelUser
from models.ModelPerson import ModelPerson

# entities
from models.entities.User import User

app=Flask(__name__)

csrf=CSRFProtect()
db=MySQL()
db.init_app(app)
login_manager_app=LoginManager(app)
moment = Moment(app)

@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(db, id)

#--------- CHECK ROLES ---------#
def check_role(roles):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for role in roles:
                is_role = ModelUser.get_by_role(db,role, session.get('username'))
                if is_role != None:
                    is_user_id= session.get('username')
                    if is_user_id == is_role.username:
                        is_user = ModelUser.get_by_id(db, is_role.id)
                        if is_user != None:
                            return func(*args, **kwargs)
            abort(403)
        return wrapper
    return decorator


@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method=='POST':
        # print(request.form['username'])
        # print(request.form['password'])
        user = User(0,request.form['username'],request.form['password'])
        logged_user=ModelUser.login(db, user)
        logged_user_rol_id=ModelUser.get__by_role_id(db, user.username)
        print(logged_user_rol_id)
        if logged_user != None:
            if logged_user.password:
                session['username']=logged_user.username
                login_user(logged_user)
                match logged_user_rol_id:
                    case '1':
                        return redirect(url_for('user_admin'))
                    case '2':
                        return redirect(url_for('user_aux'))
                    case '3':
                        return redirect(url_for('user_users'))
            else:
                flash("Invalid password")
                return render_template('auth/login.html')
        else:
            flash("User not found...")
            return render_template('auth/login.html')
    else:    
        return render_template('auth/login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/admin')
@login_required
@check_role(['admin'])
def user_admin():
    return render_template('user_admin/index.html')

@app.route('/aux')
@login_required
@check_role(['aux'])
def user_aux():
    return render_template('user_aux/index.html')

@app.route('/users')
@login_required
@check_role(['user'])
def user_users():
    return render_template('user_users/index.html')

@app.route('/admin/users')
@login_required
@check_role(['admin'])
def users_form():
    allUsers=ModelUser.get__all(db)
    return render_template('user_admin/users.html', allUsers=allUsers)

@app.route('/admin/users/save', methods=['POST'])
def save_users():
    _username = request.form['txtUsername']
    _password = request.form['txtPassword']
    _fullname = request.form['txtFullname']
    _rol = request.form['txtRol']
    ModelUser.set_user(db,_username,_password,_fullname,_rol)
    return redirect(url_for('users_form'))
    
@app.route('/admin/users/delete/<id>', methods=['GET','POST'])
def delete_users(id):
    ModelUser.delete_user(db, id)
    return redirect(url_for('users_form'))

@app.route('/admin/careers')
@login_required
@check_role(['admin'])
def careers_form():
    return render_template('user_admin/careers.html')

@app.route('/admin/signatures')
@login_required
@check_role(['admin'])
def signatures_form():
    return render_template('user_admin/signatures.html')

@app.route('/admin/teachers')
@login_required
@check_role(['admin'])
def teachers_form():
    allPersons=ModelPerson.get_all(db)
    return render_template('user_admin/teachers.html',allPersons=allPersons )

@app.route('/admin/teachers/<id>', methods=['GET'])
@login_required
@check_role(['admin'])
def get_teacher_by_id(id):
    person=ModelPerson.get_by_id(db, id)
    return render_template('user_admin/teachers.html',person=person )

@app.route('/admin/teachers/save', methods=['POST'])
def save_teachers():
    _fullname = request.form['txtFullname']
    _dni = request.form['txtDU']
    _address = request.form['txtAddress']
    _city = request.form['txtCity']
    _birth_date = request.form['txtBirthDate']
    _phone_number = request.form['txtPhoneNumber']
    _email = request.form['txtEmail']
    _created_at = request.form['txtCreatedAt']
    _role = request.form['txtRole']
    _active = request.form['txtActive']
    ModelPerson.set_teacher(db, _fullname,_address,_city,_birth_date, _dni,_phone_number,_email,_created_at,_role,_active)
    return redirect(url_for('teachers_form'))

@app.route('/admin/teachers/edit', methods=['POST'])
def edit_teachers():
    _id = request.form['txtId']
    if request.form.get('chkAddress') !='yes': None 
    else: 
        _val = request.form['txtAddress']
        datos=(_val,int(_id))
        pos = 1
        ModelPerson.edit_teacher(db,datos, pos)
    if request.form.get('chkCity') !='yes': None
    else: 
        _val = request.form['txtCity']
        datos=(_val,int(_id))
        pos = 2
        ModelPerson.edit_teacher(db,datos, pos)
    if request.form.get('chkPhoneNumber') !='yes': None 
    else: 
        _val = request.form['txtPhoneNumber']
        datos=(_val,int(_id))
        pos = 3
        ModelPerson.edit_teacher(db,datos, pos)
    if request.form.get('chkEmail') !='yes': None
    else: 
        _val = request.form['txtEmail']
        datos=(_val,int(_id))
        pos = 4
        ModelPerson.edit_teacher(db,datos, pos)
    if request.form.get('chkActive') !='yes': None
    else: 
        _val = request.form['txtActive']
        datos=(_val,int(_id))
        pos = 5
        ModelPerson.edit_teacher(db, datos, pos)
    return redirect(url_for('teachers_form'))

@app.route('/admin/teachers/delete/<id>', methods=['GET','POST'])
def delete_teachers(id):
    ModelPerson.delete_teacher(db, id)
    return redirect(url_for('teachers_form'))

def status_401(error):
    return redirect(url_for('login'))

def status_404(error):
    return '<h1>Pagina no encontrada</h1>', 404

if __name__=='__main__':
    app.config.from_object(config['development'])
    csrf.init_app(app)
    app.register_error_handler(401,status_401)
    app.register_error_handler(404,status_404)
    app.run()