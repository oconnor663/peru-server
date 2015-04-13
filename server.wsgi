import logging
import os
import sys


# make sure errors go to stderr where they can get logged
logging.basicConfig(stream=sys.stderr)

peru_server_root = os.path.abspath(os.path.dirname(__file__))

# activate virtualenv
activate_this = os.path.join(peru_server_root, '../bin/activate_this.py')
exec(open(activate_this).read())

# prepend our project import path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import server

server.DB_PATH = '/srv/peru-server-data/peru-server.sqlite3'
application = server.app
