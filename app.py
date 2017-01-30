import sqlite3 as lite
from flask import Flask, render_template, request, url_for, redirect, session

app = Flask(__name__)

@app.route("/")
def main():
    if 'username' in session:
        username_session = session['username']
        # return render_template('index_login.html', session_user_name=username_session)
        con = lite.connect('app1.db')
        cur = con.cursor()
        cur.execute("SELECT first_name from Users where username = (?)", username_session)
        # firstname_session = session['first_name']
        return render_template('index_login.html', session_first_name=['first_name'])
    else:
        return render_template('index.html')

@app.route("/showSignUp")
def showSignUp():
  return render_template('signup.html')

@app.route('/saveuser', methods=['GET','POST'])
def save_user():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        gender = request.form['gender']

        con = lite.connect('app1.db')

        with con:
            cur = con.cursor()
            cur.execute("INSERT INTO Users (first_name,last_name,gender,email,username,password) VALUES (?,?,?,?,?,?)",(firstname,lastname,gender,email,username,password))
            con.commit()

    return redirect(url_for('userlist'))

@app.route("/showsignin")
def showsignin():
  return render_template("login.html")

@app.route('/signin', methods=['GET','POST'])
def signin():
    con = lite.connect("app1.db")
    con.row_factory = lite.Row

    cur = con.cursor()

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cur.execute("select * from Users where username=(?)",[username])

        rows = cur.fetchall();
        con.close()

        if password==rows[password]:
            return "Login Sukses"
        else:
            return "Login Gagal"

@app.route('/goSignIn/', methods=['GET','POST'])
def goSignIn():
    error = ""
    if request.method == 'POST':
        username_form = request.form['username']
        password_form = request.form['password']

        con = lite.connect('app1.db')
        cur = con.cursor()
        cur.execute("SELECT count(1) from Users where username = (?)", [username_form])
        if cur.fetchone()[0]:
            cur.execute("SELECT password from Users where username = (?)", [username_form])
            for row in cur.fetchall():
                if password_form == row[0]:
                    session['username']=request.form['username']

                    return redirect(url_for('main'))
                else:
                    error = "Invalid Credential - Error Password"
        else:
            error = "Invalid Credential - Error Username"
    return render_template('login.html',error=error)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('main'))

@app.route('/carlist')
def carlist():
    con = lite.connect("app1.db")
    con.row_factory = lite.Row

    cur = con.cursor()
    cur.execute("select * from Cars")

    rows = cur.fetchall();
    con.close()
    return render_template("car_list.html",rows = rows)

@app.route('/userlist')
def userlist():
    con = lite.connect("app1.db")
    con.row_factory = lite.Row

    cur = con.cursor()
    cur.execute("select * from Users")

    rows = cur.fetchall();
    con.close()
    return render_template("user_list.html",rows = rows)

@app.route('/insertcar')
def insertcar():
    return render_template("insertcar.html")

@app.route('/savecar', methods=['GET','POST'])
def savecar():
    if request.method == 'POST':
        idcar = request.form['txt_idcar']
        namecar = request.form['txt_namecar']
        pricecar = request.form['txt_pricecar']

        con = lite.connect('app1.db')

        with con:
            cur = con.cursor()
            cur.execute("INSERT INTO Cars VALUES (?,?,?)",(idcar,namecar,pricecar))
            con.commit()

    return redirect(url_for('carlist'))

@app.route('/showupdatecar')
def showupdatecar():
    con = lite.connect("app1.db")
    con.row_factory = lite.Row

    cur = con.cursor()
    cur.execute("select Id from Cars")

    rows = cur.fetchall();
    con.close()
    return render_template("updatecar.html",rows = rows)

@app.route('/updatecar', methods=['GET','POST'])
def updatecar():
    if request.method == 'POST':
        idcar = request.form['id']
        namecar = request.form['namecar']
        pricecar = request.form['price']

        con = lite.connect('app1.db')

        with con:
            cur = con.cursor()
            # cur.execute("UPDATE Cars SET (?,?) where ",(namecar,pricecar))
            cur.execute("UPDATE Cars SET Name = ?,Price = ? WHERE Id= ?",(namecar,pricecar,idcar))
            con.commit()

    return redirect(url_for('carlist'))

@app.route('/showdeletecar')
def showdeletecar():
    con = lite.connect("app1.db")
    con.row_factory = lite.Row

    cur = con.cursor()
    cur.execute("select Id from Cars")

    rows = cur.fetchall();
    con.close()
    return render_template("deletecar.html",rows = rows)

@app.route('/deletecar', methods=['GET','POST'])
def deletecar():
    if request.method == 'POST':
        idcar = request.form['id']

        con = lite.connect('app1.db')

        with con:
            cur = con.cursor()
            cur.execute("DELETE FROM Cars WHERE Id = ?",(idcar,))
            con.commit()

    return redirect(url_for('carlist'))

@app.route('/carlist_delete/<int:idcar>', methods=['GET','POST'])
def carlist_delete(idcar):
    try:
        idcar = str(idcar)
        con = lite.connect('app1.db')
        cur = con.cursor()

        with con:
            cur = con.cursor()
            cur.execute("DELETE FROM Cars WHERE Id = ?",(idcar,))
            con.commit()
            return redirect(url_for('carlist'))

    except:
        return redirect(url_for('carlist'))

app.secret_key = 'baksosolo'
if __name__ == "__main__":
  app.run(debug="True")
