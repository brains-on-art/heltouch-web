# from flask import session, redirect, url_for, render_template, request, jsonify
from flask import render_template, request, jsonify, current_app
from . import main
from .. import socketio, img_tasks
import json
import time


@main.route('/')
def index():
    """Page that concatenates incoming messages"""
    # name = session.get('name', '')
    # room = session.get('room', '')
    # if name == '' or room == '':
    #     return redirect(url_for('.index'))
    return render_template('messages.html')

@main.route('/image', methods=['POST'])
def image():
    """Accept an image as a POST"""
    if request.files.get('image'):
        fname = 'images/{}.jpg'.format(str(time.time()))
        request.files['image'].save(fname)
        result = img_tasks.read_img_detect_circles(fname)
        print(result)
        current_app.logger.info("POST {}".format(result))
        return jsonify({'success': True}), 200
    else:
        current_app.logger.warning("IMAGE POST FAILED")
        return jsonify({'success': False}), 400


@main.route('/lattice', methods=['POST'])
def lattice():
    try:
        payload = json.loads(str(request.data, 'utf-8'))
        msg = payload.get('lattice')
        socketio.emit('message', {'msg':msg}, namespace='/live', include_self=True)
        current_app.logger.info("MESSAGE {}".format(msg))
        return jsonify({'success': True}), 200
    except Exception as e:
        current_app.logger.warning("FAILED POST")
        return jsonify({'success': False}), 400
