from kakebo import app

@app.route('/') #decoradores que rodean a funciones. de la instancia app. Ruta(METODO)---) recurso /
def index():
    return 'Flask rulando'