from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship

from datetime import datetime

from db import Base, engine

class User(UserMixin, Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(50), index=True, unique=True)
    password_hash = Column(String(256), nullable=False)
    role = Column(String(10), index=True, default='user')
    email = Column(String(50), unique=True, nullable=False)
    # comm = relationship("Comment")

    def __repr__(self):
        return self.username
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    @property
    def is_admin(self):
        return self.role == 'admin'
    
class Wine(Base):
    __tablename__ = "wines"
    id = Column(Integer, primary_key=True)
    wine_name = Column(String(100))
    wine_type = Column(String(50))
    winery_name = Column(String(100))
    country = Column(String(50))
    region = Column(String(100))
    grape = Column(String(50))
    year = Column(String(10))
    avg_price = Column(String(10))
    viv_rating = Column(String(10))
    img_link = Column(String(100))
    comment = relationship("Comment")

    def __repr__(self):
        return self.wine_name
    
class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True)
    author = Column(Integer, ForeignKey(User.id))
    wine_id = Column(Integer, ForeignKey(Wine.id))
    text = Column(String(350), nullable=False)
    date_created = Column(DateTime, default=datetime.now)
    
    def __repr__(self):
        return f'Comment({self.text}, {self.date_created.strftime("%d.%m.%Y-%H.%M")}, {self.wine_id})'

    user = relationship("User")
    wine = relationship("Wine")

    
if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)