# Importandopaquetes desde flask
from flask import session, flash

# Importando conexion a BD
from conexion.conexionBD import connectionBD
# Para  validar contraseña
from werkzeug.security import check_password_hash

import re
# Para encriptar contraseña generate_password_hash
from werkzeug.security import generate_password_hash


def recibeInsertRegisterUser(name_surname, ruc_user, pass_user):
    respuestaValidar = validarDataRegisterLogin(name_surname, ruc_user, pass_user)

    if respuestaValidar:
        nueva_password = generate_password_hash(pass_user, method='scrypt')
        try:
            connection = connectionBD()
            if connection:
                with connection.cursor() as mycursor:
                    sql = "INSERT INTO USERS(name_surname, ruc_user, pass_user) VALUES (?, ?, ?)"
                    valores = (name_surname, ruc_user, nueva_password)
                    mycursor.execute(sql, valores)
                    connection.commit()
                    resultado_insert = mycursor.rowcount
                    return resultado_insert
            else:
                return 0
        except Exception as e:
            print(f"Error en el Insert users: {e}")
            return 0
    else:
        return 0

def validarDataRegisterLogin(name_surname, ruc_user, pass_user):
    try:
        connection = connectionBD()
        if connection:
            with connection.cursor() as cursor:
                querySQL = "SELECT * FROM USERS WHERE ruc_user = ?"
                cursor.execute(querySQL, (ruc_user,))
                userBD = cursor.fetchone()

                if userBD is not None:
                    flash('El registro no fue procesado, ya existe la cuenta', 'error')
                    return False
                # Removida la validación de email ya que usamos RUC/DNI
                elif not ruc_user.isdigit():  # Validación básica para RUC/DNI
                    flash('El RUC/DNI debe contener solo números', 'error')
                    return False
                elif not name_surname or not ruc_user or not pass_user:
                    flash('Por favor llene los campos del formulario.', 'error')
                    return False
                else:
                    return True
        else:
            return False
    except Exception as e:
        print(f"Error en validarDataRegisterLogin : {e}")
        return False

def info_perfil_session():
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor() as cursor:
                # Cambiado email_user por ruc_user en el SELECT
                querySQL = "SELECT name_surname, email_user as ruc_user FROM USERS WHERE id = ?"
                cursor.execute(querySQL, (session['id'],))
                info_perfil = cursor.fetchall()
        return info_perfil
    except Exception as e:
        print(f"Error en info_perfil_session : {e}")
        return []

def dataLoginSesion():
    inforLogin = {
        "id": session['id'],
        "name_surname": session['name_surname'],
        "ruc_user": session['ruc_user']  # Cambiado email_user por ruc_user
    }
    return inforLogin


# def procesar_update_perfil(data_form):
#     # Extraer datos del diccionario data_form
#     id_user = session['id']
#     name_surname = data_form['name_surname']
#     email_user = data_form['email_user']
#     pass_actual = data_form['pass_actual']
#     new_pass_user = data_form['new_pass_user']
#     repetir_pass_user = data_form['repetir_pass_user']

#     if not pass_actual or not email_user:
#         return 3

