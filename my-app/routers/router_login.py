
from app import app
from flask import render_template, request, flash, redirect, url_for, session

# Importando mi conexión a BD
from conexion.conexionBD import connectionBD

# Para encriptar contraseña generate_password_hash
from werkzeug.security import check_password_hash

# Importando controllers para el modulo de login
from controllers.funciones_login import *
PATH_URL_LOGIN = "public/login"


@app.route('/', methods=['GET'])
def inicio():
    if 'conectado' in session:
        return render_template('public/base_cpanel.html', dataLogin=dataLoginSesion())
    else:
        return render_template(f'{PATH_URL_LOGIN}/base_login.html')


@app.route('/mi-perfil', methods=['GET'])
def perfil():
    if 'conectado' in session:
        return render_template(f'public/perfil/perfil.html', info_perfil_session=info_perfil_session())
    else:
        return redirect(url_for('inicio'))


# Crear cuenta de usuario
@app.route('/register-user', methods=['GET'])
def cpanelRegisterUser():
    if 'conectado' in session:
        return redirect(url_for('inicio'))
    else:
        return render_template(f'{PATH_URL_LOGIN}/auth_register.html')


# Recuperar cuenta de usuario
@app.route('/recovery-password', methods=['GET'])
def cpanelRecoveryPassUser():
    if 'conectado' in session:
        return redirect(url_for('inicio'))
    else:
        return render_template(f'{PATH_URL_LOGIN}/auth_forgot_password.html')


# Crear cuenta de usuario
@app.route('/saved-register', methods=['POST'])
def cpanelResgisterUserBD():
    if request.method == 'POST' and 'name_surname' in request.form and 'ruc_user' in request.form and 'pass_user' in request.form:
        name_surname = request.form['name_surname']
        ruc_user = request.form['ruc_user']
        pass_user = request.form['pass_user']
        
        resultData = recibeInsertRegisterUser(
            name_surname, ruc_user, pass_user)
            
        if resultData:  # Si resultData es verdadero (mayor que 0)
            flash('La cuenta fue creada correctamente.', 'success')
            return redirect(url_for('inicio'))
        else:
            flash('Error al crear la cuenta. Por favor, intente nuevamente.', 'error')
            return redirect(url_for('inicio'))
    else:
        flash('Todos los campos son requeridos', 'error')
        return redirect(url_for('inicio'))


# Actualizar datos de mi perfil
@app.route("/actualizar-datos-perfil", methods=['POST'])
def actualizarPerfil():
    if request.method == 'POST':
        if 'conectado' in session:
            respuesta = procesar_update_perfil(request.form)
            if respuesta == 1:
                flash('Los datos fuerón actualizados correctamente.', 'success')
                return redirect(url_for('inicio'))
            elif respuesta == 0:
                flash(
                    'La contraseña actual esta incorrecta, por favor verifique.', 'error')
                return redirect(url_for('perfil'))
            elif respuesta == 2:
                flash('Ambas claves deben se igual, por favor verifique.', 'error')
                return redirect(url_for('perfil'))
            elif respuesta == 3:
                flash('La Clave actual es obligatoria.', 'error')
                return redirect(url_for('perfil'))
        else:
            flash('primero debes iniciar sesión.', 'error')
            return redirect(url_for('inicio'))
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))


# Validar sesión
@app.route('/login', methods=['GET', 'POST'])
def loginCliente():
    if 'conectado' in session:
        return redirect(url_for('inicio'))
    else:
        if request.method == 'POST' and 'ruc_user' in request.form and 'pass_user' in request.form:
            ruc_user = str(request.form['ruc_user'])
            pass_user = str(request.form['pass_user'])

            conexion_MySQLdb = connectionBD()
            cursor = conexion_MySQLdb.cursor()
            # Cambiado email_user por ruc_user en la consulta
            cursor.execute("SELECT * FROM USERS WHERE ruc_user = ?", (ruc_user,))
            account = cursor.fetchone()

            if account:
                columns = [column[0] for column in cursor.description]
                account_dict = dict(zip(columns, account))
                if check_password_hash(account_dict['pass_user'], pass_user):
                    session['conectado'] = True
                    session['id'] = account_dict['id']
                    session['name_surname'] = account_dict['name_surname']
                    session['ruc_user'] = account_dict['ruc_user']  # Guardamos el RUC/DNI

                    flash('la sesión fue correcta.', 'success')
                    return redirect(url_for('inicio'))
                else:
                    flash('datos incorrectos por favor revise.', 'error')
                    return render_template(f'{PATH_URL_LOGIN}/base_login.html')
            else:
                flash('el usuario no existe, por favor verifique.', 'error')
                return render_template(f'{PATH_URL_LOGIN}/base_login.html')
        else:
            flash('primero debes iniciar sesión.', 'error')
            return render_template(f'{PATH_URL_LOGIN}/base_login.html')
                                   
# Registro de Usuarios MyM
#Login Usuario MyM
@app.route('/login-mym', methods=['GET'])
def cpanelRegisterUserMym():
    if 'conectado' in session:
        return redirect(url_for('inicio'))
    else:
        return render_template(f'{PATH_URL_LOGIN}/auth_login_usuario.html')

#Registrar
# Registro de Usuario MyM
@app.route('/register-mym', methods=['GET', 'POST'])
def registerUserMym():
    if 'conectado' in session:
        return redirect(url_for('inicio')) 
    else:
        if request.method == 'POST':
            nombre_completo = request.form['nombre_completo_mym']
            user_mym = request.form['user_mym']
            pass_usermym = request.form['pass_usermym']
            company = request.form['company']
            
            # Aquí puedes agregar la lógica para guardar el usuario en la base de datos

            return redirect(url_for('inicio'))  # O redirigir a otra página si es necesario

        return render_template(f'{PATH_URL_LOGIN}/auth_register_usuario.html')


@app.route('/closed-session',  methods=['GET'])
def cerraSesion():
    if request.method == 'GET':
        if 'conectado' in session:
            # Eliminar datos de sesión, esto cerrará la sesión del usuario
            session.pop('conectado', None)
            session.pop('id', None)
            session.pop('name_surname', None)
            session.pop('email', None)
            flash('tu sesión fue cerrada correctamente.', 'success')
            return redirect(url_for('inicio'))
        else:
            flash('recuerde debe iniciar sesión.', 'error')
            return render_template(f'{PATH_URL_LOGIN}/base_login.html')
