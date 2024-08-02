from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from config import Config
import pymysql # Para tratar exceções específicas
from forms import CreateUserForm, EditUserForm


#Cria uma instância da aplicação Flask.
app = Flask(__name__)

#Carrega a configuração do banco de dados e outras configurações do arquivo config.py.
app.config.from_object(Config)

#Inicializa a extensão MySQL para Flask
mysql = MySQL(app)


#/: Rota para ler e exibir todos os usuários da tabela users.
@app.route('/')
def read():
    try:
        with mysql.connection.cursor() as cur:
            cur.execute("SELECT * FROM users")
            users = cur.fetchall()
        flash("Usuários listados com sucesso!", 'success')
        return render_template('read.html', users=users)
    except pymysql.MySQLError as e:
        flash(f"Erro ao conectar ao banco de dados: {e}", 'error')
        return render_template('read.html', users=[])


#/add: Rota para adicionar um novo usuário à tabela users.
@app.route('/add', methods=['GET', 'POST'])
def add_user():

    form = CreateUserForm()

    if form.validate_on_submit():
        nome = form.nome.data
        email = form.email.data
        try:
            with mysql.connection.cursor() as cur:
                cur.execute("INSERT INTO users (nome, email) VALUES (%s, %s)", (nome, email))
                mysql.connection.commit()
            flash("Usuário adicionado com sucesso!", 'success')
            return redirect(url_for('read'))
        except pymysql.MySQLError as e:
            flash(f"Erro ao adicionar usuário: {e}", 'error')
    return render_template('create.html', form=form)


#/edit/<int:id>: Rota para editar um usuário existente.
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_user(id):

    form = EditUserForm()

    if request.method == 'POST' and form.validate_on_submit():
        nome = form.nome.data
        email = form.email.data

        try:
            with mysql.connection.cursor() as cur:
                cur.execute("UPDATE users SET nome = %s, email = %s WHERE id = %s", (nome, email, id))
                mysql.connection.commit()
            flash("Usuário atualizado com sucesso!", 'success')
            return redirect(url_for('read'))
        except pymysql.MySQLError as e:
            flash(f"Erro ao atualizar usuário: {e}", 'error')
    
    try:
        with mysql.connection.cursor() as cur:
            cur.execute("SELECT * FROM users WHERE id = %s", (id,))
            user = cur.fetchone()
        if user:
            form.nome.data = user[1]
            form.email.data = user[2]
        else:
            flash("Usuário não encontrado!", 'error')
            return redirect(url_for('read'))
    except pymysql.MySQLError as e:
        flash(f"Erro ao recuperar dados do usuário: {e}", 'error')
        return redirect(url_for('read'))
    
    return render_template('update.html', form=form)
    

#/delete/<int:id>: Rota para excluir um usuário da tabela users.
@app.route('/delete/<int:id>', methods=['POST'])
def delete_user(id):
    try:
        with mysql.connection.cursor() as cur:
            cur.execute("DELETE FROM users WHERE id = %s", (id,))    
            mysql.connection.commit()
        flash("Usuário excluído com sucesso!", 'success')
    except pymysql.MySQLError as e:
        flash(f"Erro ao excluir usuário: {e}", 'error')
    return redirect(url_for('read'))



if __name__ == '__main__':
    app.run(debug=True)