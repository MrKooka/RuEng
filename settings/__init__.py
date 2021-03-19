from flask import Blueprint

settings = Blueprint('settings',__name__,url_prefix='/rueng',template_folder='templates',static_folder='static')

