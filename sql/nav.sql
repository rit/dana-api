WITH RECURSIVE series (slug,
    parent_slug,
    label,
    position,
    depth)
AS (
    SELECT
        c.slug,
        c.parent_slug,
        c.label,
        c.position,
        1
    FROM
        collections c
    WHERE
        parent_slug = '2011m30'
    UNION ALL
    SELECT
        c.slug,
        c.parent_slug,
        c.label,
        c.position,
        s.depth + 1
    FROM
        collections c,
        series s
    WHERE
        c.parent_slug = s.slug
        AND c.type = 'sc:Collection'), collection_series (parent_slug)
AS (
    SELECT
        parent_slug, depth, count(parent_slug)
    FROM
        series
    WHERE
        series.depth < 3
    GROUP BY
        parent_slug,
        depth
    HAVING
        -- If the collection has more than 21 children,
        -- assume it's the leaf collection
        series.count < 21
)
SELECT
    s.position AS pos,
    s.slug,
    s.parent_slug,
    s.label,
    s.depth
FROM
    series s,
    collection_series
WHERE
    s.parent_slug = collection_series.parent_slug
ORDER BY
    depth,
    s.parent_slug,
    position;