#     with connectionBD() as conexion_MySQLdb:
#         with conexion_MySQLdb.cursor() as cursor:
#             querySQL = """SELECT * FROM users WHERE email_user = ?"""
#             cursor.execute(querySQL, (email_user,))
#             account = cursor.fetchone()
#             if account:
#                 columns = [column[0] for column in cursor.description]
#                 account_dict = dict(zip(columns, account))
#                 if check_password_hash(account_dict['pass_user'], pass_actual):
#                     # Verificar si new_pass_user y repetir_pass_user están vacías
#                     if not new_pass_user or not repetir_pass_user:
#                         return updatePefilSinPass(id_user, name_surname)
#                     else:
#                         if new_pass_user != repetir_pass_user:
#                             return 2
#                         else:
#                             try:
#                                 nueva_password = generate_password_hash(
#                                     new_pass_user, method='scrypt')
#                                 with connectionBD() as conexion_MySQLdb:
#                                     with conexion_MySQLdb.cursor() as cursor:
#                                         querySQL = """
#                                             UPDATE users
#                                             SET 
#                                                 name_surname = ?,
#                                                 pass_user = ?
#                                             WHERE id = ?
#                                         """
#                                         params = (name_surname,
#                                                   nueva_password, id_user)
#                                         cursor.execute(querySQL, params)
#                                         conexion_MySQLdb.commit()
#                                 return cursor.rowcount or []
#                             except Exception as e:
#                                 print(
#                                     f"Ocurrió en procesar_update_perfil: {e}")
#                                 return []
#             else:
#                 return 0
def procesar_update_perfil(data_form):
    # Extraer datos del diccionario data_form
    id_user = session['id']
    name_surname = data_form['name_surname']
    email_user = data_form['email_user']
    pass_actual = data_form['pass_actual']
    new_pass_user = data_form['new_pass_user']
    repetir_pass_user = data_form['repetir_pass_user']

    if not pass_actual or not email_user:
        return 3  # Clave actual o email vacío

    with connectionBD() as conexion_MySQLdb:
        with conexion_MySQLdb.cursor() as cursor:
            querySQL = """SELECT * FROM users WHERE email_user = ?"""
            cursor.execute(querySQL, (email_user,))
            account = cursor.fetchone()
            
            if account:
                columns = [column[0] for column in cursor.description]
                account_dict = dict(zip(columns, account))
                
                if check_password_hash(account_dict['pass_user'], pass_actual):
                    # Verificar si new_pass_user y repetir_pass_user están vacías
                    if not new_pass_user or not repetir_pass_user:
                        return updatePefilSinPass(id_user, name_surname)
                    else:
                        if new_pass_user != repetir_pass_user:
                            return 2  # Nuevas contraseñas no coinciden
                        else:
                            try:
                                nueva_password = generate_password_hash(new_pass_user, method='scrypt')
                                with connectionBD() as conexion_MySQLdb:
                                    with conexion_MySQLdb.cursor() as cursor:
                                        querySQL = """
                                            UPDATE users
                                            SET 
                                                name_surname = ?,
                                                pass_user = ?
                                            WHERE id = ?
                                        """
                                        params = (name_surname, nueva_password, id_user)
                                        cursor.execute(querySQL, params)
                                        conexion_MySQLdb.commit()
                                return cursor.rowcount
                            except Exception as e:
                                print(f"Ocurrió en procesar_update_perfil: {e}")
                                return 0  # Cambié [] a 0 para simplificar el manejo de errores
                else:
                    return 0  # Contraseña actual incorrecta
            else:
                return 0  # Usuario no encontrado


def updatePefilSinPass(id_user, name_surname):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor() as cursor:
                querySQL = """
                    UPDATE users
                    SET 
                        name_surname = ?
                    WHERE id = ?
                """
                params = (name_surname, id_user)
                cursor.execute(querySQL, params)
                conexion_MySQLdb.commit()
        return cursor.rowcount
    except Exception as e:
        print(f"Ocurrió un error en la funcion updatePefilSinPass: {e}")
        return []


def dataLoginSesion():
    inforLogin = {
        "id": session['id'],
        "name_surname": session['name_surname'],
        "ruc_user": session['ruc_user']
    }
    return inforLogin

#Para guardar a los usuarios MyM
def recibeInsertRegisterUserMyM(nombre_completo, usuario, password, compania, rol):
    # Validar los datos antes de procesar
    respuestaValidar = validarDataRegisterLoginMyM(nombre_completo, usuario, password, compania, rol)

    if respuestaValidar:
        nueva_password = generate_password_hash(password, method='scrypt')  # Encriptar la contraseña
        try:
            # Obtener la conexión a la base de datos
            connection = connectionBD()
            if connection:
                with connection.cursor() as mycursor:
                    # Consulta SQL para insertar los datos en la tabla UsersMyM
                    sql = "INSERT INTO UsersMyM (nombre_completo, usuario, password, compania, rol) VALUES (?, ?, ?, ?, ?)"
                    valores = (nombre_completo, usuario, nueva_password, compania, rol)
                    mycursor.execute(sql, valores)
                    connection.commit()
                    resultado_insert = mycursor.rowcount  # Verificar cuántas filas fueron afectadas
                    return resultado_insert
            else:
                return 0  # Retorna 0 si no se pudo conectar a la base de datos
        except Exception as e:
            print(f"Error en el Insert UsersMyM: {e}")  # Mostrar el error en caso de fallo
            return 0
    else:
        return 0  # Retorna 0 si la validación falla

def validarDataRegisterLoginMyM(nombre_completo, usuario, password, compania, rol):
    try:
        connection = connectionBD()
        if connection:
            with connection.cursor() as cursor:
                querySQL = "SELECT * FROM UsersMyM WHERE usuario = ?"
                cursor.execute(querySQL, (usuario,))
                userBD = cursor.fetchone()

                if userBD is not None:
                    flash('El registro no fue procesado, ya existe la cuenta', 'error')
                    return False
                elif not nombre_completo or not usuario or not password or not compania or not rol:
                    flash('Por favor llene los campos del formulario.', 'error')
                    return False
                else:
                    return True
        else:
            return False
    except Exception as e:
        print(f"Error en validarDataRegisterLoginMyM: {e}")
        return False
