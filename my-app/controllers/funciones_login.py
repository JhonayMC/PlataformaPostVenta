# Importandopaquetes desde flask
from flask import session, flash

# Importando conexion a BD
from conexion.conexionBD import connectionBD
# Para  validar contraseña
from werkzeug.security import check_password_hash

import re
# Para encriptar contraseña generate_password_hash
from werkzeug.security import generate_password_hash


def recibeInsertRegisterUser(name_surname, email_user, pass_user):
    respuestaValidar = validarDataRegisterLogin(name_surname, email_user, pass_user)

    if respuestaValidar:
        nueva_password = generate_password_hash(pass_user, method='scrypt')
        try:
            connection = connectionBD()
            if connection:
                with connection.cursor() as mycursor:
                    sql = "INSERT INTO users(name_surname, email_user, pass_user) VALUES (?, ?, ?)"
                    valores = (name_surname, email_user, nueva_password)
                    mycursor.execute(sql, valores)
                    connection.commit()
                    resultado_insert = mycursor.rowcount
                    return resultado_insert
            else:
                return None
        except Exception as e:
            print(f"Error en el Insert users: {e}")
            return None
    else:
        return False

def validarDataRegisterLogin(name_surname, email_user, pass_user):
    try:
        connection = connectionBD()
        if connection:
            with connection.cursor() as cursor:
                querySQL = "SELECT * FROM users WHERE email_user = ?"
                cursor.execute(querySQL, (email_user,))
                userBD = cursor.fetchone()  # Obtener la primera fila de resultados

                if userBD is not None:
                    flash('El registro no fue procesado, ya existe la cuenta', 'error')
                    return False
                elif not re.match(r'[^@]+@[^@]+\.[^@]+', email_user):
                    flash('El correo es inválido', 'error')
                    return False
                elif not name_surname or not email_user or not pass_user:
                    flash('Por favor llene los campos del formulario.', 'error')
                    return False
                else:
                    # La cuenta no existe y los datos del formulario son válidos, puedo realizar el Insert
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
                querySQL = "SELECT name_surname, email_user FROM users WHERE id = ?"
                cursor.execute(querySQL, (session['id'],))
                info_perfil = cursor.fetchall()
        return info_perfil
    except Exception as e:
        print(f"Error en info_perfil_session : {e}")
        return []


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
        "email_user": session['email_user']
    }
    return inforLogin
