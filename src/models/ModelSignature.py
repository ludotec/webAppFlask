from .entities.Signature import Signature
from fpdf import FPDF
from flask import Response 

class ModelSignature():
    @classmethod
    def get_all(self,db,pos="", data=""):
        _pos=pos
        _data=data
        match _pos:
            case "":
                sql="""SELECT m.id, m.nombre, m.code, `carrera`.`nombre`, m.creado_el, m.habilitado,
                m.id_carrera FROM `materia` m
                INNER JOIN `carrera` ON `carrera`.`code` = `id_carrera`"""
                pass
            case '0':
                # filter por materia
                sql="""SELECT m.id, m.nombre, m.code, `carrera`.`nombre`, `person`.`apenom`, m.creado_el, m.habilitado,
                m.code_teacher, m.id_carrera FROM `materia` m
                INNER JOIN `person` ON `person`.`code`= `code_teacher`
                INNER JOIN `carrera` ON `carrera`.`code` = `id_carrera`
                WHERE m.id={}""".format(_data)
                pass
            case '1':
                # filter por código de carrera
                sql="""SELECT m.id, m.nombre, m.code, `carrera`.`nombre`, `person`.`apenom`, m.creado_el, m.habilitado,
                m.code_teacher, m.id_carrera FROM `materia` m
                INNER JOIN `person` ON `person`.`code`= `code_teacher`
                INNER JOIN `carrera` ON `carrera`.`code` = `id_carrera`
                WHERE m.id_carrera={}""".format(_data)
                pass
            case '2':
                # filter por docente
                sql="""SELECT m.id, m.nombre, m.code, `carrera`.`nombre`, `person`.`apenom`, m.creado_el, m.habilitado,
                m.code_teacher, m.id_carrera FROM `materia` m
                INNER JOIN `person` ON `person`.`code`= `code_teacher`
                INNER JOIN `carrera` ON `carrera`.`code` = `id_carrera`
                WHERE m.code_teacher={}""".format(_data)
                pass
            case '3':
                sql="""SELECT m.id, m.nombre, m.code, `carrera`.`nombre`, `person`.`apenom`, m.creado_el, m.habilitado,
                m.code_teacher, m.id_carrera FROM `materia` m
                INNER JOIN `person` ON `person`.`code`= `code_teacher`
                INNER JOIN `carrera` ON `carrera`.`code` = `id_carrera`
                WHERE m.habilitado={}""".format(_data)
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
                    _sql = "UPDATE `materia` SET `code_teacher`=%s  WHERE `id`= %s"
                    con=db.connect()
                    cursor=con.cursor()
                    cursor.execute(_sql, datos)
                    con.commit()
                    pass
                case 4 :
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

    @classmethod
    def get_subject(self, db, code):
        try:
            con=db.connect()
            cursor = con.cursor()
            sql="""SELECT m.id, m.nombre, `carrera`.`nombre`, m.code FROM `materia` m
                INNER JOIN `clase` ON `clase`.`id_materia` = m.code
                INNER JOIN `carrera` ON `carrera`.`code` = `id_carrera`
                WHERE `clase`.`id_maestro`= {};""".format(code)
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
    def get_by_career(self, db, code):
        try:
            con=db.connect()
            cursor = con.cursor()
            sql="""SELECT * FROM `materia` WHERE `materia`.`id_carrera`= {};""".format(code)
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
    def get_report(self, db, code):
        try:
            con=db.connect()
            cursor = con.cursor()
            sql="""SELECT m.id, m.nombre, `carrera`.`nombre`, m.code FROM `materia` m
                INNER JOIN `clase` ON `clase`.`id_materia` = m.code
                INNER JOIN `carrera` ON `carrera`.`code` = `id_carrera`
                WHERE `clase`.`id_maestro`= {};""".format(code)
            cursor.execute(sql)
            row=cursor.fetchall()
            pdf = FPDF()
            pdf.add_page()
            page_width = pdf.w -2 * pdf.l_margin
            pdf.set_font('Times','B', 22.0)
            pdf.set_text_color(0,125,255)
            pdf.cell(page_width, 0.0, 'Materias Asignadas', align='C')
            pdf.ln(10)
            pdf.set_font('Courier', '',12)
            pdf.set_text_color(64,64,64)
            col_width = page_width/2
            pdf.ln(1)
            th = pdf.font_size
            for r in row:
                pdf.cell(col_width, th, str(r[1]), border=1)
                res =r[2]
                rcut= res[:30]
                rcut = rcut + '...'
                pdf.cell(col_width, th, rcut, border=1)
                pdf.ln(th)
            
            pdf.ln(10)
            pdf.set_font('Times', '', 10.0)
            pdf.cell(page_width, 0.0, '- fin del reporte -', align='C')
            response = Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf', headers={'Content-Disposition':'inline;filename=materias_asignadas.pdf'})
            con.commit()
            if row != None:
                return response
            else:
                return None
        except Exception as ex:
            raise Exception(ex)

    