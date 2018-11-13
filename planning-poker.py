# Planning Poker
#
# @author: Edgar Han
# @date: 11/12/2018
# @email: edgar.h.han@gmail.com

from flask import Flask, session, redirect, url_for, escape, request, render_template, Response
from random import randint

# ==================================================================
# GLOBAL VARS
# ==================================================================

app = Flask(__name__)
# set the secret key.  keep this really secret:
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
#app.add_url_rule('/favicon.ico', redirect_to=url_for('static', filename='favicon.jpg'))
data = {'index':0}

@app.route('/')
def hello_world():
    return 'Hello World'

@app.route('/login/', methods=['GET', 'POST'])
@app.route('/login/<room_id>', methods=['GET', 'POST'])
def login(room_id=None, methods=['GET', 'POST']):
    if not 'username' in session:
        if request.method == 'POST':
            username = request.form['username']
            session['username'] = username
            if room_id:
                return redirect(url_for('show_room', room_id=room_id))
        else:
            return render_template('join.html')
    else:
        username = session['username']
    return 'You are logged in as {}'.format(username)

@app.route('/room/')
def no_room():
    return 'Do you want to create a room? <a href="/create">click here</a>'

@app.route('/room/<room_id>', methods=['GET', 'POST'])
def show_room(room_id=None):
    if not 'username' in session:
        return redirect(url_for('login', room_id=room_id))
    username = session['username']
    global data
    if not room_id in data:
        return 'room %s does not exist' % room_id
    room_data = data[room_id]
    if not username in room_data:
        room_data[username] = {'vote':-1}
    user_data = room_data[username]
    msg = room_data['msg']
    if request.method == 'POST':
        user_data['vote'] = request.form['vote']
        data['index'] += 1
    stats = get_stats(room_data)
    return render_template('room.html', name=username, information=msg, board=stats)

def get_stats(room_data):
    result = ''
    for k,v in room_data.items():
        if not (
                k == 'msg'
                or k == 'admin'
                or k == 'index'
                ):
            username = k
            vote = v['vote']
            if vote == '-1':
                vote = '?'
            result += '{} votes {}\n'.format(username, vote)
    return result

@app.route('/create/', methods=['GET', 'POST'])
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

@app.route('/reset/')
def reset_data():
    global data
    data = {}
    return 'Data has been reset'

@app.route('/logout/')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route("/stream")
def stream():
    def eventStream():
        global data
        previous_index = data['index']
        while True:
            if data['index'] > previous_index:
                previous_index = data['index']
                yield "data: {}\n\n".format(data)
    return Response(eventStream(), mimetype="text/event-stream")
