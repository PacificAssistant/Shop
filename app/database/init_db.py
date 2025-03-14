from app.database import models
from app.database.database import Base,engine


def create():
    models.Base.metadata.create_all(bind=engine)






