from app import create_app
from app.databse import db

app = create_app()
db.create_all(app=app)

if __name__ == "__main__":
    print("Finish!")
    app.debug = app.config['DEBUG']
    app.run()