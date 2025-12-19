--select count(*) from "WeeklyPicks".newtable where points > 0;
select
	team_name,
	points,
	row_number() over (order by points) as your_confidence_points
from
	"WeeklyPicks".newtable
where
	points > 0
group by
	team_name
order by
	points;