from flask import Flask, render_template_string, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'

# Simple user store (in production, use a database)
users = {
    'admin': generate_password_hash('password'),
    'user': generate_password_hash('123456')
}


@app.route('/')
def hello_world():
    if 'username' not in session:
        return redirect(url_for('login'))

    return render_template_string('''
    <h1>hello world</h1>
    <p>Welcome, {{ username }}! <a href="{{ url_for('logout') }}">Logout</a></p>
    <iframe
        src="https://dbc-9ca0f5e0-2208.cloud.databricks.com/embed/dashboardsv3/01f04cbf0ad41ae79edb9da824a5feb7?o=2468881257868020"
        width="100%"
        height="90%"
        frameborder="0">
    </iframe>
    ''', username=session['username'])


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users and check_password_hash(users[username], password):
            session['username'] = username
            return redirect(url_for('hello_world'))
        else:
            flash('Invalid username or password')

    return render_template_string('''
    <h2>Login</h2>
    {% with messages = get_flashed_messages() %}
        {% if messages %}
            <ul>
            {% for message in messages %}
                <li style="color: red;">{{ message }}</li>
            {% endfor %}
            </ul>
        {% endif %}
    {% endwith %}
    <form method="post">
        <p>
            <label>Username:</label><br>
            <input type="text" name="username" required>
        </p>
        <p>
            <label>Password:</label><br>
            <input type="password" name="password" required>
        </p>
        <p>
            <input type="submit" value="Login">
        </p>
    </form>
    ''')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3030, debug=True)
