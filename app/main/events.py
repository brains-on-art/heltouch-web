from flask import request
# from flask_socketio import emit, join_room, leave_room
from heltouch import app, socketio


@socketio.on('joined', namespace='/live')
def joined(message):
    """Sent by clients when they enter a room.
    Log it."""
    agent = request.headers.get('User-Agent')
    app.logger.info("JOIN {}".format(agent))


@socketio.on('message', namespace='/live')
def text(message):
    app.logger.info("MESSAGE {}".format(message))


@socketio.on('left', namespace='/live')
def left(message):
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    agent = request.headers.get('User-Agent')
    app.logger.info("LEFT {}".format(agent))
