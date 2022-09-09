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

This utility graphs the messages in a log file by address.  It can also print out messages that contain a pgn of interest for quick looks at groups of messages.  It depends on the messages collection of parsers so it should be run from the cloned directory.

standard usage: `python graph_log.py path/to/candump 61440` <- list of pgns of interest seperated by spaces



## Instalation for use:

### 1) Set up the repo

clone the repo: `git clone https://github.com/jLevere/J1939-Utils.git`
move into the repo `cd J1939-Utils`

### 2) Set up the virtual enviroment

first we will create a virtual enviroment called venv:

`python -m venv venv`

Then we will activate it:

Windows: `./venv/Scripts/activate.ps1` if you are using powershell

Everything else: `./venv/bin/activate`

And now we need to install the required libraries:

`pip install -r requirements.txt`

### 3) Finish

Everything should be finished, you can check for functionality by trying to start a virual listener with `python stream_msgs.py`


## Usage:

You probobly already know what you want to do with these tools but if you dont, lets capture some traffic from the pcan device and then graph its contents.

First we will capture some traffic:

`python stream_msgs.py pcan > ECU_CAN2_log1.candump`  

I like to name my files with .candump to keep track of them better.  It is also good to name them with the name of the bus channel you are using so you dont forget as the channel tagging isnt the best

Now lets see what we got:

`python graph_log.py ECU_CAN2_log1.candump`

This should print to stdout a nice graph of the messages seen on the bus as well as the NAME messages seen which can give you a decent idea of how many and what kind of controller applications are connected to the network.  Where a controler application is a particular function on the network.




