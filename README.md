# J1939-Utils
Python utilities for interacting with J1939 and J1939 networks


I like candump format for logs and messages therefor most of these utilites use it in some form.  

candump is roughly as follows:

(timestamp as float) channel can_id#data

example:

(1553794338.014188) vcan0 0C20130B#FCFFFA77FFFFFFFF

## Current utilies:

### stream_msgs.py

This utility streams recived messages on a bus to stdout in candump format.  It can either be attached to a virtual bus or to a pcan adapter currently.

standard usage: `python stream_msgs.py pcan` streams the recived messages from a connected pcan adaptor.  

to save to a log file:  `python stream_msgs.py pcan > log1.candump`

### graph_log.py

This utility graphs the messages in a log file by address.  It can also print out messages that contain a pgn of interest for quick looks at groups of messages.

standard usage: `python graph_log.py path/to/candump 61440` <- list of pgns of interest seperated by spaces




