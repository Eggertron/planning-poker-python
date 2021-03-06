# Planning Poker
#
# @author: Edgar Han
# @date: 11/12/2018
# @email: edgar.h.han@gmail.com

from flask import Flask, session, redirect, url_for, escape, request, render_template, Response, Markup, send_from_directory
from random import randint
import time # remove this for mutex
import json

# ==================================================================
# GLOBAL VARS
# ==================================================================

app = Flask(__name__)
# set the secret key.  keep this really secret:
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
data = {'index':0}

@app.route('/')
def hello_world():
    return redirect(url_for('login', room_id='1'))

@app.route('/login/<room_id>', methods=['GET', 'POST'])
def login(room_id='1'):
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
        if room_id:
            return redirect(url_for('show_room', room_id=room_id))
        else:
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
    print(data)
    if not room_id in data:
        return '{}, room {} does not exist, <a href="/create">Create New Room?</a>'.format(username, room_id)
    room_data = data[room_id]
    users_data = room_data['users']
    msg = room_data['msg']
    if not username in users_data:
        users_data[username] = {'vote':'-1'}
        data['index'] += 1
    user_data = users_data[username]
    if username == room_data['admin']:
        is_admin = username
    else:
        is_admin = None
    if request.method == 'POST':
        if 'vote' in request.form:
            form_response = request.form['vote']
            if form_response == 'True':
                room_data['hide_vote'] = True
            elif form_response == 'False':
                room_data['hide_vote'] = False
            elif form_response == 'Reset':
                room_data['hide_vote'] = True
                reset_users_data(users_data)
            else:
                user_data['vote'] = form_response
        if is_admin:
            msg = request.form['message']
            room_data['msg'] = msg
        data['index'] += 1
    if room_data['hide_vote']:
        users_data = hide_votes(users_data)
    stats = get_stats(users_data)
    return render_template('room.html', name=username, information=msg, board=stats, room_id=room_id, admin=is_admin)

def get_stats(users_data):
    result = ''
    for k,v in users_data.items():
        username = k
        vote = v['vote']
        if vote == '-1':
            vote = '?'
        result += '{} votes {} <br>'.format(username, vote)
    return Markup(result)

def reset_users_data(users_data):
    for name in users_data:
        user_data = users_data[name]
        user_data['vote'] = '-1'

@app.route('/create/', methods=['GET', 'POST'])
def create_room():
    if not 'username' in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        # create a new room and add creator as admin
        global data
        admin = session['username']
        while True:
            room_id = str(randint(1000,9999))
            if not room_id in data:
                break
        data[room_id] = {
                'admin':admin,
                'msg':'default message',
                'hide_vote':True,
                'users':{
                    admin:{
                        'vote':'-1'
                        }
                    }
                }
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

@app.route("/stream/<room_id>")
def stream(room_id=None):
    if not room_id:
        return
    def eventStream():
        print('streaming for room {}'.format(room_id))
        global data
        previous_index = data['index']
        room_data = data[room_id]
        while True:
            if data['index'] > previous_index:
                previous_index = data['index']
                hide_vote = room_data['hide_vote']
                users_data = room_data['users']
                room_data_pointer = room_data
                room_data = room_data.copy()
                if hide_vote:
                    hidden_users_data = hide_votes(users_data)
                    room_data['users'] = hidden_users_data
		else:
		    room_data['users'] = get_average(users_data)
                yield "data: {}\n\n".format(json.dumps(room_data))
                room_data = room_data_pointer
            time.sleep(0.2) # replace this with mutex
    return Response(eventStream(), mimetype="text/event-stream")

def hide_votes(users_data):
    results = {}
    for name in users_data:
        user_data = users_data[name]
        if user_data['vote'] == '-1':
            results[name] = {'vote':'not ready'}
        else:
            results[name] = {'vote':'hidden'}
    return results

def get_average(users_data):
    results = {}
    avg_count = 0
    avg_sum = 0
    for name in users_data:
        # copy the data to disposable dict
        user_data = users_data[name]
	vote = user_data['vote']
	results[name] = {'vote':vote}
	vote = int(vote)
	if vote > 0:
	    avg_count += 1
	    avg_sum += vote
    if avg_count != 0:
        avg = str(avg_sum / avg_count)
        results['average'] = {'vote':avg}
    return results
