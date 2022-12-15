from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, flash, abort, session, send_from_directory
from flaskext.mysql import MySQL
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_user, logout_user,login_required
import os


# third part
from flask_moment import Moment

from config import config

# models
from models.ModelUser import ModelUser
from models.ModelPerson import ModelPerson
from models.ModelCareer import ModelCareer
from models.ModelSignature import ModelSignature
from models.ModelStudent import ModelStudent
from models.ModelCourse import ModelCourse

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
            abort(403, 'No tienes permiso para estar aquí! Es solo para administradores')
        return wrapper
    return decorator


@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method=='POST':
        user = User(0,request.form['username'].strip(),request.form['password'])
        logged_user=ModelUser.login(db, user)
        logged_user_rol_id=ModelUser.get_by_role_id(db, user.username)
        if logged_user != None:
            if logged_user.password:
                session['username']=logged_user.username
                session['code']= logged_user.code
                login_user(logged_user)
                match logged_user_rol_id:
                    case '1':
                        return redirect(url_for('user_admin'))
                    case '2':
                        return redirect(url_for('user_aux'))
                    case '3':
                        return redirect(url_for('user_user'))
            else:
                flash("Usuario o Contraseña invalidos")
                return render_template('auth/login.html')
        else:
            flash("Usuario o Contraseña invalidos")
            return render_template('auth/login.html')
    else:    
        return render_template('auth/login.html')

@app.route('/logout')
def logout():
    logout_user()
    session.pop('username', None)
    session.pop('code', None)
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


@app.route('/admin/users')
@login_required
@check_role(['admin'])
def users_form():
    allUsers=ModelUser.get_all(db)
    return render_template('user_admin/users.html', allUsers=allUsers)

@app.route('/admin/users/save', methods=['POST'])
def save_users():
    _username = request.form['txtUsername']
    _password = request.form['txtPassword']
    _fullname = request.form['txtFullname']
    _rol = request.form['txtRol']
    _code = request.form['txtCode']
    ModelUser.create(db,_username,_password,_fullname,_rol, _code)
    return redirect(url_for('users_form'))

@app.route('/admin/users/edit', methods=['POST'])
def edit_users():
    _id = request.form['txtId']
    _pass1 = request.form['txtPass1']
    _pass2 = request.form['txtPass2']
    if _pass1 == _pass2:
        ModelUser.edit(db,_pass1, _id)
        return redirect(url_for('users_form'))
    else:
        flash("No se pudo cambiar la contraseña")
        return redirect(url_for('users_form'))
    
@app.route('/admin/users/delete/<id>', methods=['GET','POST'])
def delete_users(id):
    ModelUser.delete(db, id)
    return redirect(url_for('users_form'))

@app.route('/admin/careers')
@login_required
@check_role(['admin','aux'])
def careers_form():
    allCareers=ModelCareer.get_all(db)
    max_code_temp = 0
    for career in allCareers:
        if career[2] > max_code_temp:
            max_code_temp = career[2]
    max_code = max_code_temp + 100
    return render_template('user_admin/careers.html', allCareers=allCareers, max_code=max_code)

@app.route('/admin/careers/save', methods=['POST'])
@login_required
@check_role(['admin','aux'])
def save_careers():
    _name = request.form['txtName']
    _code = request.form['txtCode']
    _created_at = request.form['txtCreatedAt']
    _active = request.form['txtActive']
    ModelCareer.create(db, _name,_code,_created_at,_active)
    return redirect(url_for('careers_form'))

@app.route('/admin/careers/edit', methods=['POST'])
@login_required
@check_role(['admin','aux'])
def edit_careers():
    _id = request.form['txtId']
    if request.form.get('chkName') !='yes': None 
    else: 
        _val = request.form['txtName']
        datos=(_val,int(_id))
        pos = 1
        ModelCareer.edit(db,datos, pos)
    if request.form.get('chkActive') !='yes': None
    else: 
        _val = request.form['txtActive']
        datos=(_val,int(_id))
        pos = 2
        ModelCareer.edit(db, datos, pos)
    return redirect(url_for('careers_form'))

