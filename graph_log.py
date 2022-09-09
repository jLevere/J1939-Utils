import json
import sys

from messages.j1939id import J1939ID as ID


def get_msgs(path: str) -> list[tuple]:
    """parses messages from candump format log file

    Args:
        path (str): the path to the file to read
    Returns:
        list[tuple], (time:float, channel:str, can_id:J1939ID, data:str)
    """

    messages: list[tuple] = []
    with open(path, 'r', encoding='UTF-8') as f:
        for line in f:
            line = line.strip()
            time, channel, message = line.split(' ')

            time = time.replace(')', '').replace('(', '').strip()
            time = float(time)

            can_id, data = message.split("#")
            messages.append((time, channel, ID(can_id), data))

    return messages


def seperate_by_address(messages: list[tuple]) -> dict:
    """Takes list of messages and builds dict with structure:

    src_addr:
            dest_addr
                    pgn
                        list[msg:str]

    Args:
        messages (list[tuple]): list of messages to proccess

    Returns:
        dict: dict of structure described above
    """

    src_dict = {}

    for line in messages:
        _, _, can_id, data = line

        if str(can_id.sa) not in src_dict:
            src_dict[str(can_id.sa)] = {}

        if str(can_id.da) not in src_dict[str(can_id.sa)]:
            src_dict[str(can_id.sa)][str(can_id.da)] = {}

        if str(can_id.pgn) not in src_dict[str(can_id.sa)][str(can_id.da)]:
            src_dict[str(can_id.sa)][str(can_id.da)][str(can_id.pgn)] = []

        src_dict[str(can_id.sa)][str(can_id.da)][str(can_id.pgn)
                                                 ].append(f"{str(can_id.hex)}#{data}")

    return src_dict


def get_names(messages: list[tuple]) -> dict:
    """Return a dict of names by src addr seen

    Args:
        messages (list[tuple]): (time:float, channel:str, can_id:J1939ID, data:str)

    Returns:
        dict: src : list[messages:tuple]
    """

    names_by_src = {}

    for line in messages:
        _, _, can_id, data = line

        if can_id.pgn == 60928:
            if str(can_id.sa) not in names_by_src:
                names_by_src[str(can_id.sa)] = []

            names_by_src[str(can_id.sa)].append(f"{can_id.hex}#{data}")

    return names_by_src


def validate_path(path:str) -> bool:
    """Check that there is a file and it can be read

    Args:
        path (str): path to file

    Returns:
        bool: file is ready
    """
    try:
        with open(path, 'r') as f:
            _ = f.readline()
        return True
    except FileNotFoundError:
        print("file not found, please try again")
        return False
    except Exception as e:
        print(f"something is wrong: {e}")
        return False
    



def main(path:str, pgns_of_interest:list[str]):
    """Main

    Args:
        path (str): path to file
        pgns_of_interest (list[str]): list of pgns to print
    """

    messages:list[tuple] = get_msgs(path)
    names:dict = get_names(messages)
    
    messages_by_src:dict = seperate_by_address(messages)


    print(
        f"NAME messages seen by src address:\n{json.dumps(names, indent=4)}\n")

    print("Breakdown of messages in log")
    print("src\tda\tpgn\tmsg_count")
    print("=================================")

    for src, da_dict in messages_by_src.items():

        print(f"{src}")
        print("|-------|")

        for da, pgn_dict in da_dict.items():

            print(f"\t{da}\n\t |")

            for pgn, msg_list in pgn_dict.items():

                print(f"\t |--- {pgn}\n\t |\t|---- {len(msg_list)}")

                if str(pgn) in pgns_of_interest:
                    print(msg_list)


if __name__ == '__main__':

    path = sys.argv[1] if len(sys.argv) > 1 else None
    pgns_of_interest = sys.argv[2:] if len(sys.argv) > 2 else []

    if not path:
        path = input("please enter path to candump format log: ")
        
        if not validate_path(path):
            sys.exit()
            
        pgn_str = input("enter pgns of interest seperated by spaces else enter: ")
        pgns_of_interest = pgn_str.split(" ")
        print("\n")

    if not validate_path(path): #TODO: should be fixed to be non redudant
        sys.exit()
        
    main(path, pgns_of_interest)
