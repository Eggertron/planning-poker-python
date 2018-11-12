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
data = {'123':1}

@app.route('/')
def hello_world():
    return 'Hello World'

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % username

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
@app.route('/room/<room_id>')
def show_room(room_id=None):
    global data
    print(data)
    if not room_id in data:
        return 'room %s does not exist' % room_id
    data[room_id] = data[room_id] + 1
    return 'current number is %d' % data[room_id]

@app.route('/create', methods=['GET', 'POST'])
def create_room():
    if request.method == 'POST':
        # create a new room and add creator as admin
        room_id = str(randint(1000,9999))
        global data
        data[room_id] = 0
        return 'hello {} your room number is <a href="/room/{}">{}</a>'.format(request.form['username'], room_id, room_id)
    else:
        return render_template('create_room.html')
