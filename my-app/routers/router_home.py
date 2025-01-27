from app import app
from flask import render_template, request, flash, redirect, url_for, session,  jsonify
from mysql.connector.errors import Error


# Importando cenexión a BD
from controllers.funciones_home import *

PATH_URL = "public/printer"

# clic en el menu bar
@app.route('/registrar-impresion', methods=['GET'])
def viewFormImpresion():
    if 'conectado' in session:
        return render_template(f'{PATH_URL}/form_impresion.html')
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))

#probando impresion
from flask import jsonify
from flask import jsonify
from flask import request, jsonify


# procesar_nueva_impresion su api calcular_nuevo_correlativo,actualizar_estado_impresoras

from flask import Flask, session, request, redirect, url_for, render_template, flash
import threading

@app.route('/form-registrar-impresion', methods=['POST'])
def FormImpresion():
    if 'conectado' in session:
        resultado, correlativo_actual, nuevo_correlativo,id_impresion= procesar_nueva_impresion(request.form)

        if resultado:
            # # Crear un hilo para ejecutar imprimir_zpl en segundo plano
            # imprimir_thread = threading.Thread(target=imprimir_zpl, args=(request.form['id_impresora'], request.form['id_pallet'], request.form['id_tipo_plantilla'], correlativo_actual, nuevo_correlativo))
            # imprimir_thread.start()
            # # Almacenar el objeto del hilo y su identificador
            # info_hilos[id_impresion] = {'hilo': imprimir_thread, 'identificador': imprimir_thread.ident}
            # Continuar con el proceso principal
            return redirect(url_for('lista_impresiones'))
        else:
            flash('La impresion NO fue registrado.', 'error')

        return render_template(f'{PATH_URL}/form_impresion.html')
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))

# api sql_lista_cola_impresiones
@app.route('/lista-de-cola-impresiones', methods=['GET'])
def lista_impresiones():
    if 'conectado' in session:
        return render_template(f'{PATH_URL}/lista_cola_impresion.html', cola_impresiones=sql_lista_cola_impresiones())
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))


# api sql_detalle_impresion 

@app.route("/detalle-impresion/", methods=['GET'])
@app.route("/detalle-impresion/<int:idImpresion>", methods=['GET'])
def detalleImpresion(idImpresion=None):
    if 'conectado' in session:
        # Verificamos si el parámetro idEmpleado es None o no está presente en la URL
        if idImpresion is None:
            return redirect(url_for('inicio'))
        else:
            detalle_impresion = sql_detalle_impresion(idImpresion) or []
            return render_template(f'{PATH_URL}/detalles_impresion.html', detalle_impresion=detalle_impresion)
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))


#  buscador de por inicales de impresora api de buscarimpresora con java script rebisar buscador.js
@app.route("/buscador-impresora", methods=['POST'])
def viewBuscarimpresoraBD():
    resultadoBusqueda = buscarimpresora(request.json['busqueda'])
    if resultadoBusqueda:
        return render_template(f'{PATH_URL}/resultado_busqueda_impresion.html', dataBusqueda=resultadoBusqueda)
    else:
        return jsonify({'fin': 0})


#generarReporteExcel tercer modulo api activador
@app.route("/descargar-informe-empleados/", methods=['GET'])
def reporteBD():
    if 'conectado' in session:
        return generarReporteExcel()
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))


#api de lista_correlativos 
@app.route("/lista-de-correlativos", methods=['GET'])
def lista_correlativos_actuales():
    if 'conectado' in session:
        resp_correlativos = lista_correlativos()
        return render_template(f'{PATH_URL}/lista_correlativos.html', resp_correlativos=resp_correlativos)
    else:
        return redirect(url_for('inicioCpanel'))
    


@app.route("/lista-de-usuarios", methods=['GET'])
def usuarios():
    if 'conectado' in session:
        resp_usuariosBD = lista_usuariosBD()
        return render_template('public/usuarios/lista_usuarios.html', resp_usuariosBD=resp_usuariosBD)
    else:
        return redirect(url_for('inicioCpanel'))



