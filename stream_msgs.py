"""Streams mesages from pcan adaptor to screen with one simple command
"""
import sys
import binascii

from can import ThreadSafeBus, Message
from bitarray.util import int2ba, ba2hex



config = {
    "channel": "vcan0",
    "bustype": "virtual",
    "bitrate": "250000",
}

def message_to_candump(msg: Message) -> tuple:
    """Convert can Message object to a tuple of (time, can_id, data)

    Args:
        msg (Message): incoming can Message object

    Returns:
        str: candump format msg
    """

    time = float(msg.timestamp)
    channel = msg.channel if msg.channel else 'can'

    # bytearray to string of hex
    data = binascii.hexlify(msg.data).decode()
    
    # all of this is to convert arbitration id to can_id
    # this can be either CBFF or CEFF type
    if msg.is_extended_id:
        can_id_bits = int2ba(msg.arbitration_id, 29)
    else:
        can_id_bits = int2ba(msg.arbitration_id, 11)

    can_id_bits.reverse()
    can_id_bits.fill()
    can_id_bits.reverse()

    can_id = ba2hex(can_id_bits)

    return f"({time}) {channel} {can_id}#{data}"


def main(bustype: str = None):
    """Read messages from source.  If no bustype, then use virtual interface

    Args:
        bustype (str, optional): bustype, usually this should be pcan. Defaults to None.
    """

    bustype = str(bustype) if bustype else config['bustype']
    channel = 'PCAN_USBBUS1' if bustype else config['channel']

    bus = ThreadSafeBus(channel=channel,
                        bustype=bustype, bitrate=config['bitrate'])

    count = 0
    try:
        print(
            f"running with config: channel: {bus.channel_id if hasattr(bus, 'channel_id') else 'can'}, channel_info: {bus.channel_info}")
        for msg in bus:
            count += 1

            if not msg.error_state_indicator:
                print(message_to_candump(msg))
            else:
                print(msg)

    except KeyboardInterrupt:
        print(f"msgs seen: {count}")
        print("bye")

    finally:
        bus.shutdown()


if __name__ == '__main__':
    bustype = sys.argv[1] if len(sys.argv) > 1 else None
    print("if no args: virutal, ex usage: python stream_msgs.py pcan")
    main(bustype)
