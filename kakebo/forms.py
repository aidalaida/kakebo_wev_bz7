from flask_wtf import FlaskForm
from wtforms import DateField
from wtforms.fields.core import BooleanField, SelectField, StringField, FloatField
from wtforms.fields.simple import SubmitField #clase que se convierte en campo de tipo fecha
from wtforms.validators import DataRequired, Length, ValidationError #clase
from datetime import date

def fecha_por_debajo_de_hoy(formulario, campo): #para validar fechas, instancia del formulrio y el campo
    hoy = date.today()
    if campo.data > hoy:
        raise ValidationError('La fecha no puede ser mayor que hoy') #lanzando una excepcion propia de WTF




class MovimientosForm(FlaskForm):
    fecha = DateField("Fecha", validators = [DataRequired(message="Debe informar una fecha válida"), fecha_por_debajo_de_hoy]) #etiqueta que queremos que tenga el campo + validadores
    concepto = StringField("Concepto", validators = [DataRequired(), Length(min=10)])
    categoria = SelectField("Categoria", choices=[('00', ''),('SU', 'Supervivencia'), ('OV', 'Ocio/Vicio'),
                            ('CU', 'Cultura'), ('EX', 'Extras')])
    cantidad = FloatField("Cantidad", validators = [DataRequired()])
    esGasto = BooleanField("Es gasto")
    submit = SubmitField('Aceptar')

