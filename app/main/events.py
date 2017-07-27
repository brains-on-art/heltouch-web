from flask import request, current_app
# from flask_socketio import emit, join_room, leave_room
from .. import socketio


@socketio.on('joined', namespace='/live')
def joined(message):
    """Sent by clients when they enter a room.
    Log it."""
    agent = request.headers.get('User-Agent')
    current_app.logger.info("JOIN {}".format(agent))


@socketio.on('left', namespace='/live')
def left(message):
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    agent = request.headers.get('User-Agent')
    current_app.logger.WARNING("LEFT {}".format(agent))
