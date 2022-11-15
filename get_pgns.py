"""
get_pgns.py

    Running options:
        1) cmd args
            get_pgns.py path_to_logs pgn1 pgn3 pgn3...

        2) config file
            get_pgns.py (checks for presense of get_pgns.conf and sets the arguments with that)

            conf file format:
            {
                "path": "path/to/file",
                "pgns: [
                    "pgn1",
                    "pgn2"
                ]
            }

        3) interative session
            get_pgns.py (no conf file, no arguments) -> interactive mode

"""
import sys
import json
import chardet

from messages.j1939id import J1939ID


def get_msgs(path: str) -> list:
    """gets msgs from file and returns list

    Args:
        path (str): path to file

    Returns:
        list: list of messages
    """
    messages: list[tuple] = []
    try:
        with open(path, 'rb') as f:
            ch = chardet.detect(f.readline())
            encoding = ch['encoding']

        with open(path, 'r', encoding=encoding) as f:
            for line in f:
                line = line.strip()
                time, channel, message = line.split(' ')

                time = time.replace(')', '').replace('(', '').strip()
                time = float(time)

                can_id, data = message.split("#")
                messages.append((time, channel, J1939ID(can_id), data))

        return messages

    except FileNotFoundError:
        print("file not found, please try again")
        sys.exit()


def get_args() -> tuple:
    """returns path and list of pgns of interest

    Returns:
        tuple: (path, [pgns])
    """
    if len(sys.argv) > 2:
        path = sys.argv[1]
        interest_pgns = sys.argv[2:]

    elif conf_file():
        with open(f"{__file__}.conf", 'r') as f:
            conf = json.loads(f)
        path = conf['path']
        interest_pgns = conf['pgns']

    else:
        path = input("enter path to candump file: ")
        pgn_str = input("enter pgns of interest seperated by spaces: ")
        interest_pgns = pgn_str.split()

    return (path, interest_pgns)


def conf_file() -> bool:
    """check for presense of conf file

    conf file format:
        {
            "path": "path/to/file",
            "pgns: [
                "pgn1",
                "pgn2"
            ]
        }

    Returns:
        bool: conf file is present and working
    """
    try:
        with open(f"{__file__}.conf", 'r', encoding='UTF-8') as f:
            return True
    except FileNotFoundError:
        return False


class PGN_Filter():
    """Creates an iterator of messages filtered by their pgn values

    Args:
        interest_pgns (list): list of pgns to return

        messages: (list[tuple[timestamp, channel, can_id, data]]): list of messages to filter
    """

    def __init__(self,
                 interest_pgns: list,
                 messages: list[tuple[float, str, J1939ID, str]]) -> None:

        self._interest_pgns: list = interest_pgns
        self._messages: list[tuple[float, str, J1939ID, str]] = messages

    def __iter__(self) -> iter:
        """Iterator for values

        Returns:
            iter: iterator

        Yields:
            Iterator[iter]: iterator
        """

        for msg in self._messages:
            _, _, can_id, data = msg

            if str(can_id.pgn) in self._interest_pgns:
                yield f"{can_id.hex}#{data}"


def main():

    path, interest_pgns = get_args()

    messages: tuple = get_msgs(path)

    results = PGN_Filter(interest_pgns=interest_pgns, messages=messages)

    for result in results:
        print(result)


if __name__ == '__main__':
    main()
