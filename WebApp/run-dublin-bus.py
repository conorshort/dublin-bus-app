""" I made this because I find it slightly annoying to start the server by
typing 'python manage.py runserver'. This python file can be run instead """

import os
os.system("python WebApp\manage.py runserver 0.0.0.0:8000")
