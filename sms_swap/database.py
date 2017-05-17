from flask_sqlalchemy import SQLAlchemy
from hi_stranger import create_app


app = create_app()
db = SQLAlchemy(app)