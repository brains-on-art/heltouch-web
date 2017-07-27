#!/bin/env python
from app import create_app, socketio
import logging
import settings

app = create_app(debug=settings.DEBUG)

if __name__ == '__main__':
    handler = logging.FileHandler('heltouch.log', encoding='utf-8')
    handler.setLevel(logging.DEBUG)
    app.logger.addHandler(handler)
    socketio.run(app)
