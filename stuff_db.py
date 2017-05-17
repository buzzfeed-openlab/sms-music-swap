from hi_stranger.database import db
from hi_stranger.models import Answer

#TODO: make this smarter and then move into init_db.py
def stuff_db():

    print("\nADDING SOMETHING TO DB")

    rec = Answer('dummy1', '', "boys don't cry by frank ocean")
    rec.is_approved = True
    db.session.add(rec)
    db.session.commit()

    # TODO: pre-populate db w/ some stuff?

    # TODO: add stuff to create some admin users for moderation


if __name__ == "__main__":
    stuff_db()
    print("done!")