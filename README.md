## cook_scheduler
This program generates a cook schedule given a list of date preferences for each cook. In particular, it uses linear programming to select a schedule minimizing the average cook preference.

### Usage
```
> python cook_scheduler.py --help
usage: cook_scheduler.py [-h] [-e [EXCLUDE [EXCLUDE ...]]]
                         [-c [COMMUNITY [COMMUNITY ...]]] [--csv CSV]
                         [--ical ICAL]
                         start end preferences

generate an cook cycle assignment from ranked date preferences

positional arguments:
  start                 date to start the cook cycle on (inclusive)
  end                   date to end the cook cycle on (inclusive)
  preferences           path to preferences csv file

optional arguments:
  -h, --help            show this help message and exit
  -e [EXCLUDE [EXCLUDE ...]], --exclude [EXCLUDE [EXCLUDE ...]]
                        dates to exclude from cook cycle
  -c [COMMUNITY [COMMUNITY ...]], --community [COMMUNITY [COMMUNITY ...]]
                        dates requiring two cooks
  --csv CSV             file to save schedule to
  --ical ICAL           file to save ical to
```

### Example
The repository contains sample preferences in the `data` directory. For example, to generate an optimal cook schedule for July and save it to `output.csv` and save an iCalendar to `calendar.ics`:
```
> python cook_scheduler.py 2016-07-31 2016-08-20 data/july_2016.csv -c 2016-08-17 --exclude 2016-08-03 2016-08-10 --csv output.csv --ical calendar.ics
WARNING:root:Sony  selected excluded dates: ['21-08-2016']
WARNING:root:There 20 slots but only 18 cooks
Status: Optimal
Average preference: 1.88888888889
WARNING:root:Unassigned dates: ['31-07-2016', '01-08-2016']
                      name  preference
date                                  
2016-07-31            None         NaN
2016-08-01            None         NaN
2016-08-02      Joey Brink         3.0
2016-08-04           Laura         3.0
2016-08-05           Sarah         3.0
2016-08-06          Sophia         1.0
2016-08-07            Kara         2.0
2016-08-08            Noah         1.0
2016-08-09           geoff         1.0
2016-08-11     Kevin Casto         1.0
2016-08-12           Kayla         1.0
2016-08-13            Will         2.0
2016-08-14             Asa         2.0
2016-08-15            Eric         1.0
2016-08-16         Chris q         4.0
2016-08-17            Jeff         2.0
2016-08-17         Michael         3.0
2016-08-18        Magnolia         1.0
2016-08-19  David Nekimken         1.0
2016-08-20           Sony          2.0
```

### TODO
- add wildcard preferences for cooks who have insufficient preferences
- allow weighting of cook preferences this cycle by assignments last cycle
