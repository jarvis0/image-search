import os


ROOT: str = os.getenv('ROOT', default=os.getcwd())
HOST: str = os.getenv('HOST', default='localhost')
PORT: str = os.getenv('PORT', default='8080')
