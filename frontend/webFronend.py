from flask import Flask, render_template, redirect, url_for

app = Flask(__name__, template_folder="front",static_folder="front/imagenes")

@app.route('/')
def redirigir_a_login():
    return redirect(url_for('login'))
@app.route('/login', methods=['GET'])
def login():
    return render_template('loginBD.html')
@app.route('/admin', methods=['GET'])
def admin():
    return render_template('crudAdmin.html')

@app.route('/user', methods=['GET'])
def user():
    return render_template('homeUsuario.html')

@app.route('/verificacion', methods=['GET'])
def verificacion2FA():
    return render_template('autenticacionGoogle.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 
