from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class EditUserForm(FlaskForm):
    nome = StringField('Nome', validators=[
        DataRequired(message="O nome é obrigatório."),
        Length(max=100, message="O nome deve conter no máximo 100 caracteres.")
    ])
    email = EmailField('Email', validators=[
        DataRequired(message="O e-mail é obrigatório."),
        Email(message="Formato de e-mail inválido.")
    ])
    submit = SubmitField('Editar')


class CreateUserForm(FlaskForm):
    nome = StringField('Nome', validators=[
        DataRequired(message="O nome é obrigatório."),
        Length(max=100, message="O nome deve conter no máximo 100 caracteres.")
    ])
    email = EmailField('Email', validators=[
        DataRequired(message="O e-mail é obrigatório."),
        Email(message="Formato de e-mail inválido.")
        ])
    submit = SubmitField('Cadastrar')