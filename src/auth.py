import json
import base64

class AuthManager:
    def __init__(self, path="config/auth_users.json"):
        try:
            with open(path, "r") as f:
                self.users = json.load(f)["users"]
        except:
            self.users = {}

    def is_request_authorized(self, headers):
        if not self.users:
            return True  # no auth required

        auth_header = headers.get("Proxy-Authorization")
        if not auth_header:
            return False

        if not auth_header.startswith("Basic "):
            return False

        encoded = auth_header.split(" ")[1]
        decoded = base64.b64decode(encoded).decode()

        if ":" not in decoded:
            return False

        username, password = decoded.split(":", 1)

        return self.users.get(username) == password
