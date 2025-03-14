from app import create_app, db


app = create_app()

with app.app_context():
    from app.database.models import *

if __name__ == "__main__":
    app.run(debug=True)
