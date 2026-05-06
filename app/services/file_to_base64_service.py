import base64

def file_to_base64(file_path: str) -> str:
    with open(file_path, "rb") as file:
        encoded = base64.b64encode(file.read())
    return encoded.decode("utf-8")


