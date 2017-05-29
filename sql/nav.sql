with recursive parent(slug, parent_slug, label, position, depth) as (
  select c.slug, c.parent_slug, c.label, c.position, 1
  from collections c
  where parent_slug = '2011m30'
union all
  select c.slug, c.parent_slug, c.label, c.position, p.depth + 1
  from collections c, parent p
  where c.parent_slug = p.slug
  and c.type = 'sc:Collection'
), 

series(parent_slug) as (
  select parent_slug, depth, count(parent_slug) from parent
  where parent.depth < 3
  group by parent_slug, depth
  having parent.count < 21
)

select p.position as pos, p.slug, p.parent_slug, p.label, p.depth from parent p, series
where p.parent_slug = series.parent_slug
order by depth, p.parent_slug, position
;
