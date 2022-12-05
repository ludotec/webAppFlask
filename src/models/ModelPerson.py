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