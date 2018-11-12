# Planning Poker
#
# @author: Edgar Han
# @date: 11/12/2018
# @email: edgar.h.han@gmail.com

from flask import Flask, session, redirect, url_for, escape, request, render_template
from random import randint

# ==================================================================
# GLOBAL VARS
# ==================================================================

app = Flask(__name__)
# set the secret key.  keep this really secret:
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
data = {}

@app.route('/')
def hello_world():
    return 'Hello World'

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id

@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /path/
    return 'Subpath %s' % subpath

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)

@app.route('/room/')
def no_room():
    return 'Do you want to create a room? <a href="/create">click here</a>'

@app.route('/room/<room_id>', methods=['GET', 'POST'])
def show_room(room_id=None):
    username = ''
    if request.method == 'POST':
        username = request.form['username']
        session['username'] = username
    elif 'username' in session:
        username = session['username']
    else:
        return render_template('join.html')
    global data
    if not room_id in data:
        return 'room %s does not exist' % room_id
    room_data = data[room_id]
    if not username in room_data:
        room_data[username] = {'vote':-1}
    user_data = room_data[username]
    msg = room_data['msg']
    return render_template('room.html', name=username, information=msg)

@app.route('/create', methods=['GET', 'POST'])
def create_room():
    if request.method == 'POST':
        # create a new room and add creator as admin
        admin = request.form['username']
        room_id = str(randint(1000,9999))
        global data
        data[room_id] = {'admin':admin, 'msg':'default message'}
        return 'hello {} your room number is <a href="/room/{}">{}</a>'.format(admin, room_id, room_id)
    else:
        return render_template('create_room.html')

@app.route('/reset')
def reset_data():
    global data
    data = {}
    return 'Data has been reset'

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('show_room'))
