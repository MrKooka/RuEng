from app import *
from rueng.models import *

manager = app.migrate()

if __name__ == '__main__':
	manager.run()