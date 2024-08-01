from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from config import Config
import pymysql # Para tratar exceções específicas

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
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users")
        users = cur.fetchall()
        cur.close()
        return render_template('read.html', users=users)
    except pymysql.MySQLError as e:
        flash(f"Erro ao conectar ao banco de dados: {e}", 'error')
        return render_template('read.html', users=[])


#/add: Rota para adicionar um novo usuário à tabela users.
@app.route('/add', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        try:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO users (nome, email) VALUES (%s, %s)", (nome, email))
            mysql.connection.commit()
            cur.close()
            flash("Usuário adicionado com sucesso!", 'success')
            return redirect(url_for('read'))
        except pymysql.MySQLError as e:
            flash(f"Erro ao adicionar usuário: {e}", 'error')
            return render_template('create.html')
    return render_template('create.html')


#/edit/<int:id>: Rota para editar um usuário existente.
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_user(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE id = %s", (id,))
        user = cur.fetchone()
        cur.close() 
        if request.method == 'POST':
            nome = request.form['nome']
            email = request.form['email']
            try:
                cur = mysql.connection.cursor()
                cur.execute("UPDATE users SET nome = %s, email = %s WHERE id = %s", (nome, email, id))
                mysql.connection.commit()
                cur.close()
                flash("Usuário atualizado com sucesso!", 'success')
                return redirect(url_for('read'))
            except pymysql.MySQLError as e:
                flash(f"Erro ao atualizar usuário: {e}", 'error')
                return render_template('update.html', user=user)        
        return render_template('update.html', user=user)
    except pymysql.MySQLError as e:
        flash(f"Erro ao recuperar dados do usuário: {e}", 'error')
        return redirect(url_for('read'))
    

#/delete/<int:id>: Rota para excluir um usuário da tabela users.
@app.route('/delete/<int:id>', methods=['POST'])
def delete_user(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM users WHERE id = %s", (id,))    
        mysql.connection.commit()
        cur.close()
        flash("Usuário excluído com sucesso!", 'seccess')
    except pymysql.MySQLError as e:
        flash(f"Erro ao excluir usuário: {e}", 'error')
    return redirect(url_for('read'))



if __name__ == '__main__':
    app.run(debug=True)