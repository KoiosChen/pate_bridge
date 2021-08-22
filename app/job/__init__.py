from flask import Blueprint

job = Blueprint('job', __name__)

from . import job_api
