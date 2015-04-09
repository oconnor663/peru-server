import os
import sys

peru_server_root = os.path.abspath(os.path.dirname(__file__))

# activate virtualenv
activate_this = os.path.join(peru_server_root, '../bin/activate_this.py')
exec(open(activate_this).read())

# prepend our project import path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from server import app as application
