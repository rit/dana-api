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
        p.depth + 1
    FROM
        collections c,
        series p
    WHERE
        c.parent_slug = p.slug
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
    p.position AS pos,
    p.slug,
    p.parent_slug,
    p.label,
    p.depth
FROM
    series p,
    collection_series
WHERE
    p.parent_slug = collection_series.parent_slug
ORDER BY
    depth,
    p.parent_slug,
    position;

