from __future__ import annotations
from typing import List
import json
import os

class User:
    USERS_FILE = "/app/config/users.json"
    ALL: List[User] = []

    name: str
    perms: List[str]
    key: str

    def __init__(self, name: str, profile) -> None:
        self.name = name
        self.perms = profile.get("permissions", [])
        self.key = profile.get("key", "")

    def has_perm(self, needed: str) -> bool:
        return needed in self.perms

    def dump(self):
        return {"name": self.name, "perms": self.perms, "key": "<secret>"}

    @classmethod
    def load_users(cls) -> None:
        if not os.path.exists(cls.USERS_FILE):
            raise Exception("no users.json")
        with open(cls.USERS_FILE, "r") as f:
            data = json.load(f)
            cls.ALL = []
            for name, prof in data.items():
                cls.ALL.append(User(name, prof))
