from starlette.config import Config

try:
    config = Config(".env")
except FileNotFoundError:
    config = Config()

DATA_BASE_URL = config("DATA_BASE_URL" , cast=str)
TEST_DATA_BASE_URL = config("TEST_DATA_BASE_URL" , cast=str)
SECRET_KEY= config("SECRET_KEY" , cast=str)
ALGORITHM = config("ALGORITHM" , cast=str)
OPENAI_API_KEY= config("OPENAI_API_KEY" , cast=str)