"""
Allocate Bowers cook cycle.
"""

import pandas as pd
import random

# Information about this cycle
start_date = '6-6-2016'
end_date = '6-24-2016'
exclude_dates = ['6-8-2016', '6-22-2016']
community_dinners = ['6-15-2016']
fname = 'june_2016.csv'

dir_name = '/Users/gbrookshire/Documents/projects/bowers_cook_cycle/'
choice_cols = [u'Preferred day', u'Second choice', u'Third choice',
               u'Fourth choice', u'Fifth choice']
name_col = 'Your Name'


def format_date(s):
    month, day, year = s.split('-')
    if len(month) == 1:
        month = '0' + month
    return '-'.join([year, month, day])


# Read in the data
data = pd.read_csv(dir_name + fname)
date_range = pd.date_range(start_date, end_date)
# Kick out community dinners at other houses
date_range = date_range[~date_range.isin(exclude_dates)]
# Double the community dinner days so two people can sign up
date_range = [d.date().strftime('%Y-%m-%d') for d in date_range]
date_range.extend([format_date(d) for d in community_dinners])

# Sort dates by the number of times they were chosen (ascending)
all_choices = data[choice_cols[0]]
for i_col in range(1, len(choice_cols)):
    all_choices = all_choices.append(data[choice_cols[i_col]])
date_counts = all_choices.value_counts()
sorted_date_range = date_counts.keys().tolist()
sorted_date_range.reverse()

# Make date assignments
assignments = pd.DataFrame(columns = ['name', 'date', 'choice'])
unassigned_dates = []

for date in sorted_date_range:

    # Find people who chose this date as their top choice (highest if no top) 
    for n_choice in range(len(choice_cols)):
        col_name = choice_cols[n_choice]
        choosers = data[data[col_name] == date]
        if not choosers.empty:
            break

    # Randomly choose one of these people
    # If no one chose this date, go on to the next date
    if choosers.empty:
        unassigned_dates.append(date)
        continue
    else:
        i_winner = random.choice(range(choosers.shape[0]))
        winner = choosers.iloc[i_winner]

    # Note who won this date
    d = {'name': winner[name_col],
         'date': winner[choice_cols[n_choice]],
         'choice': n_choice + 1}
    assignments = assignments.append(d, ignore_index=True)

    # Remove the person and the date from circulation
    data = data[data[name_col] != winner[name_col]]


print 'Assignments:'
print assignments
print 'Unassigned dates:'
print unassigned_dates
print 'Remaining people:'
print data[name_col].tolist()
