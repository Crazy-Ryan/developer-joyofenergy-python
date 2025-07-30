import hashlib
import json
import os
import secrets


def get_key_user(api_key: str) -> str | None:
    valid_key_map = json.loads(os.getenv("API_KEY_DIGEST_TO_USER", "{}"))
    hashed_incoming_key = hashlib.sha256(api_key.encode()).hexdigest()
    for valid_hash, user in valid_key_map.items():
        if secrets.compare_digest(hashed_incoming_key, valid_hash):
            return user
    return None
