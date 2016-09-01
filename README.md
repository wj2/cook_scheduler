## cook_scheduler
This program generates a cook schedule given a list of date preferences for each cook. In particular, it uses linear programming to select a schedule minimizing the average cook preference.

### Usage
```
WARNING:root:Sony  selected excluded dates: ['21-08-2016']
WARNING:root:There 20 slots but only 18 cooks
Status: Optimal
Average preference: 1.88888888889
WARNING:root:Unassigned dates: ['31-07-2016', '01-08-2016']
                     date  preference
name                                 
               2016-07-31         NaN
               2016-08-01         NaN
Joey Brink     2016-08-02         3.0
Laura          2016-08-04         3.0
Sarah          2016-08-05         3.0
Sophia         2016-08-06         1.0
Kara           2016-08-07         2.0
Noah           2016-08-08         1.0
geoff          2016-08-09         1.0
Kevin Casto    2016-08-11         1.0
Kayla          2016-08-12         1.0
Will           2016-08-13         2.0
Asa            2016-08-14         2.0
Eric           2016-08-15         1.0
Chris q        2016-08-16         4.0
Jeff           2016-08-17         2.0
Michael        2016-08-17         3.0
Magnolia       2016-08-18         1.0
David Nekimken 2016-08-19         1.0
Sony           2016-08-20         2.0
```

### Example
The repository contains sample preferences in the `data` directory. For example, to generate an optimal cook schedule for July and save it to `output.csv` and save an iCalendar to `calendar.ics`:
```
> python cook_scheduler.py 2016-07-31 2016-08-20 data/july_2016.csv -c 2016-08-17 --exclude 2016-08-03 2016-08-10 --csv output.csv --ical calendar.ics

WARNING:root:Sony  selected excluded dates: set([Timestamp('2016-08-21 00:00:00')])
WARNING:root:There 20 slots but only 18 cooks
Status: Optimal
Average preference: 1.88888888889
                     date  preference
name                                 
Joey Brink     2016-08-02           3
Laura          2016-08-04           3
Sarah          2016-08-05           3
Sophia         2016-08-06           1
Kara           2016-08-07           2
Noah           2016-08-08           1
geoff          2016-08-09           1
Kevin Casto    2016-08-11           1
Kayla          2016-08-12           1
Will           2016-08-13           2
Asa            2016-08-14           2
Eric           2016-08-15           1
Chris q        2016-08-16           4
Jeff           2016-08-17           2
Michael        2016-08-17           3
Magnolia       2016-08-18           1
David Nekimken 2016-08-19           1
Sony           2016-08-20           2
```

### TODO
- add wildcard preferences for cooks who have insufficient preferences
- allow weighting of cook preferences this cycle by assignments last cycle
