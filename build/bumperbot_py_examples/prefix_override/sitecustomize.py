import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/cxt13/bumperbot_ws/install/bumperbot_py_examples'
