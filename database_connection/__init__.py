import os
from datetime import datetime, timedelta
import uuid

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, Boolean, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import Session

Base = declarative_base()
engine = None
conn = None
sess = None

class Story(Base):
    __tablename__ = 'Stories'
    id = Column('id', String, primary_key=True)
    mediaId = Column('mediaId', String)
    title = Column('title', String)
    url = Column('url', String)
    publishDate = Column('publishDate', DateTime, index=True)
    mediaName = Column('mediaName', String)
    mediaUrl = Column('mediaUrl', String)
    collectDate = Column('collectDate', DateTime)
    isMediaCloud = Column('isMediaCloud', Boolean)
    isSuperglue = Column('isSuperglue', Boolean)
    leftRight = Column('leftRight', Float, index=True)
    image = Column('image', String)
    posNeg = Column('posNeg', Float, index=True)
    trend = Column('trend', Float, index=True)
    objective = Column('objective', Float, index=True)
    createdAt = Column('createdAt', DateTime, default=datetime.now)
    updatedAt = Column('updatedAt', DateTime, onupdate=datetime.now)

class Descriptor(Base):
    __tablename__ = 'Descriptors'
    id = Column('id', String, primary_key=True, index=True)


class Descriptor_result(Base):
    __tablename__ = 'DescriptorsResults'
    id = Column('id', Integer, primary_key=True)
    descriptorId = Column('descriptorId', None, ForeignKey(Descriptor.id), index=True)
    storyId = Column('storyId',None, ForeignKey(Story.id), index=True)
    score = Column('score', Float)
    createdAt = Column('createdAt', DateTime, default=datetime.now)
    updatedAt = Column('updatedAt', DateTime, onupdate=datetime.now)

class Connection(Base):
    __tablename__ = 'Connections'
    id = Column('id', Integer, primary_key=True)
    origin = Column('origin', None, ForeignKey(Descriptor.id), index=True)
    dest = Column('dest', String, index=True)
    count = Column('count',Integer)

class Trend(Base):
    __tablename__ = 'Trends'
    id = Column('id', String, primary_key=True, index=True)
    created_at = Column('created_at', DateTime, default=datetime.now)
    updated_at = Column('updated_at', DateTime, onupdate=datetime.now, index=True)

class Trend_timestamp(Base):
    __tablename__ = 'TrendsTimestamps'
    id = Column('id', Integer, primary_key=True)
    trend_id = Column('trend_id', None, ForeignKey(Trend.id), index=True)
    created_at = Column('created_at', DateTime, default=datetime.now, index=True)

class Label(Base):
    __tablename__ = 'Labels'
    id = Column('id', Integer, primary_key=True)
    storyId = Column('storyId',None, ForeignKey(Story.id), index=True)
    isSuperglue = Column('isSuperglue', Boolean)
    isMediaCloud = Column('isMediaCloud', Boolean)
    posNeg = Column('posNeg', Float, index=True)
    trend = Column('trend', Float, index=True)
    objective = Column('objective', Float, index=True)
    leftRight = Column('leftRight', Float, default=0, index=True)
    isUsed = Column('isUsed', Boolean, default=False, index=True)
    createdAt = Column('createdAt', DateTime, default=datetime.now)
    updatedAt = Column('updatedAt', DateTime, onupdate=datetime.now, index=True)

def load_db():
    global engine
    global conn
    global sess
    engine = create_engine(os.environ.get('DB_URL'))
    Base.metadata.create_all(engine)
    conn = engine.connect()
    sess = Session(bind=conn)

load_db()

def close_db():
    global enging, conn, sess
    conn.close()
    sess.close()
    engine.dispose()

