# J1939-Utils

Python utilities for interacting with J1939 and J1939 networks.

## Description

J1939-Utils is a collection of Python utilities designed to facilitate communication and analysis within J1939 networks. J1939 is a protocol suite commonly used in heavy-duty vehicles, providing a standardized way for electronic control units (ECUs) to communicate over a CAN bus. These utilities aim to simplify tasks such as message filtering, streaming, and graphing, making it easier to work with J1939 networks.

## Table of Contents

- [Current Utilities](#current-utilities)
  - [get_pgns.py](#get_pgns.py)
  - [stream_msgs.py](#stream_msgs.py)
  - [graph_log.py](#graph_log.py)
- [Installation](#installation)
- [Usage](#usage)
  - [Example 1: Filtering Messages by PGN](#example-1-filtering-messages-by-pgn)
  - [Example 2: Streaming Messages](#example-2-streaming-messages)
  - [Example 3: Graphing Messages](#example-3-graphing-messages)
- [Configuration](#configuration)
- [Notes](#notes)
- [License](#license)

## current utilies:

### `get_pgns.py`

This utility filters messages in a candump file by Parameter Group Number (PGN) and prints them to the standard output.

**Standard Usage:**

```sh
get_pgns.py log1.candump 61440
```

### stream_msgs.py

This utility streams received messages on a bus to the standard output in candump format. It can be attached to a virtual bus or a PCAN adapter.

**Standard Usage:**

```sh
python stream_msgs.py pcan
```

to save to a log file:

```sh
python stream_msgs.py pcan > log1.candump
```

### graph_log.py

This utility graphs messages in a log file by address and can also print out messages that contain specific PGNs of interest. It relies on a collection of parsers, so it should be run from the cloned directory.

**Standard Usage:**

```sh
python graph_log.py path/to/candump 61440
```

Sample output:

```sh
NAME messages seen by src address:
{}

Breakdown of messages in log
src     da      pgn     msg_count
=================================
0
|-------|
        255
         |
         |--- 61424
         |      |---- 25
         |--- 68247
         |      |---- 5
         |--- 65570
        18
         |
         |--- 0
         |      |---- 2
24
|-------|
        255
         |
         |--- 65235
         |      |---- 3
```

## Instalation for use:

To get started with J1939-Utils, follow these steps:

### 1) Set up the repo

`git clone https://github.com/jLevere/J1939-Utils.git`
move into the repo `cd J1939-Utils`

### 2) Set up the virtual enviroment

First, create a virtual environment called venv:

`python -m venv venv`

Then, activate it:

- On Windows (PowerShell):

```sh
./venv/Scripts/activate.ps1
```

- On other platforms:

```sh
./venv/bin/activate
```

Install the required libraries:

```sh
pip install -r requirements.txt
```

### 3) Finish

Your setup should now be complete. You can verify functionality by trying to start a virtual listener with:

```sh
python stream_msgs.py
```

## Usage:

Here are some common use cases for these tools:

### Example 1: Filtering Messages by PGN

You can use `get_pgns.py`` to filter messages in a candump file by PGN. For example, to filter messages with PGN 61440:

```sh
get_pgns.py log1.candump 61440
```

### Example 2: Streaming Messages

To stream received messages from a PCAN adapter and save them to a log file

```sh
python stream_msgs.py pcan > ECU_CAN2_log1.candump
```

### Example 3: Graphing Messages

To graph messages in a log file and specify PGNs of interest:

```sh
python graph_log.py path/to/candump 61440 65235
```

Running this command will generate a comprehensive graph in the standard output, providing insights into the messages observed on the bus. It also identifies NAME messages, giving you valuable information about the number and types of controller applications connected to the network. In this context, a controller application refers to a specific network function.

## Configuration

To configure `get_pgns.py`, you can utilize a `get_pgns.conf` file, which should follow a JSON structure with two essential fields: `path` and `pgns`. This configuration file simplifies repeated usage.

**Example `get_pgns.conf`:**

```json
{
  "path": "log1.candump",
  "pgns": [61440, 61447]
}
```

In this example, the `path` field specifies the file path, and the `pgns` field contains an array of PGNs to filter for.

## Notes:

I like the candump format for logs and messages therefor most of these utils use it in some form. Candump is roughly as follows:

(timestamp as float) channel can_id#data

example:
(1553794338.014188) vcan0 0C20130B#FCFFFA77FFFFFFFF

## License

This project is licensed under the MIT License. See the LICENSE file for details.
