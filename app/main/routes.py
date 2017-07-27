# from flask import session, redirect, url_for, render_template, request, jsonify
from flask import render_template, request, jsonify
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
    payload = json.loads(str(request.data, 'utf-8'))
    # print(payload)
    # print(type(payload))
    socketio.emit('message', {'msg':payload['lattice']}, namespace='/live')
    return jsonify({'success': True}), 200
