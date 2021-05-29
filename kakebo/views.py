from kakebo import app
from flask import jsonify, render_template, request, redirect, url_for
from kakebo.forms import MovimientosForm
import sqlite3

def consultaSQL(query, parametros = []):
    # Abrimos conexion
    conexion = sqlite3.connect("movimientos.db") #para conectar (como un tubo) con la Base de Datos
    cur = conexion.cursor() #manejador de la base

    # Ejecutamos consulra

    cur.execute(query)

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


@app.route('/') #decoradores que rodean a funciones. de la instancia app. Ruta(METODO)---) recurso /
def index():

    conexion = sqlite3.connect("movimientos.db") #para conectar (como un tubo) con la Base de Datos
    cur = conexion.cursor() #manejador de la base

    cur.execute("SELECT * FROM movimientos;") #Acaba con un ; y ejecuta la consulta y lo devuelve
    
    claves= cur.description #tupla de tuplas
    filas = cur.fetchall() #lista de tuplas
    movimientos = []
    saldo = 0 #se compian con valor no con referencia
    for fila in filas:
        d = {}
        for tclave, valor in zip(claves, fila):
            d[tclave[0]] = valor
            print(d)
        if d['esGasto'] == 0:
            saldo = saldo + d['cantidad']
        else:
            saldo = saldo - d['cantidad']
        d['saldo'] = saldo
        movimientos.append(d) #crea la clave saldo
    conexion.close()
    return render_template('movimientos.html', datos = movimientos)

@app.route('/nuevo', methods=['GET', 'POST'])
def nuevo():
    formulario = MovimientosForm()

    if request.method == 'GET':
        return render_template('alta.html', form = formulario)
    else:
        if formulario.validate():
            conexion = sqlite3.connect("movimientos.db") 
            cur = conexion.cursor() 

            query = """ 
                INSERT INTO movimientos (fecha, concepto, categoria, esGasto, cantidad)
                VALUES (?, ?, ?, ?, ?)
            """
            try:
                cur.execute(query, [formulario.fecha.data, formulario.concepto.data,
                                formulario.categoria.data, formulario.esGasto.data, formulario.cantidad.data])
            except sqlite3.Error as el_error:
                print("Error SQL insert", el_error)
                return render_template('alta.html', form=formulario)
            
            conexion.commit() #el cambio realizado lo fija en la base de datos 
            conexion.close()

            return redirect(url_for("index"))

        else:
            return render_template('alta.html', form = formulario)

    