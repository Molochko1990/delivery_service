from dynaconf import Dynaconf

settings = Dynaconf(
    settings_files=["settings.toml"],
    envvar_prefix="",
    environments=True,
    default_env="test"
)

class Config:
    def __init__(self):
        self.DATABASE_URL = settings.get('DATABASE_URL')
        self.REDIS_HOST = settings.get('REDIS_HOST')
        self.REDIS_PORT = settings.get('REDIS_PORT')

    def __str__(self):
        return (
            f"Config(\n"
            f"  DATABASE_URL='{self.DATABASE_URL}',\n"
            f"  REDIS_HOST='{self.REDIS_HOST}',\n"
            f"  REDIS_PORT={self.REDIS_PORT}\n"
            f")"
        )

def get_config():
    return Config()

# print(settings.to_dict())