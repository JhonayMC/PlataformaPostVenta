
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
        return redirect(url_for('dashboard'))
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
                    return redirect(url_for('dashboard'))
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
@app.route('/login-mym', methods=['GET', 'POST'])
def loginUserMyM():
    if 'loggedin' in session:
        return redirect(url_for('menuMyM'))
    else:
        if request.method == 'POST' and 'usuario' in request.form and 'password' in request.form and 'compania' in request.form:
            usuario = str(request.form['usuario'])
            password = str(request.form['password'])
            compania = str(request.form['compania'])
            compania_map = {
                '1': '30 ANADI', 
                '2': '10 M&M REPUESTOS Y SERVICIOS S.A.'
            }
            mapped_company = compania_map[compania]
            conexion_MySQLdb = connectionBD()
            cursor = conexion_MySQLdb.cursor()
            cursor.execute(""" SELECT * FROM UsersMyM 
                WHERE usuario = ? AND compania = ?
            """, (usuario, mapped_company))
            account = cursor.fetchone()
            if account:
                columns = [column[0] for column in cursor.description]
                account_dict = dict(zip(columns, account))
                
                # Use the correct column name for password
                # Assuming the password column is actually named 'password' or something similar
                if check_password_hash(account_dict['password'], password):
                    session['loggedin'] = True
                    session['id'] = account_dict['id']
                    session['usuario'] = account_dict['usuario']
                    session['compania'] = account_dict['compania']
                    flash('la sesión fue correcta.', 'success')
                    return redirect(url_for('menuMyM'))
                else:
                    flash('datos incorrectos por favor revise.', 'error')
                    return render_template(f'{PATH_URL_LOGIN}/auth_login_usuario.html')
            else:
                flash('el usuario no existe, por favor verifique.', 'error')
                return render_template(f'{PATH_URL_LOGIN}/auth_login_usuario.html')
        else:
            flash('primero debes iniciar sesión.', 'error')
            return render_template(f'{PATH_URL_LOGIN}/auth_login_usuario.html')


# Registro de Usuario MyM . /register-mym
@app.route('/register-mym', methods=['GET'])
def register_mym():
    return render_template(f'{PATH_URL_LOGIN}/auth_register_usuario.html')

#Para manejar el registro de un usuario MyM DE auth_register_usuario.html
@app.route('/saved-register-mym', methods=['POST'])
def saved_register_mym():
    if request.method == 'POST' and 'nombre_completo_mym' in request.form and 'usuario_mym' in request.form and 'password_mym' in request.form and 'compania_mym' in request.form:
        nombre_completo = request.form['nombre_completo_mym']
        usuario = request.form['usuario_mym']
        password = request.form['password_mym']
        compania = request.form['compania_mym']

        # Llamada a la función de inserción
        resultData = recibeInsertRegisterUserMyM(
            nombre_completo, usuario, password, compania
        )

        if resultData:  # Si la inserción fue exitosa
            flash('Usuario registrado exitosamente.', 'success')
            return redirect(url_for('inicio'))
        else:
            flash('Error al registrar usuario. Por favor, intente nuevamente.', 'error')
            return redirect(url_for('inicio'))
    else:
        flash('Todos los campos son requeridos.', 'error')
        return redirect(url_for('inicio'))



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

#Redirigir al dashborad de mi pagina, mi menu principal
@app.route('/dashboard')
def dashboard():
    if 'conectado' in session:  # Verificar si el usuario está logueado
        # Si está logueado, mostrar la página del dashboard
        return render_template('public/includes/dashboard.html')
    else:
        # Si no está logueado, redirigir al login
        flash('Debes iniciar sesión para acceder al dashboard', 'error')
        return redirect(url_for('loginCliente')) 
    
#Redirigir a mi menuMyM, despues de hacer login
@app.route('/menu-mym')
def menuMyM():
    if 'loggedin' in session:  # Verificar si el usuario está logueado
        # Si está logueado, mostrar la página del dashboard
        return render_template('public/includes/menuMyM.html')
    else:
        # Si no está logueado, redirigir al login
        flash('Debes iniciar sesión para acceder al dashboard', 'error')
        return redirect(url_for('loginUserMyM'))

    
