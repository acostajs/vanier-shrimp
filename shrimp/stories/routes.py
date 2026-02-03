from flask import redirect, render_template, url_for, request, flash, session
from re import match

from shrimp.stories import blueprint, forms
from shrimp.stories.models import StoryModel, CommentModel
from shrimp.utils import db
from shrimp.utils.forms import Field
from shrimp.stories.forms import CommentForm


@blueprint.get("/")
def index():
    story_model = StoryModel(db.get_connection())
    stories = story_model.latest()

    return render_template("/stories/index.jinja", stories=stories)


@blueprint.get("/create")
def create():
    account_id = session.get("account_id")
    if account_id is None:
        flash("You must be logged in to be able to submit a story.")
        return redirect(url_for("accounts.login"))

    form = forms.StoriesCreateForm()
    return render_template("/stories/create.jinja", form=form)


@blueprint.post("/create")
def create_submit():
    account_id = session.get("account_id")
    if account_id is None:
        return redirect(url_for("accounts.login"))

    title = request.form["title"]
    link = request.form["link"]
    description = request.form["description"]

    form = forms.StoriesCreateForm(title, link, description)
    stories = StoryModel(db.get_connection())

    form.check_field(Field.not_blank(form.title), "title", "This field cannot be blank")
    form.check_field(
        Field.max_chars(form.title, 80),
        "title",
        "This field cannot be more than 80 characters long",
    )

    form.check_field(Field.not_blank(form.link), "link", "This field cannot be blank")
    form.check_field(
        Field.unique_value(link, lambda link: stories.get_by_link(link) is not None),
        "link",
        "This link has already been submitted.",
    )

    if not form.is_valid:
        return render_template("stories/create.jinja", form=form), 422

    story_id = stories.insert(form.title, form.link, form.description, int(account_id))

    flash("Story added successfully!")

    return redirect(url_for("stories.story_show", story_id=story_id))


@blueprint.get("/<int:story_id>", endpoint="story_show")
def story_show(story_id):
    story_model = StoryModel(db.get_connection())
    comment_model = CommentModel(db.get_connection())

    story = story_model.get(story_id)
    comments = comment_model.comments_for_story(story_id)

    form = forms.CommentForm()

    return render_template(
        "stories/description.jinja", story=story, comments=comments, form=form
    )


@blueprint.post("/<int:story_id>")
def submit_comment(story_id):
    account_id = session.get("account_id")

    if account_id is None:
        flash("You must be logged in to be able to comment.")
        return redirect(url_for("accounts.login"))

    body = request.form["body"]

    form = forms.CommentForm(body)

    form.check_field(Field.not_blank(form.body), "body", "This field cannot be blank")
    form.check_field(
        Field.max_chars(form.body, 10000),
        "body",
        "Comment is too long (max 10,000 characters)",
    )

    story_model = StoryModel(db.get_connection())
    comment_model = CommentModel(db.get_connection())

    if not form.is_valid:
        story = story_model.get(story_id)
        comments = comment_model.comments_for_story(story_id)

        return render_template(
            "stories/description.jinja", story=story, comments=comments, form=form
        ), 422

    comment_model.insert(body, story_id, int(account_id))

    flash("Comment submitted successfully.")
    return redirect(url_for("stories.story_show", story_id=story_id))
