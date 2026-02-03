from dataclasses import dataclass

from shrimp.utils.forms import Form


@dataclass
class LoginForm(Form):
    email: str = ""
    password: str = ""


@dataclass
class AccountCreateForm(Form):
    username: str = ""
    email: str = ""
    password: str = ""
