from .entities.User import User
from werkzeug.security import generate_password_hash

class ModelUser():

    @classmethod
    def login(self, db, user):
        try:
            con=db.connect()
            cursor = con.cursor()
            sql="""SELECT id, username, password, fullname , code FROM user
                    WHERE username = '{}'""".format(user.username)
            cursor.execute(sql)
            row=cursor.fetchone()
            con.commit()
            if row != None:
                user=User(row[0],row[1],User.check_password(row[2],user.password),row[3],None,row[4])
                return user
            else:
                return None
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_by_id(self, db, id):
        try:
            con=db.connect()
            cursor = con.cursor()
            sql="""SELECT user.id, username, fullname, rol.rol_nombre FROM user
            INNER JOIN user_rol ON user_rol.user_id = user.id
            INNER JOIN rol ON rol.id = user_rol.rol_id
            WHERE user.id = '{}'""".format(id)
            cursor.execute(sql)
            row=cursor.fetchone()
            con.commit()
            if row != None:
                return User(row[0],row[1],None,row[2],row[3])
            else:
                return None
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_by_role(self, db, role, name_user):
        try:
            con=db.connect()
            cursor = con.cursor()
            sql="""SELECT user.id, username, fullname FROM user
                   INNER JOIN user_rol ON user_rol.user_id = user.id
                   INNER JOIN rol ON rol.id = user_rol.rol_id
                   WHERE rol.rol_nombre LIKE '%{}%' AND user.username LIKE '%{}%'
                    """.format(role, name_user)
            cursor.execute(sql)
            row=cursor.fetchone()
            con.commit()
            if row != None:
                return User(row[0],row[1],None,row[2])
            else:
                return None
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_by_role_id(self, db, name_user):
        try:
            con=db.connect()
            cursor = con.cursor()
            sql="""SELECT rol.id FROM rol
                INNER JOIN user_rol ON user_rol.rol_id = rol.id
                INNER JOIN user ON user.id = user_rol.user_id
                WHERE user.username LIKE '%{}%'""".format(name_user)
            cursor.execute(sql)
            row=cursor.fetchone()
            con.commit()
            if row != None:
                row_string=str(row)
                return row_string[1]
            else:
                return None
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def create(self, db, username, password, fullname, rol, code):
        hashed_password=generate_password_hash(password)
        match rol:
            case 'admin':
                rol_id = 1
            case 'aux'  :
                rol_id = 2
            case 'user' :
                rol_id = 3
                
        try:
            con=db.connect()
            cursor=con.cursor()
            sql_lastId="SELECT max(id) FROM user"
            cursor.execute(sql_lastId)
            row=cursor.fetchone()
            if row != None:
                lastId = row[0] + 1
            sql_create_user="INSERT INTO user (id, username, password, fullname, code) VALUES (%s, %s, %s, %s, %s)"
            datos=(lastId,username, hashed_password, fullname, code)
            cursor.execute(sql_create_user, datos)
            sql_rol_id="INSERT INTO user_rol (rol_id,user_id) VALUES ({}, {})".format(rol_id, lastId )
            cursor.execute(sql_rol_id)
            con.commit()
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_all(self, db):
        try:
            con=db.connect()
            cursor = con.cursor()
            sql="""SELECT `user`.`id`,`user`.`username`,`user`.`fullname`, `rol`.`rol_nombre`  FROM `user`
                    INNER JOIN `user_rol` ON `user_rol`.`user_id`=`user`.`id`
                    INNER JOIN `rol` ON `rol`.`id`=`user_rol`.`rol_id`"""
            cursor.execute(sql)
            row=cursor.fetchall()
            con.commit()
            if row != None:
                return row
            else:
                return None
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def edit(self, db, newPass, id):
        hashed_password=generate_password_hash(newPass)
        try:
            con=db.connect()
            cursor = con.cursor()
            sql = "UPDATE `user` SET `password`='{}' WHERE `id`={} ".format(hashed_password, id)
            cursor.execute(sql)
            con.commit()
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def delete(self, db, id):
        try:
            con=db.connect()
            cursor = con.cursor()
            sql_1="DELETE FROM `user_rol` WHERE `user_rol`.`user_id` = {};".format(id)
            sql_2="DELETE FROM `user` WHERE `user`.`id` = {};".format(id)
            
            cursor.execute(sql_1)
            cursor.execute(sql_2)
            con.commit()
        except Exception as ex:
            raise Exception(ex)
