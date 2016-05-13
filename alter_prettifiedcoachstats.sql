select 
	concat(seasonstartyear, '-',seasonendyear) as seasondoubleyear,
    tnt.Team_Name,
    tnt.Team_ID,
	zz.* 
    
from(
		select
			x.season,
			left(x.season,4) as SeasonStartYear,
			concat(case when cast(x.season as char(10)) like '19%' then '19'  else '20' end,cast(right(cast(x.season as char(10)),2) as char(10))) as SeasonEndYear,
			x.coach,
			x.school,
			left(rtrim(ltrim(x.season)),4) - min(left(rtrim(ltrim(z.firstseason)),4)) as coachtenure,
			SUM(totalgame) AS totalgames,
			SUM(wins) AS totalwins,
			SUM(losses) AS totallosses,
			SUM(wins) / SUM(totalgame) AS seasonwinpercentage,
			case when max(y.ncaavisit) then max(y.ncaavisits) -1 else max(y.ncaavisits) end as ncaavisits,
			max(y.ncaavisit) as ncaavisit,
			max(y.regseasonchamp) as regseasonchamp,
			max(y.ncaachamp) as ncaachamp
			
		from ncaabasketball.coaches x
		join (
				SELECT 
					a.coach,
					a.school,
					a.season,
					#@rownum := @rownum + 1 AS coachtenure, #num of coaching seasons at beginning of year
					sum(c.ncaavisits) as ncaavisits,
					case when notes like '%NCAA Tournament%' then 1 else 0 end as ncaavisit,
					case when notes like '%Reg. Season Champion%' then 1 else 0 end as regseasonchamp,
					case when notes like '%Tournament Champion%' then 1 else 0 end as ncaachamp
					
				FROM ncaabasketball.coaches a

				join ( 
				select 
					distinct coach, 
					season, 
					case when notes like '%NCAA Tournament%' then 1 else 0 end  = 1 as ncaavisits
				from ncaabasketball.coaches
					) c
					on c.coach = a.coach
					and c.season <= a.season

				#where a.coach like '%al skinner%'
				GROUP BY a.coach, a.school, a.season, notes

		) y 
			on y.coach = x.coach
			and y.school = x.school
			and y.season = x.season

		join (
			select 
				coach, 
				min(season) as firstseason
			from ncaabasketball.coaches
			group by coach
			) z
			on z.coach = x.coach

		group by x.coach, x.school, x.season

) zz

left join ncaabasketball.teamnametranslations tnt
	on tnt.formattedschool = zz.school




#use ncaabasketball;





    
