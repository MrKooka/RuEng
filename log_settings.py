import logging
from pprint import pprint
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
session = requests.Session()
retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)
class BotDebugsHandler(logging.Handler):
    def __init__(self):
        logging.Handler.__init__(self)

    def emit(self,record):

        message = self.format(record)
        token = ''
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        data = {"chat_id": '-1001182116382,',"text": message}
        session.get(url,data=data)


class BotErrorsHandler(logging.Handler):
    def __init__(self):
        logging.Handler.__init__(self)

    def emit(self,record):
        message = self.format(record)
        token = ''
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        data = {"chat_id": '-1001290697961,',"text": message}
        session.get(url,data=data)

logger_config = {
	'version':1,
	'disable_existing_loggers':False,
	'formatters': {
		'std_format':{
			'format':'{asctime} - {levelname} - {name}- {pathname}:{module}:{funcName}:{lineno} - {message}',
			'style': '{'
		}
	},
	'handlers': {
		'consol_hand': {
			'class': 'logging.StreamHandler',
			'level': 'NOTSET',
			'formatter': 'std_format', 
		},
		'bot_debug_handlers': {
			'()':BotDebugsHandler,
			'level':'DEBUG',
			'formatter':'std_format',
		},
		'bot_errors_handlers':{
			'()':BotErrorsHandler,
			'level':'WARNING',
			'formatter':'std_format'

		},		
		'file':{
			'class':'logging.FileHandler',
			'level':'ERROR',
			'filename':'debug.log',
			'formatter':'std_format'

		}
	},
	'loggers': {
		'notset_logger':{
			'level':'INFO',
			'handlers':['consol_hand','bot_debug_handlers']
		},
		'debug_logger':{
			'level':'DEBUG',
			'handlers':['consol_hand','bot_debug_handlers']
		},
		
		'info_logger':{
			'level':'INFO',
			'handlers':['consol_hand','bot_debug_handlers']
		},
		'warning_logger': {
			'level':'WARNING',
			'handlers': ['consol_hand','bot_errors_handlers'],
			# 'propagate': False
		},
		'error_logger':{
			'level':'ERROR',
			'handlers':['file','bot_errors_handlers']
		},
		'critical_logger':{
			'level':'CRITICAL',
			'handlers':['file','bot_errors_handlers']
		}

	},
	
	# 'root': {},# '':{} 
 	# 'incremental':True
}



