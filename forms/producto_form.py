from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange


class ProductoForm(FlaskForm):

    nombre = StringField(
        "Nombre del producto",
        validators=[
            DataRequired(
                message="El nombre es obligatorio."
            ),
            Length(
                min=3,
                max=100,
                message="El nombre debe tener entre 3 y 100 caracteres."
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

    stock = IntegerField(
        "Stock",
        validators=[
            DataRequired(
                message="El stock es obligatorio."
            ),
            NumberRange(
                min=0,
                message="El stock no puede ser negativo."
            )
        ]
    )

    id_proveedor = SelectField(
        "Proveedor",
        coerce=int,
        validators=[
            DataRequired(
                message="Debe seleccionar un proveedor."
            )
        ]
    )

    submit = SubmitField("Guardar producto")