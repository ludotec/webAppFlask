from .entities.Person import Person

class ModelPerson():
    @classmethod
    def get_all(self,db):
        try:
            con=db.connect()
            cursor = con.cursor()
            sql="SELECT * FROM `person`"
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
    def set_teacher(self, db, fullname, address, city, birth_date, dni, phone_number, email, created_at, rol, active):
        try:
            con=db.connect()
            cursor=con.cursor()
            sql_create_teacher="""INSERT INTO `person`(`id`, `apenom`, `direccion`, `localidad`, `fecha_nac`, `dni`,
             `telefono`, `correo_elect`, `creado_el`, `rol`, `habilitado`) VALUES (null,%s, %s, %s, %s,%s, %s, %s, %s, %s,%s)"""
            datos=(fullname, address, city, birth_date, dni, phone_number, email, created_at, rol, active)
            cursor.execute(sql_create_teacher, datos)
            con.commit()
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def edit_teacher(self, db, datos, pos):
        try:
            match pos :
                case 1 :
                    _sql = "UPDATE `person` SET `direccion`=%s  WHERE `id`= %s"
                    con=db.connect()
                    cursor=con.cursor()
                    cursor.execute(_sql, datos)
                    con.commit()
                    pass
                case 2 :
                    _sql = "UPDATE `person` SET `localidad`=%s  WHERE `id`= %s"
                    con=db.connect()
                    cursor=con.cursor()
                    cursor.execute(_sql, datos)
                    con.commit()
                    pass
                case 3 :
                    _sql = "UPDATE `person` SET `telefono`=%s  WHERE `id`= %s"
                    con=db.connect()
                    cursor=con.cursor()
                    cursor.execute(_sql, datos)
                    con.commit()
                    pass
                case 4 :
                    _sql = "UPDATE `person` SET `correo_elect`=%s  WHERE `id`= %s"
                    con=db.connect()
                    cursor=con.cursor()
                    cursor.execute(_sql, datos)
                    con.commit()
                    pass
                case 5 :
                    _sql = "UPDATE `person` SET `habilitado`=%s  WHERE `id`= %s"
                    con=db.connect()
                    cursor=con.cursor()
                    cursor.execute(_sql, datos)
                    con.commit()
                    pass
        except Exception as ex:
                raise Exception(ex)

    @classmethod
    def delete_teacher(self, db, id):
        try:
            con=db.connect()
            cursor = con.cursor()
            sql="DELETE FROM `person` WHERE `person`.`id` = {};".format(id)
            cursor.execute(sql)
            con.commit()
        except Exception as ex:
            raise Exception(ex)


    @classmethod
    def get_by_id(self, db, id):
        try:
            con=db.connect()
            cursor = con.cursor()
            sql="SELECT * FROM `person` WHERE id = '{}'".format(id)
            cursor.execute(sql)
            row=cursor.fetchone()
            con.commit()
            if row != None:
                return row
            else:
                return None
        except Exception as ex:
            raise Exception(ex)