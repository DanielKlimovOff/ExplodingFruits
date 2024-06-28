from flask import Flask, render_template, request, make_response
import sqlite3
import random


app = Flask(__name__)


@app.route('/')
def main():
    session_key = request.cookies.get("session_key")
    if not session_key:
        return render_template('enter.html')

    connection = sqlite3.connect('server.db')
    cursor = connection.cursor()
    cursor.execute(f'select count(*) from sessions where key="{session_key}";')
    is_session_exist = cursor.fetchone()[0]
    connection.commit()
    connection.close()

    if not is_session_exist:
        response = make_response(render_template('enter.html'))
        response.set_cookie('session_key', '', expires=0)
        return response
    
    connection = sqlite3.connect('server.db')
    cursor = connection.cursor()
    cursor.execute(f'select user from sessions where key="{session_key}";')
    user_id = cursor.fetchone()[0]
    cursor.execute(f'select login from users where id={user_id};')
    login = cursor.fetchone()[0]
    connection.commit()
    connection.close()

    response = make_response('', 301)
    response.headers['Location'] = 'home'
    return response

@app.get('/login')
def login_get():
    return render_template('login.html')

@app.post('/login')
def login_post():
    login = request.form['login']
    password = request.form['password']

    connection = sqlite3.connect('server.db')
    cursor = connection.cursor()
    cursor.execute(f'select count(*) from users where login="{login}" and password="{password}";')
    is_user_exist = cursor.fetchone()[0]
    connection.commit()
    connection.close()

    if not is_user_exist:
        return render_template('error.html', text='Войти в аккаунт не удалось. Ошибка в логине или пароле.', link='/login')

    session_key = format(random.getrandbits(128), 'x')

    connection = sqlite3.connect('server.db')
    cursor = connection.cursor()
    cursor.execute(f'select id from users where login="{login}" and password="{password}";')
    user_id = cursor.fetchone()[0]
    cursor.execute(f'delete from sessions where user={user_id};')
    cursor.execute(f'insert into sessions values ("{session_key}", {user_id});')
    connection.commit()
    connection.close()

    response = make_response('', 301)
    response.headers['Location'] = 'home'
    response.set_cookie('session_key', session_key, max_age=60*60)
    return response

@app.get('/home')
def home():
    session_key = request.cookies.get("session_key")
    if not session_key:
        response = make_response('', 301)
        response.headers['Location'] = '/'
        return response

    connection = sqlite3.connect('server.db')
    cursor = connection.cursor()
    cursor.execute(f'select count(*) from sessions where key="{session_key}";')
    is_session_exist = cursor.fetchone()[0]
    connection.commit()
    connection.close()

    if not is_session_exist:
        response = make_response('', 301)
        response.headers['Location'] = '/'
        response.set_cookie('session_key', '', expires=0)
        return response
    
    connection = sqlite3.connect('server.db')
    cursor = connection.cursor()
    cursor.execute(f'select user from sessions where key="{session_key}";')
    user_id = cursor.fetchone()[0]
    cursor.execute(f'select login from users where id={user_id};')
    login = cursor.fetchone()[0]
    connection.commit()
    connection.close()

    return render_template('home.html', login=login)

@app.get('/logout')
def logout():
    print('logout')
    session_key = request.cookies.get("session_key")

    connection = sqlite3.connect('server.db')
    cursor = connection.cursor()
    cursor.execute(f'delete from sessions where key="{session_key}";')
    connection.commit()
    connection.close()

    response = make_response(render_template('message.html', text='Успешно вышли из аккаунта.', link='/'))
    response.set_cookie('session_key', '', expires=0)
    return response

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=4000)
