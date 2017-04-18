ics files allow us to move calendar events between calendaring systems (e.g.,
Google and Exchange).  The problem is that they get big... and cloud-based
systems aren't much good at uploading large ICS files (e.g., Google has a
ridiculously small threshold - something like 500 Kb).

This utility works around this by letting you extract events by years, making
smaller ics files that can (hopefully) be uploaded serially.

Basic usage for this tool is:

	python ics_splitter.py my_big_file.ics 2016 my_2016_events.ics

Replace the arguments with your big file, the year you want to extract and the
file you want to write the extracted events into. Note that, in addition to the
events, the script pulls out all the boilerplate stuff (like timezones and
such) that are sometimes required to make a valid ics file.

Enjoy!

