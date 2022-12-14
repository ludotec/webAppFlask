class ModelCourse():
    
    @classmethod
    def new_course(self, db, ):
        try:
            pass
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_all(self,db):
        try:
            con=db.connect()
            cursor = con.cursor()
            sql="""SELECT clase.id, carrera.nombre, materia.nombre,  person.apenom FROM `clase`
            INNER JOIN materia ON materia.code = clase.id_materia
            INNER JOIN person ON person.code = clase.id_maestro
            INNER JOIN carrera on carrera.code = materia.id_carrera"""
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
    def get_by_id(self,db,id):
        try:
            con=db.connect()
            cursor = con.cursor()
            sql="SELECT * FROM `clase` WHERE id={}".format(id)
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
    def create(self, db, id, id_materia, id_maestro):
        try:
            con=db.connect()
            cursor = con.cursor()
            sql="INSERT INTO `clase`(`id`, `id_materia`, `id_maestro`) VALUES (%s,%s,%s)"
            datos = (id, id_materia, id_maestro)
            cursor.execute(sql, datos)
            con.commit()
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def delete(self, db, id):
        try:
            con=db.connect()
            cursor = con.cursor()
            sql="DELETE FROM `clase` WHERE `clase`.`id` = {};".format(id)
            cursor.execute(sql)
            con.commit()
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def add_student(self, db, id_student, id_clase):
        try:
            con=db.connect()
            cursor = con.cursor()
            sql="INSERT INTO `student_clase`(`id`, `id_student`, `id_clase`) VALUES (null,%s,%s)"
            datos = (id_student, id_clase)
            cursor.execute(sql, datos)
            con.commit()
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_by_class(self,db,id_student, id_clase):
        try:
            con=db.connect()
            cursor = con.cursor()
            sql="SELECT * FROM `student_clase` WHERE id_student=%s AND id_clase=%s"
            datos= (id_student, id_clase)
            cursor.execute(sql, datos)
            row=cursor.fetchone()
            con.commit()
            if row != None:
                return row
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
       
    
