import os
from dotenv import load_dotenv


class Config(object):

    load_dotenv()
    SECRET_KEY = os.getenv('SECRET_KEY')
    FSA_API_URI = os.getenv('FSA_API_URI')
    ESTABLISHMENT_URI_PATH = os.getenv('ESTABLISHMENT_URI_PATH')