# from flask import session, redirect, url_for, render_template, request, jsonify
from flask import render_template, request, jsonify, current_app
from . import main
from .. import socketio
import json


@main.route('/')
def index():
    """Page that concatenates incoming messages"""
    # name = session.get('name', '')
    # room = session.get('room', '')
    # if name == '' or room == '':
    #     return redirect(url_for('.index'))
    return render_template('messages.html')


@main.route('/lattice', methods=['POST'])
def lattice():
    """Accept a lattice as a POST"""
    print(request.files)
    try:
        payload = json.loads(str(request.data, 'utf-8'))
        msg = payload.get('lattice')
        socketio.emit('message', {'msg':msg}, namespace='/live', include_self=True)
        current_app.logger.info("MESSAGE {}".format(msg))
        return jsonify({'success': True}), 200
    except Exception as e:
        current_app.logger.warning("FAILED POST")
        return jsonify({'success': False}), 400
