import secrets


from flask import Flask, render_template, request, redirect, url_for, session


app = Flask(__name__)
app.secret_key = secrets.token_hex()
@app.route ('/')
def index():
    return render_template('index.html')
@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session ['username'] = request.form.get('username','email')
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout/')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(port=5000, debug=False)