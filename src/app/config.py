from dynaconf import Dynaconf

settings = Dynaconf(
    settings_files=["settings.toml"],
    envvar_prefix=False,
    environments=True
)

class Config:
    def __init__(self):
        env = settings.get("DEFAULT", "TEST")
        self.DATABASE_URL = settings[env].DATABASE_URL
        self.REDIS_HOST = settings[env].REDIS_HOST
        self.REDIS_PORT = settings[env].REDIS_PORT

def get_config():
    return Config()

# print(settings.to_dict())