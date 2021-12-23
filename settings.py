import os
from dotenv import load_dotenv


load_dotenv()

TOKEN_USER = os.getenv('TOKEN_USER')
TOKEN_GROUP = os.getenv('TOKEN_GROUP')
DSN = os.getenv('DSN')
