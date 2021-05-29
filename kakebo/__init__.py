from flask import Flask

app = Flask(__name__, instance_relative_config=True) #Creamos la aplicación, la configuracion la vamos a relaizar relativa a un fichero
app.config.from_object('config')

import kakebo.views

