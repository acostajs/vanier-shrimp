from flask import Blueprint

blueprint = Blueprint("stories", __name__, url_prefix="/stories")


from shrimp.stories import routes
