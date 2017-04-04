import os
from datetime import datetime, timedelta
import uuid

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, Boolean, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import Session

Base = declarative_base()

class Story(Base):
    __tablename__ = 'Stories'
    id = Column('id', String, primary_key=True)
    media_id = Column('mediaId', String)
    title = Column('title', String)
    url = Column('url', String)
    publish_date = Column('publishDate', DateTime, index=True)
    media_name = Column('mediaName', String)
    media_url = Column('mediaUrl', String)
    collect_date = Column('collectDate', DateTime)
    is_media_cloud = Column('isMediaCloud', Boolean)
    is_supeglue = Column('isSuperglue', Boolean)
    left_right = Column('leftRight', Float, default=0, index=True)
    image = Column('image', String)
    pos_neg = Column('posNeg', Float, default=0, index=True)
    trend = Column('trend', Float, default=0, index=True)
    objective = Column('objective', Float, default=0, index=True)

class Descriptor(Base):
    __tablename__ = 'Descriptors'
    id = Column('id', String, primary_key=True, index=True)


class Descriptor_result(Base):
    __tablename__ = 'DescriptorsResults'
    id = Column('id', Integer, primary_key=True)
    descriptor_id = Column('descriptorId', None, ForeignKey('Descriptors.id'), index=True)
    story_id = Column('storyId',None, ForeignKey('Stories.id'), index=True)
    score = Column('score', Float)

class Taxonomy(Base):
    __tablename__ = 'Taxonomies'
    id = Column('id', String, primary_key=True)

class Taxonomy_result(Base):
    __tablename__ = 'TaxonomiesResults'
    id = Column('id', Integer, primary_key=True)
    taxonomy_id = Column('taxonomyId', None, ForeignKey('Taxonomies.id'))
    story_id = Column('storyId',None, ForeignKey('Stories.id'), index=True)
    score = Column('score', Float)

class Connection(Base):
    __tablename__ = 'Connections'
    id = Column('id', String, primary_key=True, default=lambda: uuid.uuid4().hex)
    origin = Column('origin', None, ForeignKey('Descriptors.id'), index=True)
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
    trend_id = Column('trend_id', None, ForeignKey('Trends.id'), index=True)
    created_at = Column('created_at', DateTime, default=datetime.now, index=True)

class Label(Base):
    __tablename__ = 'Labels'
    id = Column('id', Integer, primary_key=True)
    storyId = Column('storyId',None, ForeignKey('Stories.id'), index=True)
    isSuperglue = Column('isMediaCloud', Boolean)
    isMediaCloud = Column('isMediaCloud', Boolean)
    posNeg = Column('posNeg', Float, index=True)
    trend = Column('trend', Float, index=True)
    objective = Column('objective', Float, index=True)
    leftRight = Column('leftRight', Float, default=0, index=True)
    isUsed = Column('isUsed', Boolean, default=False, index=True)
    createdAt = Column('createdAt', DateTime, default=datetime.now)
    updatedAt = Column('updatedAt', DateTime, onupdate=datetime.now, index=True)

engine = create_engine(os.environ.get('DB_URL'))
Base.metadata.create_all(engine)
conn = engine.connect()
sess = Session(bind=conn)

