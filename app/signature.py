from flask import request

from hashlib import sha1


def get_signature():
    user_agent = request.user_agent
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    h = sha1((str(user_agent) + ip).encode())
    return h.hexdigest()


def check_signature(h):
    return get_signature() == h
