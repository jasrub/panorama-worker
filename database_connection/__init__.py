import os
from datetime import datetime, timedelta
import uuid

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm.session import sessionmaker, Session

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

engine = create_engine(os.environ.get('DB_URL'))
Base.metadata.create_all(engine)
conn = engine.connect()

def insert_trend(term):
    insert_stmt = insert(Trend.__table__).values(
        id=term, updated_at=datetime.now())
    do_update_stmt = insert_stmt.on_conflict_do_update(
        index_elements=['id'],
        set_=dict(updated_at=datetime.now())
    )
    conn.execute(do_update_stmt)
    conn.execute(insert(Trend_timestamp.__table__).values(trend_id=term))

def is_story_in_db(story_id):
    conn = engine.connect()
    instance = conn.query(Story).filter_by(id=story_id).first()
    return True if instance else False

def get_all_trends(timeframe):
    sess = Session(bind=conn)
    last_updated = (datetime.now() - timedelta(days=timeframe))
    qry = sess.query(Trend).filter(Trend.updated_at >= last_updated).order_by(Trend.updated_at.desc())
    return [u.__dict__ for u in qry.all()]