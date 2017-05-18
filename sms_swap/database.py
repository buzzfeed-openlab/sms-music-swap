from flask_sqlalchemy import SQLAlchemy
from sms_swap import create_app


app = create_app()
db = SQLAlchemy(app)
