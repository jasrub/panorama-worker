from database_connection import conn, sess, Trend, Trend_timestamp, Story, Descriptor_result, Connection, Label
from sqlalchemy.dialects.postgresql import insert
from datetime import datetime, timedelta
from sqlalchemy import text

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
    return bool(sess.query(Story).filter(Story.id==str(story_id)).count())

def get_all_trends(timeframe):
    last_updated = (datetime.now() - timedelta(days=timeframe))
    qry = sess.query(Trend).filter(Trend.updated_at >= last_updated).order_by(Trend.updated_at.desc())
    return [u.__dict__ for u in qry.all()]

def insert_stories(arr):
    conn.execute(Story.__table__.insert(), arr)

def insert_descriptors(arr):
    conn.execute(Descriptor_result.__table__.insert(), arr)

def recalculate_connections():
    # delete all rows in connections table
    connections_table = Connection.__table__
    d = connections_table.delete()
    conn.execute(d)

    sql = text('''
    select "f"."descriptorId" "origin", "s"."descriptorId" "dest", count(*)
    from "DescriptorsResults" "f", "DescriptorsResults" "s"
    where "f"."storyId"="s"."storyId" and "f"."descriptorId"<>"s"."descriptorId"
    group by "f"."descriptorId", "s"."descriptorId"
    ''')
    result = conn.execute(sql)
    i = 0
    for row in result:
        conn.execute(connections_table.insert(), row)

def get_new_labels():
    qry = sess.query(Label).filter(Label.isUsed == False)
    return [u.__dict__ for u in qry.all()]

def label_used(label_id):
    stmt = Label.__table__.update().where(Label.id==label_id).values(isUsed=True)
    conn.execute(stmt)
