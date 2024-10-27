from dynaconf import Dynaconf


settings = Dynaconf(
    settings_files=["settings.toml"],
    envvar_prefix=False,  # префикс для переменных окружения
)


class Config:
    def __init__(self):
        self.DATABASE_URL = settings.DEFAULT.DATABASE_URL
        self.REDIS_HOST = settings.DEFAULT.REDIS_HOST
        self.REDIS_PORT = settings.DEFAULT.REDIS_PORT

def get_config():
    return Config()

# print(settings.to_dict())