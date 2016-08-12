import pandas as pd
import argparse
from pulp import *
from datetime import date, timedelta

def create_parser():
    parser = argparse.ArgumentParser(description='generate an cook cycle assignment from ranked date preferences')
    parser.add_argument('-e', '--exclude', type=pd.Timestamp, nargs='*',
	help='dates to exclude from cook cycle')
    parser.add_argument('-c', '--community', type=pd.Timestamp, nargs='*',
	help='dates requiring two cooks')
    parser.add_argument('-o', '--output', type=str,
	help='file to save schedule to')
    parser.add_argument('start', type=pd.Timestamp,
	help='date to start the cook cycle on  (inclusive)')
    parser.add_argument('end', type=pd.Timestamp,
	help='date to end the cook cycle on (inclusive)')
    parser.add_argument('preferences', type=str,
	help='path to preferences csv file')
    return parser

def create_problem(start, end, data, exclude, community):
    # generate list of eligible dates
    dates = set(pd.date_range(start, end))
    dates = dates.difference(exclude)

    names = []
    variables = {}
    preferences = {}

    for i,person in data.iterrows():
	name = person['Your Name']
	names.append(name)
	
	p = person[2:].values
	if not dates.issuperset(p):
	    bad_dates = set(p).difference(dates)
	    logging.warning('%s selected excluded dates: %s' % 
		    (name, bad_dates))
	    p = [d for d in p if d in dates]

	preferences[name] = p
	variables[name] = {d: LpVariable('%s %s' % (name,d), cat=LpBinary) 
		for d in p}

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

    return prob, variables, preferences

if __name__ == '__main__':
    parser = create_parser()
    args = parser.parse_args()
    data = pd.read_csv(args.preferences, parse_dates=range(2,7))

    prob, variables, preferences = create_problem(args.start, args.end, data, pd.Series(args.exclude), pd.Series(args.community))

    prob.solve()
    print("Status: %s" % LpStatus[prob.status])
    print("Average preference: %s" % value(prob.objective))

    schedule = []
    for name in data['Your Name']:
        for d,v in variables[name].items():
            if v.value() == 1.0:
                schedule.append((name, d, list(preferences[name]).index(d)+1))

    schedule = pd.DataFrame(schedule, columns=['name', 'date', 'preference']).set_index('name').sort_values('date')
    print schedule 

    if args.output:
        schedule.to_csv(args.output)
