# Planning Poker
#
# @author: Edgar Han
# @date: 11/12/2018
# @email: edgar.h.han@gmail.com

from flask import Flask
from flask import render_template

# ==================================================================
# GLOBAL VARS
# ==================================================================

app = Flask(__name__)
data = {'123':'456'}

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
    return 'room %s does not exist' % room_id
