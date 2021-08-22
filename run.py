#!/usr/bin/env python
import os
import multiprocessing
from app import create_app

__author__ = 'jinzhang.chen'

app = create_app(os.getenv('FLASK_CONFIG') or 'development')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=22222, debug=False)
