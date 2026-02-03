from os import getcwd, path


class Config:
    DATABASE_PATH = path.join(getcwd(), "instance", "db.sqlite")
    SECRET_KEY = b'_5#y2L"F4Q8z\n\xec]/'
