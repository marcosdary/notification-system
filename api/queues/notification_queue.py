from datetime import datetime

from api.constants import redisClient
from api.services import TokenService
from api.schemas import NotificationSchema

class NotificationQueue:
    def __init__(self):
        self._redis_client = redisClient
        self._token_service = TokenService()
        self._name_key = "queue:notification"

    def _encode_notification(self, schema: NotificationSchema) -> str:
        return self._token_service.encode(schema.model_dump())

    def _decode_notification(self, key: str) -> dict:
        return self._token_service.decode(key)
    
    def add_notification(self, schema: NotificationSchema) -> None:
        key = self._encode_notification(schema)
        self._redis_client.lpush(self._name_key, key)
        return

    def get_end_notification(self) -> NotificationSchema:
        key = self._redis_client.rpop(self._name_key)

        if not key:
            return None
        
        data = self._decode_notification(key)
        schema = NotificationSchema.model_validate(data)
        schema.endIn = datetime.now()
        return schema

    
    
