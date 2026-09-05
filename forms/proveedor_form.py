from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class ProveedorForm(FlaskForm):

    empresa = StringField(
        "Empresa",
        validators=[
            DataRequired(message="La empresa es obligatoria."),
            Length(
                min=2,
                max=100,
                message="La empresa debe tener entre 2 y 100 caracteres."
            )
        ]
    )

    contacto = StringField(
        "Persona de contacto",
        validators=[
            DataRequired(message="El contacto es obligatorio."),
            Length(
                min=3,
                max=100,
                message="El contacto debe tener entre 3 y 100 caracteres."
            )
        ]
    )

    telefono = StringField(
        "Teléfono",
        validators=[
            DataRequired(message="El teléfono es obligatorio."),
            Length(
                min=7,
                max=15,
                message="El teléfono debe tener entre 7 y 15 caracteres."
            )
        ]
    )

    producto = StringField(
        "Producto",
        validators=[
            DataRequired(message="El producto es obligatorio."),
            Length(
                min=2,
                max=100,
                message="El producto debe tener entre 2 y 100 caracteres."
            )
        ]
    )

    submit = SubmitField("Guardar proveedor")