@app.route('/admin/careers/delete/<id>', methods=['GET','POST'])
@login_required
@check_role(['admin'])
def delete_careers(id):
    is_subject_exists = ModelSignature.get_by_career(db, id)
    if is_subject_exists != None:
        flash('La carrera no se puede eliminar, tiene asignadas materias.')
        return redirect(url_for('careers_form'))    
    print(id)
    ModelCareer.delete(db, id)
    return redirect(url_for('careers_form'))

@app.route('/admin/signatures', methods=['GET','POST'])
@login_required
@check_role(['admin','aux'])
def signatures_form():
    _pos = ""
    _data = ""
    if request.form.get('txtFilter'): 
        _filterSelected = request.form['txtFilter']
        _pos=_filterSelected
        print(_filterSelected)
    if request.form.get('txtTeacherFilter'): 
        _filterTeacher = request.form['txtTeacherFilter']
        _data=_filterTeacher
        print(_filterTeacher)
    if request.form.get('txtSignatureFilter'): 
        _filterSignature = request.form['txtSignatureFilter']
        _data=_filterSignature
        print(_filterSignature)
    if request.form.get('txtCareerFilter'): 
        _filterCareer = request.form['txtCareerFilter']
        _data=_filterCareer
        print(_filterCareer)
    if request.form.get('txtActiveFilter'): 
        _filterActive = request.form['txtActiveFilter']
        _data=_filterActive
        print(_filterActive)

    allSignatures=ModelSignature.get_all(db,_pos,_data)
    allCareers = ModelCareer.get_all(db)
    allPersons=ModelPerson.get_all(db)
    max_code = 0
    for signature in allSignatures:
        if signature[2] > max_code:
            max_code = signature[2]
    return render_template('user_admin/signatures.html', allSignatures=allSignatures, allPersons=allPersons, allCareers=allCareers, max_code= max_code)

@app.route('/admin/signatures/save', methods=['POST'])
@login_required
@check_role(['admin','aux'])
def save_signatures():
    _name = request.form['txtName']
    _code = request.form['txtCode']
    _career_from =  request.form['txtCareerFrom']
    # _code_teacher = request.form['txtTeacher']
    _created_at = request.form['txtCreatedAt']
    _active = request.form['txtActive']
    allSignatures=ModelSignature.get_all(db)
    _max_code = 0
    for signature in allSignatures:
        if int(signature[2]) > int(_career_from) and int(signature[2]) < int(_career_from)+100:
            _max_code = int(signature[2]) + 1
    for signature in allSignatures:
        if int(_code) == int(signature[2]):
            val=0
            flash("Error al crear la materia!, Código sugerido " + str(_max_code))
            return redirect(url_for('signatures_form'))    
        else:
            val=1 
    if val:
        ModelSignature.create(db, _name,_code,_career_from, _created_at,_active)
        return redirect(url_for('signatures_form'))    
    
@app.route('/admin/signatures/edit', methods=['POST'])
@login_required
@check_role(['admin','aux'])
def edit_signatures():
    _id = request.form['txtId']
    if request.form.get('chkName') !='yes': None 
    else: 
        _val = request.form['txtName']
        datos=(_val,int(_id))
        pos = 1
        ModelSignature.edit(db,datos, pos)
    if request.form.get('chkCode') !='yes': None
    else: 
        _val = request.form['txtCode']
        datos=(int(_val),int(_id))
        pos = 2
        ModelSignature.edit(db,datos, pos)
    if request.form.get('chkTeacher') !='yes': None
    else: 
        _val = request.form['txtTeacher']
        datos=(int(_val),int(_id))
        pos = 3
        ModelSignature.edit(db,datos, pos)
    if request.form.get('chkCareerFrom') !='yes': None
    else: 
        _val = request.form['txtCareerFrom']
        datos=(int(_val),int(_id))
        pos = 4
        ModelSignature.edit(db,datos, pos)
    if request.form.get('chkActive') !='yes': None
    else: 
        _val = request.form['txtActive']
        datos=(_val,int(_id))
        pos = 5
        ModelSignature.edit(db, datos, pos)
    return redirect(url_for('signatures_form'))

