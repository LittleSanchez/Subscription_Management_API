BLOCKLIST = set()


def add_to_blocklist(jti):
    BLOCKLIST.add(jti)


def is_token_revoked(jwt_payload):
    jti = jwt_payload["jti"]
    return jti in BLOCKLIST
