import random
from src.config.config import Config

class ProxyManager:
    @staticmethod
    def get_random_proxy():
        if Config.PROXY_LIST:
            return random.choice(Config.PROXY_LIST)
        return None 