@app.route('/admin/signatures/delete/<id>', methods=['GET','POST'])
@login_required
@check_role(['admin'])
def delete_signatures(id):
    ModelSignature.delete(db, id)
    return redirect(url_for('signatures_form'))

@app.route('/admin/teachers', methods=['GET','POST'])
@login_required
@check_role(['admin','aux'])
def teachers_form():
    _pos = ""
    _data = ""
    if request.form.get('txtFilter'): 
        _filterSelected = request.form['txtFilter']
        _pos=_filterSelected
        print(_filterSelected)
    if request.form.get('txtTeacherFilter'): 
        _filterTeacher = request.form['txtTeacherFilter']
        _data=_filterTeacher
        print(_filterTeacher)
    if request.form.get('txtActiveFilter'): 
        _filterActive = request.form['txtActiveFilter']
        _data=_filterActive
        print(_filterActive)

    allPersons=ModelPerson.get_all(db,_pos,_data)
    codePersons=ModelPerson.get_all(db)
    max_code = 0
    for person in codePersons:
        if person[10] > max_code:
            max_code = person[10]
    return render_template('user_admin/teachers.html',allPersons=allPersons, max_code=max_code )

@app.route('/admin/teachers/<id>', methods=['GET'])
@login_required
@check_role(['admin'])
def get_teacher_by_id(id):
    person=ModelPerson.get_by_id(db, id)
    return render_template('user_admin/teachers.html',person=person )

@app.route('/admin/teachers/save', methods=['POST'])
@login_required
@check_role(['admin','aux'])
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
    _code = request.form['txtCodeTeacher']
    _active = request.form['txtActive']
    ModelPerson.create(db, _fullname,_address,_city,_birth_date, _dni,_phone_number,_email,_created_at,_role,_code,_active)
    return redirect(url_for('teachers_form'))

@app.route('/admin/teachers/edit', methods=['POST'])
@login_required
@check_role(['admin','aux'])
def edit_teachers():
    _id = request.form['txtId']
    if request.form.get('chkAddress') !='yes': None 
    else: 
        _val = request.form['txtAddress']
        datos=(_val,int(_id))
        pos = 1
        ModelPerson.edit(db,datos, pos)
    if request.form.get('chkCity') !='yes': None
    else: 
        _val = request.form['txtCity']
        datos=(_val,int(_id))
        pos = 2
        ModelPerson.edit(db,datos, pos)
    if request.form.get('chkPhoneNumber') !='yes': None 
    else: 
        _val = request.form['txtPhoneNumber']
        datos=(_val,int(_id))
        pos = 3
        ModelPerson.edit(db,datos, pos)
    if request.form.get('chkEmail') !='yes': None
    else: 
        _val = request.form['txtEmail']
        datos=(_val,int(_id))
        pos = 4
        ModelPerson.edit(db,datos, pos)
    if request.form.get('chkActive') !='yes': None
    else: 
        _val = request.form['txtActive']
        datos=(_val,int(_id))
        pos = 5
        ModelPerson.edit(db, datos, pos)
    return redirect(url_for('teachers_form'))

@app.route('/admin/teachers/delete/<id>', methods=['GET','POST'])
@login_required
@check_role(['admin','aux'])
def delete_teachers(id):
    teacher_in_class = ModelCourse.get_by_teacher_class(db, id)
    if teacher_in_class != None:
         flash('Docente no se puede eliminar, tiene asignada una clase.')
         return redirect(url_for('teachers_form'))
    ModelPerson.delete(db, id)
    return redirect(url_for('teachers_form'))

@app.route('/admin/students', methods=['GET','POST'])
@login_required
@check_role(['admin','aux'])
def students_form():
    _pos = ""
    _data = ""
    if request.form.get('txtFilter'): 
        _filterSelected = request.form['txtFilter']
        _pos=_filterSelected
        print(_filterSelected)
    if request.form.get('txtStudentFilter'): 
        _filterStudent = request.form['txtStudentFilter']
        _data=_filterStudent
        print(_filterStudent)
    if request.form.get('txtActiveFilter'): 
        _filterActive = request.form['txtActiveFilter']
        _data=_filterActive
        print(_filterActive)

    allStudents=ModelStudent.get_all(db,_pos,_data)
    codeStudents=ModelStudent.get_all(db)
    max_code = 0
    for codeStudent in codeStudents:
        if codeStudent[9] > max_code:
            max_code = codeStudent[9]
    return render_template('user_admin/students.html',allStudents=allStudents, max_code=max_code )

