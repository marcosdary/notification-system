from jwt import encode

def sign_token(key: str, payload: dict) -> str:
    return encode(payload, key, "HS256") 

