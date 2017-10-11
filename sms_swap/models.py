import datetime

from sms_swap.database import db


class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text_sid = db.Column(db.String(255))
    from_number = db.Column(db.String(255))
    answer_text = db.Column(db.Text)
    is_approved = db.Column(db.Boolean)
    view_count = db.Column(db.Integer)
    dt = db.Column(db.DateTime, default=datetime.datetime.now)

    def __init__(self, text_sid, from_number, answer_text):
        self.text_sid = text_sid
        self.from_number = from_number
        self.answer_text = answer_text
        self.view_count = 0


    def __repr__(self):
        return '<Answer %r %r>' % (self.from_number, self.answer_text[:10])