@app.route('/borrar-usuario/<string:id>', methods=['GET'])
def borrarUsuario(id):
    resp = eliminarUsuario(id)
    if resp:
        flash('El Usuario fue eliminado correctamente', 'success')
        return redirect(url_for('usuarios'))




#reimprimir impresiones boton reemprimir
@app.route('/reemprimir-impresion/<string:id_impresion>', methods=['GET'])
def reemprimirCola(id_impresion):
    # Crear un hilo para ejecutar reimpimir_zpl en segundo plano
    imprimir_thread = threading.Thread(target=reimpimir_zpl, args=(id_impresion,))
    imprimir_thread.start()
    # Almacenar el objeto del hilo y su identificador
    info_hilos[id_impresion] = {'hilo': imprimir_thread, 'identificador': imprimir_thread.ident}
    # Mensaje de flash inmediato y redirección a lista_impresiones
    flash('La reimpresión está en proceso', 'info')
    return redirect(url_for('lista_impresiones'))

# Estructura para almacenar información de hilos
info_hilos = {}

@app.route('/parar-impresion/<string:id_impresion>', methods=['GET'])
def detener_impresion2(id_impresion):
    resp = detener_impresion(id_impresion)
    if resp:
        flash('La impresion fue parada ahora ya puedo reemprimir', 'success')
        return redirect(url_for('lista_impresiones'))
# Llamada a la función para parar la impresión de un hilo específico

#Para que me redirijia a reclamo.html
@app.route('/reclamo', methods=['GET'])
def reclamo():
    if 'conectado' in session:
        return render_template('public/reclamos/reclamo.html')
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))

#Para que me redirijia a otroReclamoQueja.html
@app.route('/otroReclamo', methods=['GET'])
def otroReclamo():
    if 'conectado' in session:
        return render_template('public/reclamos/otroReclamoQueja.html')
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))

    
#Para que me redirijia a consultarEstado.html
@app.route('/consultarEstado', methods=['GET'])
def consultarEstado():
    if 'conectado' in session:
        return render_template('public/reclamos/consultarEstado.html')
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))

#Para que me redirija a otroReclamoG1.html
@app.route('/otroReclamoG1', methods=['GET'])
def otroReclamoG1():
    if 'conectado' in session:
        return render_template('public/reclamos/otroReclamoG1.html')
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))

#Para que me redirija a otroReclamoG2.html
@app.route('/otroReclamoG2', methods=['GET'])
def otroReclamoG2():
    if 'conectado' in session:
        return render_template('public/reclamos/otroReclamoG2.html')
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))
    
#Menu de inicio usuarios MyM

#Para que me redirija a mym_reclamo.html
@app.route('/mym_reclamo', methods=['GET'])
def mym_reclamo():
    if 'loggedin' in session:
        return render_template('public/reclamos/mym_reclamo.html')
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('loginUserMyM'))

#Para que me redirija a mym_otroReclamoQueja.html
@app.route('/mym_otroReclamo', methods=['GET'])
def mym_otroReclamo():
    if 'loggedin' in session:
        return render_template('public/reclamos/mym_otroReclamoQueja.html')
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('loginUserMyM'))
    
#Para que me redirija a mym_otroReclamoG1.html
@app.route('/mym_otroReclamoG1', methods=['GET'])
def mym_otroReclamoG1():
    if 'loggedin' in session:
        return render_template('public/reclamos/mym_otroReclamoG1.html')
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('loginUserMyM'))

#Para que me redirija a otroReclamoG2.html
@app.route('/mym_otroReclamoG2', methods=['GET'])
def mym_otroReclamoG2():
    if 'loggedin' in session:
        return render_template('public/reclamos/mym_otroReclamoG2.html')
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('loginUserMyM'))
    
#Para que me redirija a mym_seguimiento.html
@app.route('/mym_seguimiento', methods=['GET'])
def mym_seguimiento():
    if 'loggedin' in session:
        return render_template('public/reclamos/mym_seguimiento.html')
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('loginUserMyM'))