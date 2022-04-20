from pydantic import BaseSettings
from dotenv import load_dotenv


# load_dotenv()  # fix bug with dotenv! should remember in future


# https://github.com/samuelcolvin/pydantic/issues/1368#issuecomment-1068200381


class Settings(BaseSettings):
    server_host: str = '0.0.0.0'
    server_port: int = '80'
    db_path: str
    jwt_secret: str
    jwt_algorithm: str = 'HS256'
    jwt_expiration: int = 3600


settings = Settings(_env_file='.env',
                    _env_file_encoding='utf-8')

if __name__ == '__main__':
    print(settings.db_path)
