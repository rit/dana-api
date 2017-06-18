from sqlalchemy import select

from .walker import Collection


def test_cte(dbsession):
    # Get the parents of a collection. To be used in the Location in Collection.
    slug = '2011m30_ref6628_a6e'
    c = Collection.__table__.columns
    coll = select(c).where(c.slug==slug).cte(recursive=True)
    coll_alias = coll.alias()
    parents = Collection.__table__.alias()
    coll = coll.union_all(
        select(parents.c).
        where(parents.c.slug == coll_alias.c.parent_slug)
    )
    sql = select(coll.c).order_by(coll.c.slug)
    res = dbsession.execute(sql)
    assert 0, [row.doc.get('label', '') for row in res.fetchall()]
