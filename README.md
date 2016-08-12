usage: cook_scheduler.py [-h] [-e [EXCLUDE [EXCLUDE ...]]]
                         [-c [COMMUNITY [COMMUNITY ...]]] [-o OUTPUT]
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
  -o OUTPUT, --output OUTPUT
                        file to save schedule to
