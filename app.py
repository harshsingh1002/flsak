from flask import Flask  , render_template , request , session  , url_for , logging , redirect
from sqlalchemy.orm import scoped_session ,  sessionmaker
from sqlalchemy import create_engine
from passlib.hash import sha256_crypt

engine = create_engine('mysql+pysql://root:redhat@localhost/registerdb')
db = scoped_session(sessionmaker(bind=engine))

app = Flask(__name__)



@app.route('/')
def home():
    return render_template("home.html")

##register route
@app.route('/register' , methods=["GET","POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        username = request.form.get("username")
        password = request.form.get("password")
        confirm = request.form.get("confirm")
        secure_password = sha256_crypt.encrypt(str(password))

        if password == confirm:
            db.execute("INSERT INTO public.users(name,username,password) VALUES(name, username, password)",
                       {"name":name , "username":username , "password":secure_password});
            db.commit()
            return redirect(url_for('login'))
        else:

            return render_template("register.html")


    return render_template("register.html")


##login route
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")

        usernamedata= db.execute(" SELECT username FROM users WHERE username=:username" , {"username":username}).fetchone()
        passwordata = db.execute(" SELECT password FROM users WHERE username=:username",
                                  {"username": username}).fetchone()

        if usernamedata is None :
            return render_template('login.html')
        else:
            for pass_data in passwordata:
                if sha256_crypt.verify(password,passwordata):
                    session["log"] = True

                    return redirect(url_for('success_login'))
                else:
                    return render_template('login.html')

    return render_template("login.html")

@app.route('/success_login')
def pic():
    return render_template("success_login.html")

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ =="__main__":
    app.secret_key = "123456qwerty"
    app.run(debug=True,port=5000)



