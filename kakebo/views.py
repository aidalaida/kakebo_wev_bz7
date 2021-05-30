from flask.helpers import flash
from kakebo import app
from flask import jsonify, render_template, request, redirect, url_for
from kakebo.forms import MovimientosForm
from datetime import date

import sqlite3

def consultaSQL(query, parametros = []):
    # Abrimos conexion
    conexion = sqlite3.connect("movimientos.db") #para conectar (como un tubo) con la Base de Datos
    cur = conexion.cursor() #manejador de la base

    # Ejecutamos consulta

    cur.execute(query, parametros)

    # Obtenemos los datos de la consulta

    claves= cur.description #tupla de tuplas
    filas = cur.fetchall() #lista de tuplas

    # Procesar datos para devolver una lista de diccionarios

    resultado = []
    for fila in filas:
        d = {}
        for tclave, valor in zip(claves, fila):
            d[tclave[0]] = valor
        resultado.append(d) #crea la clave saldo
    conexion.close()
    return resultado

def modificaTablaSQL(query, parametros=[]):
    conexion = sqlite3.connect("movimientos.db") 
    cur = conexion.cursor() 
    cur.execute(query, parametros)
    
    conexion.commit() #el cambio realizado lo fija en la base de datos 
    conexion.close()



@app.route('/') #decoradores que rodean a funciones. de la instancia app. Ruta(METODO)---) recurso /
def index():

    movimientos = consultaSQL("SELECT * FROM movimientos order by fecha;")
    saldo = 0 #se compian con valor no con referencia
    for d in movimientos:
        
        if d['esGasto'] == 0:
            saldo = saldo + d['cantidad']
        else:
            saldo = saldo - d['cantidad']
        d['saldo'] = saldo

    return render_template('movimientos.html', datos = movimientos)

@app.route('/nuevo', methods=['GET', 'POST'])
def nuevo():
    formulario = MovimientosForm()

    if request.method == 'GET':
        return render_template('alta.html', form = formulario)
    else:

        if formulario.validate():
            query = "INSERT INTO movimientos (fecha, concepto, categoria, esGasto, cantidad)  VALUES (?, ?, ?, ?, ?)"
            try:
                modificaTablaSQL(query, [formulario.fecha.data, formulario.concepto.data, formulario.categoria.data, formulario.esGasto.data, formulario.cantidad.data])

            except sqlite3.Error as el_error:
                print("Error en SQL INSERT", el_error)
                flash("Se ha producido un error en la base de datos. Pruebe en unos minutos", "error") #inyecta el mensaje en la plantilla 
                return render_template('alta.html', form=formulario)

            return redirect(url_for("index"))

            #Redirect a la ruta /
        else:
            return render_template('alta.html', form = formulario)

@app.route('/borrar/<int:id>', methods=['GET', 'POST'])
def borrar(id):
    if request.method == 'GET':
        filas = consultaSQL("SELECT * FROM movimientos WHERE id=?", [id])
        if len(filas) == 0:
            flash("El registro no existe") 
            return render_template('borrar.html')

        return render_template('borrar.html', movimiento=filas[0])
    else:
        try:
            modificaTablaSQL("DELETE FROM movimientos WHERE id=?;", [id])
        except sqlite3 as e:
            flash ("Se ha producido un error de la base de datos, vuelva a interntarlo", 'error')
            return redirect(url_for('index'))
        
        flash("Borrado realizado con éxito", 'aviso') #Flash como un print, con aviso o error como un tipo de mensaje de error
        return redirect(url_for('index'))

@app.route('/modificar/<int:id>', methods=['GET', 'POST'])
def modificar(id):

    if request.method == 'GET':
        filas = consultaSQL("SELECT * FROM movimientos WHERE id=?", [id])
        if len(filas) == 0:
            flash("El registro no existe", "error")
            return render_template('modificar.html')
        registro = filas[0]
        registro['fecha'] = date.fromisoformat(registro['fecha']) #con el metodo date

        formulario = MovimientosForm(data=registro)
        
        return render_template('modificar.html', form=formulario)
    else:
        formulario = MovimientosForm()
        if formulario.validate():
            
            try:
                modificaTablaSQL("UPDATE movimientos SET fecha =?, concepto =?, categoria=?, esGasto=?, cantidad=? WHERE id=?",[formulario.fecha.data, formulario.concepto.data, formulario.categoria.data, formulario.esGasto.data, formulario.cantidad.data, id])

            except sqlite3.Error as el_error:
                print("Error en SQL UPDATE", el_error)
                flash("Se ha producido un error en la base de datos. Pruebe en unos minutos", "error") #inyecta el mensaje en la plantilla 
                return render_template('modificar.html', form=formulario)

            flash("Modificación realizada con éxito", 'aviso')
            return redirect(url_for("index"))
        
        else:
            return render_template('modificar.html', form = formulario)

            

