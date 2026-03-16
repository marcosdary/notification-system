from api.constants import redisClient
from api.schemas import NotificationSchema

class NotificationQueue:
    def __init__(self):
        self._redis_client = redisClient

    
    

