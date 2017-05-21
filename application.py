from flask import redirect, request, render_template, Response, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import func
from functools import wraps
from sms_swap import create_app
from sms_swap.app_config import ADMIN_USER, ADMIN_PASS, SECRET_KEY, \
                                    TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NO
# TODO: allow these config variables to be set in the environment
from sms_swap.models import Answer
from sms_swap.database import db
import twilio.twiml
from twilio.rest import TwilioRestClient


application = create_app()

@application.route("/")
def index():
    # TODO: grab some recordings to show
    return render_template('index.html')



@application.route("/respond", methods=['GET', 'POST'])
def respond():
    """Respond to incoming texts"""


    print("\n\nrequest.values")
    print(request.values)

    resp = twilio.twiml.Response()

    incoming_msg = request.values.get('Body', '')

    # this clears all cookies
    if(incoming_msg=='clear'):
        session['seen_prompt'] = False
        session['gave_rec'] = False
        session['extra_msg'] = False
        resp.sms("erasing my memory of our conversation")
        return str(resp)


    # if exchange has been completed
    if session.get('extra_msg',False):
        session['extra_msg'] = False
        if incoming_msg.lower().startswith('y'):
            session['seen_prompt'] = False
            session['gave_rec'] = False
        elif incoming_msg.lower().startswith('n'):
            # TODO: ask for feedback?
            resp.sms('ok, later!')
            return str(resp)



    if not session.get('seen_prompt',False):
        # custom greeting for creative mornings
        if 'serendipity' in incoming_msg.lower():
            resp.sms("hey there! want to exchange music recs with random people in the CreativeMornings community? reply & tell me about a song you wish more people knew about.")
        else:
            resp.sms("give a music rec, get a music rec! \nreply & tell me about a song you wish more people knew about.")
        session['seen_prompt'] = True

    elif not session.get('gave_rec',False):
        # saving rec here
        if incoming_msg: # only if there is a msg
            new_rec = Answer(request.values.get('SmsSid'), request.values.get('From'), incoming_msg)
            db.session.add(new_rec)
            db.session.commit()

        # grabbing a rec from a stranger
        # TODO: ensure that this is not a rec from yourself
        random_rec = Answer.query.filter_by(is_approved=True).filter(Answer.from_number!=request.values.get('From')).order_by(func.rand()).first()

        if random_rec:
            random_rec.view_count = random_rec.view_count+1
            db.session.add(random_rec)
            db.session.commit()
            resp.sms("thanks! I'll pass it on. here's a rec from a stranger: \n%s" %random_rec.answer_text)

            # alerting rec-giver when rec has been seen for the first time
            if random_rec.from_number and random_rec.view_count==1:
                client = TwilioRestClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

                msg = "your rec (%s) was just delivered to a stranger" %random_rec.answer_text
                message = client.messages.create(to=random_rec.from_number, from_=TWILIO_PHONE_NO,
                                                             body=msg)
        else:
            # TODO: deal with this
            resp.sms("thanks! unfortunately I don't have any recs to show you b/c I haven't collected enough")

        session['gave_rec'] = True
    else:
        # TODO: a more elegant way of handling additional messages?
        session['extra_msg'] = True
        resp.sms("do you want to start over & exchange another album rec? \n(y/n)")


    return str(resp)

@application.route("/rollback", methods=['GET', 'POST'])
def rollback():
    # TODO: figure out what's going on???
    db.session.rollback()
    return redirect('/respond')


def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == ADMIN_USER and password == ADMIN_PASS

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your credentials for that url', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated


@application.route('/review')
@requires_auth
def review():
    review_queue = Answer.query.filter_by(is_approved=None).all()
    approved = Answer.query.filter_by(is_approved=True).all()
    disapproved = Answer.query.filter_by(is_approved=False).all()
    return render_template('review.html', review_queue = review_queue, approved=approved, disapproved=disapproved)

@application.route('/approve/<ans_id>')
@requires_auth
def approve(ans_id):
    ans = Answer.query.get(ans_id)
    ans.is_approved = True
    db.session.commit()
    return redirect('/review')

@application.route('/disapprove/<ans_id>')
@requires_auth
def disapprove(ans_id):
    ans = Answer.query.get(ans_id)
    ans.is_approved = False
    db.session.commit()
    return redirect('/review')


@application.route('/initialize')
@requires_auth
def initialize():
    # TODO: only do this if tables don't exist?
    db.create_all()
    return redirect('/')



if __name__ == "__main__":

    application.secret_key = SECRET_KEY
    application.run(debug=True, host='0.0.0.0')
