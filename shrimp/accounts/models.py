from dataclasses import dataclass

from werkzeug.security import generate_password_hash, check_password_hash

from shrimp.utils.db import Model
from shrimp.stories.models import Story, StoryModel


@dataclass
class Account:
    id: int
    username: str
    email: str
    password: str
    stories: list[Story]


class InvalidCredentialsError(Exception): ...


class AccountModel(Model):
    def insert(self, username: str, email: str, password: str) -> int:
        cursor = self.db.execute(
            """
            INSERT INTO Accounts (username, email, password)
                VALUES (?, ?, ?)
            """,
            (username, email, generate_password_hash(password)),
        )
        self.db.commit()

        id = cursor.lastrowid
        if not id:
            raise RuntimeError("insert failed: no lastrowid")

        return id

    def get(self, id: int) -> Account:
        username, email, password = self.db.execute(
            "SELECT id, username, email, password FROM Accounts WHERE id = ?", (id,)
        ).fetchone()
        stories = StoryModel(self.db)
        return Account(id, username, email, password, stories.account_stories(id))

    def authenticate(self, email: str, password: str) -> Account:
        account = self.db.execute(
            "SELECT id, username, email, password FROM Accounts WHERE email = ?",
            (email,),
        ).fetchone()

        if account is None or not check_password_hash(account[3], password):
            raise InvalidCredentialsError()

        id, username, email, password = account
        stories = StoryModel(self.db)
        return Account(id, username, email, password, stories.account_stories(id))

    def email_exists(self, email: str) -> bool:
        account = self.db.execute(
            "SELECT * FROM Accounts WHERE email = ?", (email,)
        ).fetchone()
        return account is not None

    def username_exists(self, username: str) -> bool:
        account = self.db.execute(
            "SELECT * FROM Accounts WHERE username = ?", (username,)
        ).fetchone()
        return account is not None
