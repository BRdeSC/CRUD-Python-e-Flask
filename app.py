from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

mysql = MySQL(app)

@app.route('/')
def read():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users")
    users = cur.fetchall()
    cur.close()
    return render_template('read.html', users=users)


@app.route('/add', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (nome, email) VALUES (%s, %s)", (nome, email))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('read'))
    return render_template('create.html')


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_user(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE id = %s", (id,))
    user = cur.fetchone()
    cur.close()
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute("UPDATE users SET nome = %s, email = %s WHERE id = %s", (nome, email, id))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('read'))
    return render_template('update.html', user=user)


@app.route('/delete/<int:id>', methods=['POST'])
def delete_user(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM users WHERE id = %s", (id,))    
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('read'))



if __name__ == '__main__':
    app.run(debug=True)