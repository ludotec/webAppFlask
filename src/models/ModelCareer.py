from .entities.Career import Career

class ModelCareer():
    @classmethod
    def get_all(self,db):
        try:
            con=db.connect()
            cursor = con.cursor()
            sql="SELECT * FROM `carrera`"
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
    def create(self, db, name, code, created_at, active):
        try:
            con=db.connect()
            cursor=con.cursor()
            sql_create_teacher="""INSERT INTO `carrera`(`id`, `nombre`, `code`, `creado_el`, `habilitado`) VALUES (null,%s, %s, %s, %s)"""
            datos=(name, code, created_at, active)
            cursor.execute(sql_create_teacher, datos)
            con.commit()
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def edit(self, db, datos, pos):
        try:
            match pos :
                case 1 :
                    _sql = "UPDATE `carrera` SET `nombre`=%s  WHERE `id`= %s"
                    con=db.connect()
                    cursor=con.cursor()
                    cursor.execute(_sql, datos)
                    con.commit()
                    pass
                case 2 :
                    _sql = "UPDATE `carrera` SET `habilitado`=%s  WHERE `id`= %s"
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
            sql="DELETE FROM `carrera` WHERE `carrera`.`code` = {};".format(id)
            cursor.execute(sql)
            con.commit()
        except Exception as ex:
            raise Exception(ex)
