class ModelStudent():
    @classmethod
    def get_all(self,db,pos="", data=""):
        _pos=pos
        _data=data 
        match _pos:
            case "":
                sql="SELECT * FROM `student`"
                pass
            case '0':
                # filter por docente
                sql="SELECT * FROM `student` WHERE code={}""".format(_data)
                pass
            case '1':
                # filter por habilitado o no
                sql="SELECT * FROM `student` WHERE active={}".format(_data)
                pass
        try:
            con=db.connect()
            cursor = con.cursor()
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
    def create(self, db, fullname, address, city, birth_date, dni, phone_number, email, created_at, code, active):
        try:
            con=db.connect()
            cursor=con.cursor()
            sql="""INSERT INTO `student`(`id`, `fullname`, `email`, 
            `address`, `city`, `phone`, `dni`, `fecha_nac`, `created_at`, `code`, `active`) 
            VALUES (null,%s, %s, %s, %s,%s, %s, %s, %s, %s,%s)"""
            datos=(fullname,  email, address, city, phone_number, dni, birth_date, created_at,code, active)
            cursor.execute(sql, datos)
            con.commit()
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def edit(self, db, datos, pos):
        try:
            match pos :
                case 1 :
                    _sql = "UPDATE `student` SET `address`=%s  WHERE `id`= %s"
                    con=db.connect()
                    cursor=con.cursor()
                    cursor.execute(_sql, datos)
                    con.commit()
                    pass
                case 2 :
                    _sql = "UPDATE `student` SET `city`=%s  WHERE `id`= %s"
                    con=db.connect()
                    cursor=con.cursor()
                    cursor.execute(_sql, datos)
                    con.commit()
                    pass
                case 3 :
                    _sql = "UPDATE `student` SET `phone`=%s  WHERE `id`= %s"
                    con=db.connect()
                    cursor=con.cursor()
                    cursor.execute(_sql, datos)
                    con.commit()
                    pass
                case 4 :
                    _sql = "UPDATE `student` SET `email`=%s  WHERE `id`= %s"
                    con=db.connect()
                    cursor=con.cursor()
                    cursor.execute(_sql, datos)
                    con.commit()
                    pass
                case 5 :
                    _sql = "UPDATE `student` SET `active`=%s  WHERE `id`= %s"
                    con=db.connect()
                    cursor=con.cursor()
                    cursor.execute(_sql, datos)
                    con.commit()
                    pass
        except Exception as ex:
                raise Exception(ex)

    @classmethod
    def delete(self, db, id, code):
        try:
            con=db.connect()
            cursor = con.cursor()
            sql_student_class = "DELETE FROM student_clase WHERE id_student = {};".format(code)
            sql="DELETE FROM `student` WHERE `student`.`id` = {};".format(id)
            cursor.execute(sql_student_class)
            cursor.execute(sql)
            con.commit()
        except Exception as ex:
            raise Exception(ex)


    @classmethod
    def get_by_id(self, db, id):
        try:
            con=db.connect()
            cursor = con.cursor()
            sql="SELECT * FROM `student` WHERE id = '{}'".format(id)
            cursor.execute(sql)
            row=cursor.fetchone()
            con.commit()
            if row != None:
                return row
            else:
                return None
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def inClass(self, db, code):
        try:
            con=db.connect()
            cursor = con.cursor()
            sql="SELECT * FROM `student_clase` WHERE id_student = '{}'".format(code)
            cursor.execute(sql)
            row=cursor.fetchone()
            con.commit()
            if row != None:
                return True
            else:
                return None
        except Exception as ex:
            raise Exception(ex)