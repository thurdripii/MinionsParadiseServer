
import hashlib
import secrets
import uuid


def generate_player_id():
    return str(uuid.uuid4())


def generate_session_id():
    return str(uuid.uuid4())


def generate_session_key():
    return secrets.token_urlsafe(32)


def hash_session_key(session_key):
    if not isinstance(session_key, str) or not session_key:
        raise ValueError("Invalid session key")

    return hashlib.sha256(
        session_key.encode("utf-8")
    ).hexdigest()


def verify_session_key(session_key, stored_hash):
    if not isinstance(session_key, str) or not isinstance(stored_hash, str):
        return False

    return secrets.compare_digest(
        hash_session_key(session_key),
        stored_hash
    )
