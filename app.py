# app.py

"""Main application and routing logic for Vaccine R&D Dash API."""
from flask import Flask, json, jsonify, request
from flask_cors import CORS
from werkzeug.exceptions import HTTPException
from decouple import config
import os

from api.routes.image_route import fetch_images
from flask import send_file


# Logging
import logging

def create_app(test_config=None):
    """
    Creates app
    """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        # Make sure to change debug to False in production env
        DEBUG=config('DEBUG', default=False),
        SECRET_KEY=config('SECRET_KEY', default='dev'),  # CHANGE THIS!!!!
        LOGFILE=config('LOGFILE', os.path.join(
            app.instance_path, 'logs/debug.log')),
        CACHE_TYPE=config('CACHE_TYPE', 'simple'),  # Configure caching
        # Long cache times probably ok for ML api
        CACHE_DEFAULT_TIMEOUT=config('CACHE_DEFAULT_TIMEOUT', 300),
        TESTING=config('TESTING', default='TRUE'),
    )

    # Enable CORS header support
    CORS(app)

    ##############
    ### Routes ###
    ##############
    @app.route('/', methods=['GET'])
    def home():
        return "This is an example app"


    @app.route('/image/<sid>', methods=['GET'])
    def get_image(sid: str = None, num_img: int = 1):
        if sid is None:
            raise HTTPException(400, 'Bad Request.  Must submit valid SID')
        return send_file(
            fetch_images(sid, num_img),
            mimetype='image/png')



    #############
    ###Logging###
    #############
    # Change logging.INFO to logging.DEBUG to get full logs.  Will be a crapload of information.
    # May significantly impair performance if writing logfile to disk (or network drive).
    # To enable different services, see README.md
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers.extend(gunicorn_logger.handlers)
    app.logger.setLevel(gunicorn_logger.level)
    app.logger.info('Application logging Set')

    # File logging. Remove in PROD
    if app.config['TESTING'] == 'TRUE':
        app.logger.info('Using TESTING log config.')
        logging.basicConfig(
            filename=app.config['LOGFILE'], 
            level=logging.INFO, 
            format='[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S %z')
    
    logging.getLogger('flask_cors').level = logging.INFO

    # Register database functions.  Will allow db.close() to run on teardown
    from db import db
    db.init_db()
    app.logger.info('Database functionality initialized.  Click commands available.')

    return app
