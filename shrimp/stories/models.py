from dataclasses import dataclass
from datetime import datetime
from shrimp.utils.db import Model


@dataclass
class Story:
    id: int
    title: str
    link: str
    description: str
    date_posted: datetime
    username: str


@dataclass
class Comment:
    id: int
    body: str
    date_posted: datetime
    username: str


class StoryModel(Model):
    def insert(self, title: str, link: str, description: str, account_id: int) -> int:
        cursor = self.db.execute(
            """
            INSERT INTO Stories (title, link, description, account_id)
                VALUES (?, ?, ?, ?)
            """,
            (title, link, description, account_id),
        )
        self.db.commit()

        id = cursor.lastrowid
        if not id:
            raise RuntimeError("insert failed: no lastrowid")

        return id

    def get(self, id: int) -> Story:
        row = self.db.execute(
            """
            SELECT Stories.id, title, link, description, date_posted, Accounts.username
            FROM Stories
            JOIN Accounts ON Stories.account_id = Accounts.id
            WHERE Stories.id = ?
            """,
            (id,),
        ).fetchone()

        if not row:
            raise RuntimeError(f"Story with id {id} not found")

        return Story(*row)

    def get_by_link(self, link: str) -> Story:
        cursor = self.db.execute(
            """
            SELECT * 
            FROM stories 
            WHERE link = ?
            """,
            (link,),
        )

        return cursor.fetchone()

    def account_stories(self, account_id: int) -> list[Story]:
        stories = self.db.execute(
            """
            SELECT Stories.id, title, link, description, date_posted, Accounts.username
            FROM Stories, Accounts
            WHERE Stories.account_id = Accounts.id
                AND Accounts.id = ?
            """,
            (account_id,),
        )
        return [Story(*s) for s in stories]

    def latest(self) -> list[Story]:
        rows = self.db.execute(
            """
            SELECT Stories.id, title, link, description, date_posted, Accounts.username
            FROM Stories
            JOIN Accounts ON Stories.account_id = Accounts.id
            ORDER BY date_posted DESC
            LIMIT 10
            """
        ).fetchall()

        return [Story(*row) for row in rows]


class CommentModel(Model):
    def insert(self, body: str, story_id: int, account_id: int) -> int:
        cursor = self.db.execute(
            """
            INSERT INTO comment (body, story_id, account_id)
            VALUES (?, ?, ?)
            """,
            (body, story_id, account_id),
        )
        self.db.commit()

        id = cursor.lastrowid
        if not id:
            raise RuntimeError("insert failed: no lastrowid")

        return id

    def account_comments(self, account_id: int) -> list[Comment]:
        comments = self.db.execute(
            """
            SELECT comment.id, comment.body, comment.date_posted
            FROM comment, Accounts
            JOIN Accounts ON comment.account_id = Accounts.id
            WHERE comment.account_id = Accounts.id
                AND Accounts.id = ?
            """,
            (account_id,),
        )
        return [Comment(*s) for s in comments]

    def comments_for_story(self, story_id: int) -> list[Comment]:
        rows = self.db.execute(
            """
            SELECT comment.id, comment.body, comment.date_posted, Accounts.username
            FROM comment
            JOIN Accounts ON comment.account_id = Accounts.id
            WHERE comment.story_id = ?
            ORDER BY comment.date_posted DESC
            """,
            (story_id,),
        )
        return [Comment(*row) for row in rows]
