from hi_stranger.database import db
from hi_stranger.models import Answer


def init_db():

    print("\nINITIALIZING DB")

    # TODO: only do this if tables don't exist?
    db.create_all()

    # TODO: pre-populate db w/ some stuff?

    # TODO: add stuff to create some admin users for moderation


if __name__ == "__main__":
    init_db()
    print("done!")