@app.route('/admin/students/save', methods=['POST'])
@login_required
@check_role(['admin','aux'])
def save_students():
    _fullname = request.form['txtFullname']
    _dni = request.form['txtDU']
    _address = request.form['txtAddress']
    _city = request.form['txtCity']
    _birth_date = request.form['txtBirthDate']
    _phone_number = request.form['txtPhoneNumber']
    _email = request.form['txtEmail']
    _created_at = request.form['txtCreatedAt']
    _code = request.form['txtCodeStudent']
    _active = request.form['txtActive']
    ModelStudent.create(db, _fullname,_address,_city,_birth_date, _dni,_phone_number,_email,_created_at,_code,_active)
    return redirect(url_for('students_form'))

@app.route('/admin/students/edit', methods=['POST'])
@login_required
@check_role(['admin','aux'])
def edit_students():
    _id = request.form['txtId']
    if request.form.get('chkAddress') !='yes': None 
    else: 
        _val = request.form['txtAddress']
        datos=(_val,int(_id))
        pos = 1
        ModelStudent.edit(db,datos, pos)
    if request.form.get('chkCity') !='yes': None
    else: 
        _val = request.form['txtCity']
        datos=(_val,int(_id))
        pos = 2
        ModelStudent.edit(db,datos, pos)
    if request.form.get('chkPhoneNumber') !='yes': None 
    else: 
        _val = request.form['txtPhoneNumber']
        datos=(_val,int(_id))
        pos = 3
        ModelStudent.edit(db,datos, pos)
    if request.form.get('chkEmail') !='yes': None
    else: 
        _val = request.form['txtEmail']
        datos=(_val,int(_id))
        pos = 4
        ModelStudent.edit(db,datos, pos)
    if request.form.get('chkActive') !='yes': None
    else: 
        _val = request.form['txtActive']
        datos=(_val,int(_id))
        pos = 5
        ModelStudent.edit(db, datos, pos)
    return redirect(url_for('students_form'))

@app.route('/admin/students/delete', methods=['POST'])
@app.route('/admin/students/delete/<id>/<code>', methods=['GET'])
@login_required
@check_role(['admin','aux'])
def delete_students(id=None, code=None):
    if request.method == 'POST':
        id = request.form['txtId']
        code = request.form['txtCode'] 
    inClass = ModelStudent.inClass(db, code)
    if request.form.get('chkDeleteStudent') != 'yes': None
    else:
        flash(u"Estudiante eliminado estába en una clase!", 'danger')
        ModelStudent.delete(db, id, code)
        return redirect(url_for('students_form'))
    if inClass:
        flash(u"Estudiante está en una clase, no se puede eliminar!", 'warning')
        return redirect(url_for('students_form'))
    else:
        flash(u"Estudiante eliminado con éxito!", 'success')
        ModelStudent.delete(db, id, code)
        return redirect(url_for('students_form'))
        

@app.route('/admin/class')
@login_required
@check_role(['admin','aux'])
def class_form():
    allCareers=ModelCareer.get_all(db)
    allSubjects = ModelSignature.get_all(db)
    allPersons = ModelPerson.get_all(db)
    allCourses = ModelCourse.get_all(db)
    allStudents=ModelStudent.get_all(db)
    max_temp_code = 0
    for course in allCourses:
        if course[0] > max_temp_code:
            max_temp_code = course[0]
            maxCode = course[0] +1
    return render_template('user_admin/class.html', allCareers=allCareers, allPersons=allPersons, allSubjects=allSubjects, allCourses=allCourses, maxCode=maxCode, allStudents=allStudents)

