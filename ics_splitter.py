"""
A handy script for extracting all events from a particular year 
from an ICS file into another ICS file.

@author Derek Ruths (druths@networkdynamics.org)
"""

import argparse
import re
import sys, os
from datetime import datetime
from datetime import timedelta

parser = argparse.ArgumentParser()
parser.add_argument('input_file',help='the input ICS file')
parser.add_argument('schedule_from',help='the date which from schedules are extract: %Y%m%d')
parser.add_argument('schedule_to', help='the date which to schedules are extract: %Y%m%d')
parser.add_argument('output_file',help='the output ICS file')

args = parser.parse_args()

print 'Extracting %s ~ %s events from %s into %s' % (args.schedule_from, args.schedule_to ,args.input_file,args.output_file)

schedule_from = datetime.strptime(args.schedule_from, '%Y%m%d')
schedule_to = datetime.strptime(args.schedule_to, '%Y%m%d')
range_in_date = [schedule_from + timedelta(days=x) for x in range(0, (schedule_to-schedule_from).days)]

in_fname =  args.input_file
out_fname = args.output_file

if os.path.exists(out_fname):
	print 'ERROR: output file already exists! As a safety check, this script will not overwrite an ICS file'
	exit()

infh = open(in_fname,'r')
outfh = open(out_fname,'w')

# parsing constants
BEGIN_CALENDAR = 'BEGIN:VCALENDAR'
END_CALENDAR = 'END:VCALENDAR'
BEGIN_EVENT = 'BEGIN:VEVENT'
END_EVENT = 'END:VEVENT'

CREATED2017_OPENER = 'CREATED:2017'

in_preamble = True
in_event = False
event_content = None
event_in_2017 = False

event_count = 0
out_event_count = 0

for line in infh:

	if in_preamble and line.startswith(BEGIN_EVENT):
		in_preamble = False

	if in_preamble:
		outfh.write(line)
	else:
		if line.startswith(BEGIN_EVENT):
			event_content = []
			event_count += 1
			event_in_2017 = False
			in_event = True

		if in_event:
			if 'DTSTART' in line:
				event_string = re.split(r'DTSTART.*:', line)[1].split('T')[0]
				event_date = datetime.strptime(event_string.strip(), '%Y%m%d')
				if event_date in range_in_date:
					event_in_2017 = True
			event_content.append(line)

		if line.startswith(END_EVENT):
			in_event = False

			if event_in_2017:
				out_event_count += 1
				outfh.write(''.join(event_content))

outfh.write(END_CALENDAR)
outfh.close()

# done!
print 'wrote %d of %d events' % (out_event_count,event_count)
			

	
