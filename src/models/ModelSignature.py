from .entities.Signature import Signature

class ModelSignature():
    @classmethod
    def get_all(self,db):
        try:
            con=db.connect()
            cursor = con.cursor()
            sql="SELECT * FROM `materia`"
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
    def create(self, db, name, code, career_from, created_at, active):
        try:
            con=db.connect()
            cursor=con.cursor()
            sql="""INSERT INTO `materia`(`id`,`nombre`, `code`, `id_carrera`, `creado_el`, `habilitado`)
             VALUES (null,%s, %s, %s, %s,%s)"""
            datos=(name, code, career_from, created_at, active)
            cursor.execute(sql, datos)
            con.commit()
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def edit(self, db, datos, pos):
        try:
            match pos :
                case 1 :
                    _sql = "UPDATE `materia` SET `nombre`=%s  WHERE `id`= %s"
                    con=db.connect()
                    cursor=con.cursor()
                    cursor.execute(_sql, datos)
                    con.commit()
                    pass
                case 2 :
                    _sql = "UPDATE `materia` SET `code`=%s  WHERE `id`= %s"
                    con=db.connect()
                    cursor=con.cursor()
                    cursor.execute(_sql, datos)
                    con.commit()
                    pass
                case 3 :
                    _sql = "UPDATE `materia` SET `id_carrera`=%s  WHERE `id`= %s"
                    con=db.connect()
                    cursor=con.cursor()
                    cursor.execute(_sql, datos)
                    con.commit()
                    pass
                case 5 :
                    _sql = "UPDATE `materia` SET `habilitado`=%s  WHERE `id`= %s"
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
            sql="DELETE FROM `materia` WHERE `materia`.`id` = {};".format(id)
            cursor.execute(sql)
            con.commit()
        except Exception as ex:
            raise Exception(ex)


    