@app.route('/admin/class/save', methods=['POST'])
@login_required
@check_role(['admin','aux'])
def save_course():
    _id = request.form['txtId']
    _id_materia = request.form['txtIdMateria']
    _id_maestro = request.form['txtIdMaestro']
    is_valid =   ModelCourse.get_by_id(db,_id)
    if is_valid == None:
        flash(u"Clase creada con éxito!", 'success')
        ModelCourse.create(db, _id, _id_materia, _id_maestro)
        return redirect(url_for('class_form'))
    else:
        flash(u"La clase no se ha creado. Verificar código de clase", 'danger')
        return redirect(url_for('class_form'))

@app.route('/admin/class/add', methods=['POST'])
@login_required
@check_role(['admin','aux'])
def add_student():
    _id_course = request.form['txtIdCourse']
    _student_ok = []
    if request.form.get('txtStudent1'):
        _student1 = request.form['txtStudent1']
        print(_student1)
        if ModelCourse.get_by_class(db, _student1, _id_course ) == None:
            if _student1 != "":
               _student_ok.append(_student1)
            else:
                flash(u"Hay algo mal en su listado, verificar. No se cargó ningún estudiante.", 'danger')
                return redirect(url_for('class_form'))
        else:
            flash(u"Hay algo mal en su listado, verificar. No se cargó ningún estudiante.", 'danger')
            return redirect(url_for('class_form'))
    else: _student1 = ""
    if request.form.get('txtStudent2'):    
        _student2 = request.form['txtStudent2']
        print(_student2)
        if ModelCourse.get_by_class(db, _student2, _id_course ) == None:
            if _student2 != "" and _student2 != _student1:
                _student_ok.append(_student2)
            else:
                flash(u"Hay algo mal en su listado, verificar. No se cargó ningún estudiante.", 'danger')
                return redirect(url_for('class_form'))
        else:
            flash(u"Hay algo mal en su listado, verificar. No se cargó ningún estudiante.", 'danger')
            return redirect(url_for('class_form'))
    else: _student2 = ""
    if request.form.get('txtStudent3'):
        _student3 = request.form['txtStudent3']
        print(_student3)
        if ModelCourse.get_by_class(db, _student3, _id_course ) == None:
            if _student3 != "" and _student3 != _student2 and _student3 != _student1:
                _student_ok.append(_student3)
            else:
                flash(u"Hay algo mal en su listado, verificar. No se cargó ningún estudiante.", 'danger')
                return redirect(url_for('class_form'))
        else:
            flash(u"Hay algo mal en su listado, verificar. No se cargó ningún estudiante.", 'danger')
            return redirect(url_for('class_form'))
    else: _student3 = ""
    if request.form.get('txtStudent4'):
        _student4 = request.form['txtStudent4']
        print(_student4)
        if ModelCourse.get_by_class(db, _student4, _id_course ) == None:
            if _student4 != "" and _student4 != _student3 and _student4 != _student2 and _student4 != _student1:
                _student_ok.append(_student4)
            else:
                flash(u"Hay algo mal en su listado, verificar. No se cargó ningún estudiante.", 'danger')
                return redirect(url_for('class_form'))
        else:
            flash(u"Hay algo mal en su listado, verificar. No se cargó ningún estudiante.", 'danger')
            return redirect(url_for('class_form'))
    else: _student4 = ""
    if request.form.get('txtStudent5'):
        _student5 = request.form['txtStudent5']
        print(_student5)
        if ModelCourse.get_by_class(db, _student5, _id_course ) == None:
            if _student5 != "" and _student5 != _student4 and _student5 != _student3 and _student5 != _student2 and _student5 != _student1:
                _student_ok.append(_student5)
            else:
                flash(u"Hay algo mal en su listado, verificar. No se cargó ningún estudiante.", 'danger')
                return redirect(url_for('class_form'))
        else:
            flash(u"Hay algo mal en su listado, verificar. No se cargó ningún estudiante.", 'danger')
            return redirect(url_for('class_form'))
    if len(_student_ok) > 0:
        for _id_student_ok in _student_ok:
            print(_id_student_ok)
            ModelCourse.add_student(db, _id_student_ok, _id_course )
    else:
        flash(u"Hay algo mal en su listado, verificar. No se cargó ningún estudiante.", 'danger')
        return redirect(url_for('class_form'))
    flash(u"Se agregaron todos los estudiantes a la clase con éxito.", 'success')
    return redirect(url_for('class_form'))
        

