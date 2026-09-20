from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField, DecimalField, SubmitField
from wtforms.validators import DataRequired, NumberRange


class FacturacionForm(FlaskForm):

    cliente = SelectField(
        "Cliente",
        coerce=int,
        validators=[
            DataRequired(
                message="Debe seleccionar un cliente."
            )
        ]
    )

    producto = SelectField(
        "Producto",
        coerce=int,
        validators=[
            DataRequired(
                message="Debe seleccionar un producto."
            )
        ]
    )

    cantidad = IntegerField(
        "Cantidad",
        validators=[
            DataRequired(
                message="La cantidad es obligatoria."
            ),
            NumberRange(
                min=1,
                message="La cantidad debe ser mayor que 0."
            )
        ]
    )

    precio = DecimalField(
        "Precio",
        validators=[
            DataRequired(
                message="El precio es obligatorio."
            ),
            NumberRange(
                min=0,
                message="El precio no puede ser negativo."
            )
        ],
        places=2
    )

    submit = SubmitField("Generar factura")