from dataclasses import dataclass

from shrimp.utils.forms import Form


@dataclass
class StoriesCreateForm(Form):
    title: str = ""
    link: str = ""
    description: str = ""
    username: str = ""


@dataclass
class CommentForm(Form):
    body: str = ""
    username: str = ""
