from app import app,reg_blueprints
from models import User
import logging.config 
from log_settings import logger_config
logging.config.dictConfig(logger_config)
debug_logger = logging.getLogger('debug_logger')
reg_blueprints(app)

if __name__ == '__main__':
	
	app.run(debug=True)