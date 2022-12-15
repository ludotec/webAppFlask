from .entities.Person import Person

class ModelPerson():
    @classmethod
    def get_all(self,db,pos="", data=""):
        _pos=pos
        _data=data 
        match _pos:
            case "":
                sql="SELECT * FROM `person` ORDER BY code"
                pass
            case '0':
                # filter por docente
                sql="SELECT * FROM `person` WHERE code={}""".format(_data)
                pass
            case '1':
                # filter por habilitado o no
                sql="SELECT * FROM `person` WHERE habilitado={}".format(_data)
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
    def create(self, db, fullname, address, city, birth_date, dni, phone_number, email, created_at, rol, code, active):
        try:
            con=db.connect()
            cursor=con.cursor()
            sql_create_teacher="""INSERT INTO `person`(`id`, `apenom`, `direccion`, `localidad`, `fecha_nac`, `dni`,
             `telefono`, `correo_elect`, `creado_el`, `rol`, `code`, `habilitado`) VALUES (null,%s, %s, %s, %s,%s, %s, %s, %s, %s,%s,%s)"""
            datos=(fullname, address, city, birth_date, dni, phone_number, email, created_at, rol, code, active)
            cursor.execute(sql_create_teacher, datos)
            con.commit()
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def edit(self, db, datos, pos):
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
    def delete(self, db, id):
        try:
            con=db.connect()
            cursor = con.cursor()
            sql="DELETE FROM `person` WHERE `person`.`code` = {};".format(id)
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


    