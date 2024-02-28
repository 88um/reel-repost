import os
from sqlalchemy import create_engine, String, Integer, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column 



Base = declarative_base()

class Account(Base):
    __tablename__ = 'account'

    id = Column(Integer, autoincrement=True, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    credentials = Column(String, unique=True, nullable=False)

    def __repr__(self):
        return f"{self.__class__.__name__}({', '.join([f'{k}={v}' for k, v in self.__dict__.items() if not k.startswith('_')])})"


class SavedMedia(Base):
    __tablename__ = 'saved_media'

    id = Column(Integer, autoincrement=True, primary_key=True)
    pk = Column(String, unique=True, nullable=False)
    media_type = Column(Integer, nullable=False)
    like_count = Column(Integer, nullable=False)
    comment_count = Column(Integer, nullable=False)
    caption = Column(String, nullable=False)
    paths = Column(String, unique=True, nullable=True)
    video_path = Column(String, nullable=True)
    thumbnail_path = Column(String, nullable=True)
    owner= Column(String, nullable=False)

    def __init__(self, media_type: int, pk: str, like_count: int, comment_count: int, caption: str,
                  owner: str, paths: str = None, video_path: str = None, thumbnail_path: str = None,
                ) -> None:
        self.pk = pk
        self.media_type = media_type
        self.like_count = like_count
        self.comment_count = comment_count
        self.caption = caption
        self.paths = paths
        self.video_path = video_path
        self.thumbnail_path = thumbnail_path
        self.owner = owner


    def __repr__(self):
        return f"{self.__class__.__name__}({', '.join([f'{k}={v}' for k, v in self.__dict__.items() if not k.startswith('_')])})"



class Target(Base):
    __tablename__ = 'target'

    id = Column(Integer, autoincrement=True, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    user_id = Column(String, nullable=False, unique=True)
    

    def __repr__(self):
        return f"{self.__class__.__name__}({', '.join([f'{k}={v}' for k, v in self.__dict__.items() if not k.startswith('_')])})"


class Log(Base):
    __tablename__ = 'log'

    id = Column(Integer, autoincrement=True, primary_key=True)
    username = Column(String, nullable=False)
    log_string = Column(String, unique=True, nullable=False)
    log = Column(String, nullable=False)

    def __repr__(self):
        return f"{self.__class__.__name__}({', '.join([f'{k}={v}' for k, v in self.__dict__.items() if not k.startswith('_')])})"

