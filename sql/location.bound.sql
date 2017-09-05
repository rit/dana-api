WITH RECURSIVE locations(label, slug, parent_slug, depth) AS
  (SELECT label,
          slug,
          parent_slug,
          1
   FROM collections
   WHERE slug = :slug
     UNION ALL
     SELECT c.label,
            c.slug,
            c.parent_slug,
            loc.depth + 1
     FROM collections c,
          locations loc WHERE loc.parent_slug = c.slug )
SELECT *
FROM locations
ORDER BY depth DESC ;

