import hashlib
import json
import os
import secrets


def get_key_user(api_key: str) -> str | None:
    valid_key_digiests = os.getenv("API_KEY_DIGESTS", "").split(",")
    hashed_incoming_key = hashlib.sha256(api_key.encode()).hexdigest()
    for valid_hash in valid_key_digiests:
        if secrets.compare_digest(hashed_incoming_key, valid_hash):
            return True
    return None
