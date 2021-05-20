from flask import Flask #Importamos la instancia de la clase flask, y será nuestra aplicación flask, metiendo todo

app = Flask(__name__) #Crear una instancia de Flask (contenedor) con NAME que es un identificador

@app.route('/') #decoradores que rodean a funciones. de la instancia app. Ruta(METODO)---) recurso /
def index():
    return 'Hola, mundo!'

@app.route('/adios')
def bye():
    return 'Hasta luego, cocodrilo'

    