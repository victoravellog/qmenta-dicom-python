def user_schema(user) -> dict:
    return {
        'id': str(user['_id']),
        'username': user['username'],
        'email': user['email'],
        'disabled': user['disabled'],
    }


def userdb_schema(user) -> dict:
    return {
        'id': str(user['_id']),
        'username': user['username'],
        'email': user['email'],
        'disabled': user['disabled'],
        'password': user['hashed_password'],
    }


def users_schema(users) -> list:
    return [user_schema(user) for user in users]
