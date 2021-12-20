import os
os.system("gunicorn -w 4 name:app")