@app.route('/admin/class/edit', methods=['POST'])
@login_required
@check_role(['admin','aux'])
def edit_course():
    _id = request.form['txtId']
    _id_materia = request.form['txtIdMateria']
    _id_maestro = request.form['txtIdMaestro']
    ModelCourse.edit(db, _id, _id_materia, _id_maestro)
    return redirect(url_for('class_form'))


@app.route('/admin/class/delete/<id>', methods=['GET','POST'])
@login_required
@check_role(['admin','aux'])
def delete_course(id):
    all_students_class = ModelCourse.get_by_student_class(db, id)
    for st in all_students_class:
        ModelCourse.delete_student_class(db, st[0])
    ModelCourse.delete(db, id)
    return redirect(url_for('class_form'))

@app.route('/users')
@login_required
@check_role(['user'])
def user_user():
    _code= session.get('code')
    print(str(_code))
    assignedSub = ModelSignature.get_subject(db, _code)
    return render_template('user_user/index.html', assignedSub=assignedSub)

@app.route('/users/download/report/pdf')
@login_required
@check_role(['user'])
def download_report():
    _code= session.get('code')
    response = ModelSignature.get_report(db, _code)
    return response

@app.route('/users/qualify', methods=['POST'])
@login_required
@check_role(['user'])
def student_qualify():
    _id_subject = request.form['txtIdSubject']
    print(_id_subject)
    _id_student = request.form['txtIdStudent']
    print(_id_student)
    _id_class = request.form['txtIdClass']
    print(_id_class)
    if request.form.get('txtParcial1'):
        _student_q1 = request.form['txtParcial1']
        _q_number = 1
        print(_student_q1)
        ModelStudent.set_qualify(db, _q_number,_id_student , _id_class, _student_q1)
    if request.form.get('txtParcial2'):
        _student_q2 = request.form['txtParcial2']
        _q_number = 2
        print(_student_q2)
        ModelStudent.set_qualify(db, _q_number, _id_student , _id_class, _student_q2)
    if request.form.get('txtParcial3'):
        _student_q3 = request.form['txtParcial3']
        _q_number = 3
        print(_student_q3)
        ModelStudent.set_qualify(db,  _q_number, _id_student , _id_class, _student_q3)
    if request.form.get('txtFinal'):
        _student_q_final = request.form['txtFinal']
        _q_number = 4
        print(_student_q_final)
        ModelStudent.set_qualify(db,  _q_number, _id_student , _id_class, _student_q_final)
    return redirect(url_for('student_class', id=_id_subject))


@app.route('/users/student/<id>')
@login_required
@check_role(['admin','user'])
def student_class(id, code=''):
    _code= session.get('code')
    allStudentsInClass=ModelStudent.get_all_student_in_class(db, id, _code)
    print(allStudentsInClass)
    if len(allStudentsInClass) < 1 :
        print('entro')
        flash('Aun no tiene alumnos asignados a esta clase.')
        return render_template('user_user/students_class.html', allStudentsInClass=allStudentsInClass)    
    return render_template('user_user/students_class.html', allStudentsInClass=allStudentsInClass)

@app.route('/users/student/<id>/<_code>')
@login_required
@check_role(['admin','user'])
def student_class_adm(id, _code):
    # _code= session.get('code')
    allStudentsInClass=ModelStudent.get_all_student_in_class(db, id, _code)
    print(allStudentsInClass)
    if len(allStudentsInClass) < 1 :
        print('entro')
        flash('Aun no tiene alumnos asignados a esta clase.')
        return render_template('user_user/students_class.html', allStudentsInClass=allStudentsInClass)    
    return render_template('user_user/students_class.html', allStudentsInClass=allStudentsInClass)

@app.route("/css/<filecss>")
def css_link(filecss):
    return send_from_directory(os.path.join('./static/css'), filecss)

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