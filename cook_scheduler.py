import pandas as pd
import argparse
from pulp import *
from icalendar import *

def create_parser():
    parser = argparse.ArgumentParser(description='generate an cook cycle assignment from ranked date preferences')
    parser.add_argument('-e', '--exclude', type=pd.Timestamp, nargs='*',
	help='dates to exclude from cook cycle')
    parser.add_argument('-c', '--community', type=pd.Timestamp, nargs='*',
	help='dates requiring two cooks')
    parser.add_argument('--csv', type=str,
	help='file to save schedule to'),
    parser.add_argument('--ical', type=str,
	help='file to save ical to'),
    parser.add_argument('start', type=pd.Timestamp,
	help='date to start the cook cycle on  (inclusive)')
    parser.add_argument('end', type=pd.Timestamp,
	help='date to end the cook cycle on (inclusive)')
    parser.add_argument('preferences', type=str,
	help='path to preferences csv file')
    return parser

def get_preferences(data, dates):
    """
    Extract preferences from survey responses table. Also excludes any invalid dates.

    Args:
        data: date preferences DataFrame. data['Your Name'] contains names
            and preferences are in decreasing order from the third column on
        dates: list of all valid dates
    
    Returns: a dictionary of (name, dates) pairs where dates is a list of valid
        dates in decreasing order
    """
    preferences = {}
    for i,person in data.iterrows():
	name = person['Your Name']
	
	p = person[2:].values
	if not dates.issuperset(p):
	    bad_dates = set(p).difference(dates)
	    logging.warning('%s selected excluded dates: %s' % 
		    (name, print_dates(bad_dates)))
	    p = [d for d in p if d in dates]

	preferences[name] = p

    return preferences

def create_problem(dates, community, preferences):
    """
    Create the cook schedule linear programming problem

    Args:
        dates: list of cook cycle dates
        community: list of cook cycle dates requring two cooks
        preferences: dictionary of (name, dates) pairs as returned by get_preferences()
    
    Returns: 
	prob: LpProblem object
	variables: a dictionary of (name, variables) pairs
	    where variables is a dictionary of (date, LpVariable)
            pairs
    """
    names = preferences.keys()
    variables = {name: {d: LpVariable('%s %s' % (name,d), cat=LpBinary) for d in p}
	for name,p in preferences.items()}

    slots = len(dates) + len(community)
    if len(names) < slots:
	logging.warning('There %s slots but only %s cooks' % (slots, len(names)))

    prob = LpProblem("Cook Cycle",LpMinimize)

    # the objective is to minimize the average preference number
    objective = LpAffineExpression()
    for name in names:
	objective += sum((i+1)*variables[name][d] 
		for i,d in enumerate(preferences[name]))
    prob += objective / float(len(names))

    # each person cooks once on their days
    for name in names:
	prob += sum(variables[name][d] for d in preferences[name]) == 1

    # each regular date has at most one cook
    for d in dates.difference(community):
	prob += sum(variables[name][d] for name in names if d in preferences[name]) <= 1

    # each community dinner date has at most two cooks
    for d in community:
	prob += sum(variables[name][d] for name in names if d in preferences[name]) <= 2

    return prob, variables

# These constants indexed by day of week (starting Monday)
# Used by to_icalendar()
MEAL_NAMES = ['Dinner', 'Dinner', 'Dinner', 'Dinner',  'Dinner', 
              'Brunch', 'Dinner']
# The time of day, in hours at which each meal begins
# Each meal is scheduled to last one hour
MEAL_TIMES = [17, 17, 17.5, 17, 17.5, 12, 17]

def to_icalendar(schedule, community=None):
    """
    Args:
        schedule: dataframe schedule

    Returns:
        icalendar.Calendar object
    """
    calendar = Calendar()
    for date, names in schedule.groupby('date').groups.items():
        event = Event()
        date = pd.Timestamp(date) # the groupby makes date a datetime64
       
        event.add('summary', '%s %s' % 
                (str.join(' & ', names), MEAL_NAMES[date.dayofweek]))

        time = MEAL_TIMES[date.dayofweek]
        event.add('dtstart', (date + pd.Timedelta(time,'h')).to_datetime())
        event.add('dtend', (date + pd.Timedelta(time+1,'h')).to_datetime())
        event.add('location', 'Bowers House')

        calendar.add_component(event)

    return calendar

def print_dates(dates):
    return map(lambda d: d.strftime('%d-%m-%Y'), dates)

if __name__ == '__main__':
    parser = create_parser()
    args = parser.parse_args()
    data = pd.read_csv(args.preferences, parse_dates=range(2,7))

    dates = set(pd.date_range(args.start, args.end))\
	.difference(pd.Series(args.exclude))

    preferences = get_preferences(data, dates)

    prob, variables = create_problem(dates, pd.Series(args.community), preferences)

    prob.solve()
    print("Status: %s" % LpStatus[prob.status])
    print("Average preference: %s" % value(prob.objective))

    schedule = [] # collection of tuples (name, date, rank)
    assigned = set()
    for name in data['Your Name']:
        for d,v in variables[name].items():
            if v.value() == 1.0:
                schedule.append((name, d, list(preferences[name]).index(d)+1))
                assigned.add(d)

    unassigned = dates.difference(assigned)
    if len(unassigned) > 0:
        logging.warning('Unassigned dates: %s' % print_dates(unassigned))
        schedule += [('',d, None) for d in unassigned]


    df = pd.DataFrame(schedule, columns=['name', 'date', 'preference']).set_index('name').sort_values('date')
    print df

    if args.csv:
        df.to_csv(args.csv)

    if args.ical:
        calendar = to_icalendar(df, args.community)
        with open(args.ical, 'wb') as f:
            f.write(calendar.to_ical())
