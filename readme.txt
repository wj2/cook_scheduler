usage: cook_scheduler.py [-h] [-e EXCLUDE_DATES [EXCLUDE_DATES ...]]
                         [-c COMMUNITY_DINNERS [COMMUNITY_DINNERS ...]]
                         [-o OUTPUT]
                         start_date end_date preferences

generate an cook cycle assignment based on n ranked preferences

positional arguments:
  start_date            date to start the cook cycle on (inclusive)
  end_date              date to end the cook cycle on (inclusive)
  preferences           path to list of date preferences, dates should be in
                        YYYY-MM-DD form, the file should be a csv

optional arguments:
  -h, --help            show this help message and exit
  -e EXCLUDE_DATES [EXCLUDE_DATES ...], --exclude_dates EXCLUDE_DATES [EXCLUDE_DATES ...]
                        list of dates to exclude from cook cycle (YYYY-MM-DD
                        format), must be within start and end dates above
  -c COMMUNITY_DINNERS [COMMUNITY_DINNERS ...], --community_dinners COMMUNITY_DINNERS [COMMUNITY_DINNERS ...]
                        list of dates on which the house requires two cooks
  -o OUTPUT, --output OUTPUT
                        file to save schedule to(default
                        <start>_to_<end>_cookcycle.csv
